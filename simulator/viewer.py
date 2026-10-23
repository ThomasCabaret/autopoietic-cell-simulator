"""Optional Pygame consumer. The worker owns physics, clocks, RNG and checkpoints."""
import json
import os
from pathlib import Path
import queue
import threading
import time
import traceback
import numpy as np

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
import pygame
from .engine import Simulation
from .config import legacy
from .runner import make_observer,create_output,save_result,compact
from . import checkpoint

BG='#eef2f5'
INK='#24364b'


class Controller:
    def __init__(self,config,parent,record=True,resume=None):
        self.config,self.parent,self.record,self.resume=config,parent,record,resume
        self.commands=queue.Queue()
        self.frames=queue.Queue(maxsize=1)
        self.startup_error=None
        self.thread=threading.Thread(target=self.work,daemon=False)
        self.thread.start()

    def send(self,action):
        self.commands.put(action)

    def publish(self,sim,obs,path,paused,rate,error=None):
        state=sim.snapshot()
        state.update(config=sim.config,metrics=compact(obs.summary()) if obs.times else {},
                     paused=paused,rate=rate,error=error,path=str(path.resolve()))
        if self.frames.full():
            try: self.frames.get_nowait()
            except queue.Empty: pass
        self.frames.put_nowait(state)

    def work(self):
        sim=obs=path=None
        start=time.perf_counter()
        paused=False
        saved=False
        speed=0
        rate=0.
        last_publish=last_rate=time.monotonic()
        last_step=0
        error=None
        try:
            if self.resume:
                sim,obs=checkpoint.load(self.resume,make_observer)
            else:
                sim=Simulation(self.config)
                obs=make_observer(sim.config,self.record)
                sim.listeners.append(obs)
            path=create_output(sim.config,self.parent)
            sim.advance(0)
            self.publish(sim,obs,path,paused,rate)
            stop=False
            while not stop:
                single=False
                while not self.commands.empty():
                    action=self.commands.get_nowait()
                    if action=='stop': stop=True
                    elif action=='pause': paused=not paused
                    elif action=='step': paused=True; single=True
                    elif action=='save': checkpoint.save(path/'user_checkpoint.npz',sim,obs)
                    elif action=='load':
                        candidate=path/'user_checkpoint.npz'
                        if candidate.exists():
                            sim,obs=checkpoint.load(candidate,make_observer)
                            paused=True
                            saved=False
                    elif action=='restart':
                        save_result(path,sim,obs,time.perf_counter()-start)
                        sim=Simulation(sim.config)
                        obs=make_observer(sim.config,self.record)
                        sim.listeners.append(obs)
                        path=create_output(sim.config,self.parent)
                        start=time.perf_counter()
                        paused=saved=False
                        last_step=0
                        sim.advance(0)
                    elif isinstance(action,tuple) and action[0]=='speed': speed=action[1]
                if stop: break
                before=time.monotonic()
                if single or (not paused and not sim.done):
                    sim.advance(1 if single else 50)
                if sim.done and not saved:
                    save_result(path,sim,obs,time.perf_counter()-start)
                    saved=True
                now=time.monotonic()
                if now-last_rate>=.5:
                    rate=(sim.step_index-last_step)/(now-last_rate)
                    last_rate,last_step=now,sim.step_index
                if now-last_publish>=.04 or single:
                    self.publish(sim,obs,path,paused,rate)
                    last_publish=now
                if paused or sim.done: time.sleep(.01)
                elif speed: time.sleep(max(0.,50/speed-(time.monotonic()-before)))
        except Exception as exc:
            error=f'{type(exc).__name__}: {exc}'
            self.startup_error=error
            if path:
                (path/'error.txt').write_text(traceback.format_exc(),encoding='utf-8')
            traceback.print_exc()
        finally:
            if sim is not None and path is not None:
                if not saved:
                    save_result(path,sim,obs,time.perf_counter()-start,error)
                self.publish(sim,obs,path,True,rate,error)


class Canvas:
    def __init__(self,screen):
        self.screen=screen
        self.font=pygame.font.SysFont('segoeui',17)
        self.small=pygame.font.SysFont('segoeui',14)
        self.bold=pygame.font.SysFont('segoeui',22,bold=True)
        self.zoom=1.
        self.pan=np.zeros(2)
        self.center=None
        self.extent=1.
        self.buttons={}

    def fit(self,state):
        pos=state['positions']
        if state.get('box'):
            lo=np.zeros(2); hi=np.array(state['box'])
        else:
            lo,hi=pos.min(axis=0),pos.max(axis=0)
        self.center=(lo+hi)/2
        self.extent=max(float((hi-lo).max()),2.)*1.17
        self.zoom=1.; self.pan[:]=0

    def text(self,value,x,y,color=INK,font=None):
        self.screen.blit((font or self.font).render(str(value),True,color),(x,y))

    def wrap(self,text,x,y,width,lines=5):
        words=str(text).split(); line=''; count=0
        for word in words:
            test=(line+' '+word).strip()
            if self.small.size(test)[0]>width and line:
                self.text(line,x,y,font=self.small); y+=20; count+=1; line=word
                if count>=lines: return y
            else: line=test
        if line: self.text(line,x,y,font=self.small); y+=20
        return y

    def draw(self,state,mode='live',speed='Max'):
        w,h=self.screen.get_size()
        side=320
        area=pygame.Rect(0,0,max(100,w-side),h)
        self.screen.fill(BG)
        pygame.draw.rect(self.screen,'#ffffff',area)
        if self.center is None: self.fit(state)
        scale=min(area.width,area.height)/self.extent*self.zoom
        p=(state['positions']-self.center)*np.array([scale,-scale])+np.array([area.centerx,area.centery])+self.pan
        def pt(i): return tuple(np.rint(p[i]).astype(int))
        self.screen.set_clip(area)
        if state.get('box'):
            box=np.array(state['box'])
            corner=(np.array([0.,box[1]])-self.center)*[scale,-scale]+[area.centerx,area.centery]+self.pan
            pygame.draw.rect(self.screen,'#dce4ea',pygame.Rect(*corner,*(box*scale)),1)
        for group,color,width in [('scaffold','#bac6cf',2),('pairing','#c795d5',2),('backbone','#536e82',3)]:
            for a,b in state['bonds'].get(group,[]): pygame.draw.line(self.screen,color,pt(a),pt(b),width)
        radius=max(3,min(11,round(scale*.105)))
        for i,color in enumerate(state['colors']):
            pygame.draw.circle(self.screen,color,pt(i),radius)
            pygame.draw.circle(self.screen,'#ffffff',pt(i),radius,1)
        self.screen.set_clip(None)
        x=area.right+18; y=18
        self.text('Chimie locale',x,y,font=self.bold); y+=38
        config=state['config']
        y=self.wrap(config['name'],x,y,285,2)+7
        y=self.wrap(config.get('description',''),x,y,285,4)+8
        self.text('RELECTURE' if mode=='replay' else 'SIMULATION',x,y,color='#687c8d'); y+=28
        self.text(f"Graine {config['seed']}  |  {len(p)} billes",x,y); y+=28
        self.text(f"Temps : {state['time']:.2f} / {config['duration']:g}",x,y); y+=27
        progress=min(1.,state['time']/config['duration'])
        bar=pygame.Rect(x,y,280,7)
        pygame.draw.rect(self.screen,'#dbe4ea',bar,border_radius=3)
        pygame.draw.rect(self.screen,'#148e9c',pygame.Rect(x,y,round(280*progress),7),border_radius=3)
        self.timeline=pygame.Rect(x,y-4,280,16); y+=23
        status='Erreur' if state.get('error') else ('Terminee' if state['done'] else ('Pause' if state.get('paused') else 'En cours'))
        self.text(status,x,y,color='#b34545' if state.get('error') else '#148e9c'); y+=27
        metrics=state.get('metrics',{})
        if config['model']=='copy':
            labels=[('G complets liberes','detached_copy_sets_ever'),('F complets liberes','translated_detached_ever'),
                    ('Generation >= 2 liberee','certified_detached_generation2'),('Ligations','ligation_events')]
            if 'food_products' in metrics:
                labels=[('F complets liberes','translated_detached_ever'),('Produits XY','food_products'),
                        ('Ligations sur F exprimes','food_expressed_tool_ligations'),
                        ('Cycles max / F exprime','food_max_turnovers_per_expressed_tool')]
        elif config['model']=='catalysis':
            labels=[('Produits','products'),('Ligations co-liees','double_bound_ligations')]
        else: labels=[('Boucles observees','closed_sets_ever'),('Plus grand fragment','final_largest_component')]
        for label,key in labels:
            self.text(f'{label} : {metrics.get(key,0)}',x,y); y+=25
        if config['model']=='copy':
            self.text('Comptes hors polymere initial.',x,y,font=self.small); y+=24
        self.text(f"{state.get('rate',0):,.0f} pas/s  |  rendu 30 Hz",x,y,font=self.small); y+=32
        self.buttons={}
        button_index=0
        for key,label in [('pause','Reprendre' if state.get('paused') else 'Pause'),('step','Un pas'),
                          ('restart','Recommencer'),('speed','Vitesse : '+str(speed)),
                          ('save','Sauver [S]'),('load','Charger [L]'),('fit','Centrer [F]')]:
            if mode=='replay' and key in ('step','save','load'): continue
            rect=pygame.Rect(x+(button_index%2)*144,y+(button_index//2)*39,136,32)
            pygame.draw.rect(self.screen,'#e0e8ee',rect,border_radius=5)
            self.text(label,rect.x+7,rect.y+5,font=self.small)
            self.buttons[key]=rect
            button_index+=1
        y+=((button_index+1)//2)*39
        if state.get('error'): y=self.wrap(state['error'],x,y,280,4)
        y=max(y+5,h-76)
        self.text('Molette : zoom | glisser : deplacer',x,y,font=self.small)
        self.text('Espace : pause | N : pas | R : debut',x,y+21,font=self.small)
        self.text('Sorties : outputs/ (config + preuves)',x,y+42,font=self.small)


def start_window():
    pygame.init()
    info=pygame.display.Info()
    screen=pygame.display.set_mode((min(1200,max(960,info.current_w-60)),min(900,max(720,info.current_h-80))),pygame.RESIZABLE)
    pygame.display.set_caption('Chimie locale — simulateur')
    return screen,Canvas(screen)


def live_view(config,parent='outputs',record=True,resume=None):
    screen,canvas=start_window()
    controller=Controller(config,parent,record,resume)
    state=None; running=True; drag=False; speeds=[0,500,2000,5000]; speed_index=0
    clock=pygame.time.Clock()
    while running:
        while not controller.frames.empty(): state=controller.frames.get_nowait()
        for event in pygame.event.get():
            action=None
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                action={pygame.K_SPACE:'pause',pygame.K_n:'step',pygame.K_r:'restart',pygame.K_s:'save',pygame.K_l:'load',pygame.K_f:'fit'}.get(event.key)
                if event.key==pygame.K_ESCAPE: running=False
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                action=next((k for k,r in canvas.buttons.items() if r.collidepoint(event.pos)),None)
                drag=action is None and event.pos[0]<screen.get_width()-320
            elif event.type==pygame.MOUSEBUTTONUP: drag=False
            elif event.type==pygame.MOUSEMOTION and drag: canvas.pan+=event.rel
            elif event.type==pygame.MOUSEWHEEL: canvas.zoom=np.clip(canvas.zoom*1.15**event.y,.1,20.)
            if action=='fit' and state: canvas.fit(state)
            elif action=='speed':
                speed_index=(speed_index+1)%len(speeds)
                controller.send(('speed',speeds[speed_index]))
            elif action: controller.send(action)
        if state: canvas.draw(state,speed='Max' if speed_index==0 else f'{speeds[speed_index]} pas/s')
        else:
            screen.fill(BG)
            if controller.startup_error:
                canvas.wrap(controller.startup_error,40,50,800,8)
            else: canvas.text('Preparation du moteur CPU (premiere compilation possible)...',40,50)
        pygame.display.flip(); clock.tick(30)
    controller.send('stop')
    while controller.thread.is_alive():
        pygame.event.pump(); controller.thread.join(.05)
    pygame.quit()


def replay_view(folder,screenshot=None):
    folder=Path(folder)
    result=json.loads((folder/'result.json').read_text(encoding='utf-8'))
    config=result.get('scenario') or legacy(result['config'])
    with np.load(folder/'trajectory.npz',allow_pickle=False) as d:
        positions=d['positions']; times=d['times']; edges=d['edges']
        n=positions.shape[1]//2
        bits=d['recognition_types'] if 'recognition_types' in d else np.zeros(n,dtype=int)
        families=d['families'] if 'families' in d else np.zeros(n,dtype=int)
        pairing=d['pairing'] if 'pairing' in d else None
        food_edges=d['food_edges'] if 'food_edges' in d else None
        food_binding=d['food_binding'] if 'food_binding' in d else None
        if config['model']=='copy': n=len(bits)
    screen,canvas=start_window()
    clock=pygame.time.Clock(); t=0.; paused=False; running=True; speed=20.; drag=False
    history=result['metrics'].get('history',[])
    history_times=np.array([x['time'] for x in history])
    if screenshot: t=float(times[-1])
    while running:
        elapsed=clock.tick(30)/1000
        for event in pygame.event.get():
            action=None
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: running=False
                action={pygame.K_SPACE:'pause',pygame.K_r:'restart',pygame.K_f:'fit'}.get(event.key)
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                action=next((k for k,r in canvas.buttons.items() if r.collidepoint(event.pos)),None)
                if hasattr(canvas,'timeline') and canvas.timeline.collidepoint(event.pos):
                    t=(event.pos[0]-canvas.timeline.left)/canvas.timeline.width*times[-1]
                drag=event.pos[0]<screen.get_width()-320
            elif event.type==pygame.MOUSEBUTTONUP: drag=False
            elif event.type==pygame.MOUSEMOTION and drag: canvas.pan+=event.rel
            elif event.type==pygame.MOUSEWHEEL: canvas.zoom=np.clip(canvas.zoom*1.15**event.y,.1,20.)
            if action=='pause': paused=not paused
            elif action=='restart': t=0.
            elif action=='speed': speed=5. if speed==100. else (100. if speed==20. else 20.)
            elif action=='fit': canvas.center=None
        if not paused: t=min(float(times[-1]),t+elapsed*speed)
        index=min(len(times)-1,int(np.searchsorted(times,t)))
        bonds={'scaffold':[(i,n+i) for i in range(n)],'backbone':[],'pairing':[]}
        if config['model']=='catalysis':
            bonds={'scaffold':[],'backbone':[],'pairing':[]}
            for i,j in np.argwhere(np.triu(edges[index],1)):
                group='scaffold' if j<3 else ('pairing' if i<3 else 'backbone')
                bonds[group].append((int(i),int(j)))
            symbols=[int(b) for b in config['chemistry']['sequence']]+[i%2 for i in range(len(positions[index])-3)]
            colors=[('#275f94' if b==0 else '#9a4aa0') if i<3 else ('#148e9c' if b==0 else '#df7947') for i,b in enumerate(symbols)]
        elif config['model']=='copy':
            bonds['backbone']=np.argwhere(np.triu(edges[index],1)).tolist()
            if pairing is not None:
                bonds['pairing']=[(n+i,n+int(j)) for i,j in enumerate(pairing[index]) if j>i]
            colors=['#718594' if f==0 else '#9a4aa0' for f in families]+[['#148e9c','#df7947','#8d75bb'][int(b)] for b in bits]
            if food_edges is not None:
                bonds['backbone'] += [(2*n+int(a),2*n+int(b)) for a,b in np.argwhere(np.triu(food_edges[index],1))]
                bonds['pairing'] += [(n+i,2*n+int(f)) for i,f in enumerate(food_binding[index]) if f>=0]
                colors += ['#148e9c' if f%2==0 else '#df7947' for f in range(len(food_edges[index]))]
        else:
            for row in (0,1): bonds['backbone'] += [(row*n+int(i),row*n+int(j)) for i,j in np.argwhere(np.triu(edges[index,row],1))]
            colors=['#148e9c']*n+['#df7947']*n
        hi=max(0,int(np.searchsorted(history_times,t,side='right'))-1)
        item=history[hi] if history else {}
        metrics=dict(result['metrics']) if t>=times[-1] else {}
        if food_edges is not None:
            events=[e for e in result['metrics']['food_events'] if e['time']<=times[index]]
            turnovers={}
            for e in events:
                if e['expressed_certified']:
                    key=tuple(e['chain']);turnovers[key]=turnovers.get(key,0)+1
            metrics.update(food_products=int(np.count_nonzero(food_edges[index]))//2,
                food_expressed_tool_ligations=sum(turnovers.values()),
                food_max_turnovers_per_expressed_tool=max(turnovers.values(),default=0))
        metrics.update({key:item[old] for key,old in [('detached_copy_sets_ever','detached_ever'),('translated_detached_ever','translated_detached_ever'),('final_largest_component','largest_head_component')] if old in item})
        if config['model']=='catalysis':
            for key in ('products','double_bound_ligations'):
                if key in item: metrics[key]=item[key]
        if 'closed' in item and t<times[-1]: metrics['closed_sets_ever']=len(item['closed'])
        state={'positions':positions[index],'bonds':bonds,'colors':colors,'config':config,'time':float(times[index]),
               'done':t>=times[-1],'paused':paused,'rate':0,'metrics':metrics,'box':config['chemistry'].get('box')}
        canvas.draw(state,'replay',f'{speed:g} unites/s')
        pygame.display.flip()
        if screenshot:
            Path(screenshot).parent.mkdir(parents=True,exist_ok=True)
            pygame.image.save(screen,str(screenshot)); running=False
    pygame.quit()
