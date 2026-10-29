"""Qt desktop shell. All graphical decisions stay in this process."""
from collections import deque
from datetime import datetime
import json
from pathlib import Path
import time
import numpy as np
import moderngl
from PySide6 import QtCore,QtGui,QtWidgets,QtOpenGLWidgets
from .camera import Camera
from .scene import Selection
from .renderer import Renderer
from .worker import ProcessSource

Q=QtWidgets

STYLE='''
QMainWindow,QWidget { background:#111b2a; color:#d6e2ef; font-family:"Segoe UI"; font-size:13px; }
QToolBar { background:#172335; padding:8px; border-bottom:1px solid #2a3b51; spacing:7px; }
QToolButton,QPushButton { background:#24364c; border:1px solid #354c67; padding:7px 12px; border-radius:5px; }
QToolButton:hover,QPushButton:hover { background:#304966; }
QToolButton:checked { background:#245c64; border-color:#43b8a9; }
QComboBox { background:#23344a; border:1px solid #354c67; padding:5px; border-radius:4px; }
QComboBox QAbstractItemView { background:#203248; selection-background-color:#30656e; }
QDockWidget { font-weight:600; }
QDockWidget::title { background:#1a2a3e; padding:9px; }
QGroupBox { border:1px solid #2a3b51; border-radius:5px; margin-top:15px; padding:14px 10px 8px; }
QGroupBox::title { subcontrol-origin:margin; left:10px; padding:0 4px; color:#8cb5d8; }
QLabel { background:transparent; }
QCheckBox { spacing:8px; padding:3px 0; }
QSlider::groove:horizontal { background:#293d55; height:4px; border-radius:2px; }
QSlider::handle:horizontal { background:#5ccabc; width:12px; margin:-4px 0; border-radius:6px; }
QListWidget { background:#0e1826; border:1px solid #2a3b51; padding:3px; font-size:11px; }
QStatusBar { background:#142134; color:#95afc9; }
QMenuBar,QMenu { background:#172335; }
QMenu::item:selected { background:#2a4c64; }
QScrollArea { border:0; }
'''


def configure_gl():
    fmt=QtGui.QSurfaceFormat();fmt.setVersion(3,3);fmt.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(0);fmt.setStencilBufferSize(0);fmt.setSwapInterval(1)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)


class Viewport(QtOpenGLWidgets.QOpenGLWidget):
    picked=QtCore.Signal(object)
    failure=QtCore.Signal(str)
    def __init__(self):
        super().__init__();self.camera=Camera();self.frame=None;self.opacity=[];self.selection=Selection()
        self.flashes=deque(maxlen=512);self.soft=True;self.grid=True;self.show_flashes=True
        self.renderer=None;self.ctx=None;self.press=None;self.last=None;self.dragged=False
        self.fbo=None;self.last_fbo=None;self.render_count=0;self.paint_ms=0.
        self.setMinimumSize(400,350);self.setMouseTracking(True)
        self.empty=Q.QLabel('CHIMIE LOCALE\n\nOuvrir un scénario pour explorer la simulation',self)
        self.empty.setAlignment(QtCore.Qt.AlignCenter)
        self.empty.setStyleSheet('color:#91abc6;background:transparent;font-size:18px;')

    def initializeGL(self):
        try:
            self.ctx=moderngl.create_context(require=330);self.renderer=Renderer(self.ctx)
            self.context().aboutToBeDestroyed.connect(self.cleanup)
        except Exception as exc:self.failure.emit(f'Initialisation OpenGL impossible : {exc}')

    def cleanup(self):
        if self.renderer:
            self.makeCurrent();self.renderer.release();self.renderer=None;self.doneCurrent()

    def paintGL(self):
        if not self.renderer:return
        started=time.perf_counter();ratio=self.devicePixelRatioF()
        size=(max(1,round(self.width()*ratio)),max(1,round(self.height()*ratio)))
        if self.last_fbo!=self.defaultFramebufferObject():
            self.fbo=self.ctx.detect_framebuffer(self.defaultFramebufferObject());self.last_fbo=self.defaultFramebufferObject()
        self.fbo.use()
        camera=Camera(self.camera.center.copy(),self.camera.scale*ratio)
        self.renderer.render(self.frame,camera,size,self.opacity,self.selection,
            self.flashes if self.show_flashes else (),time.monotonic(),self.soft,self.grid)
        self.paint_ms=(time.perf_counter()-started)*1000;self.render_count+=1

    def resizeEvent(self,event):
        super().resizeEvent(event);self.empty.setGeometry(self.rect())

    def fit(self):
        if self.frame:self.camera.fit(self.frame.positions,(self.width(),self.height()),self.frame.box)
        self.selection.follow=False;self.update()

    def wheelEvent(self,event):
        self.camera.zoom(event.angleDelta().y()/120,event.position().toTuple(),(self.width(),self.height()));self.update()

    def mousePressEvent(self,event):
        if event.button()==QtCore.Qt.LeftButton:
            self.press=np.array(event.position().toTuple());self.last=self.press.copy();self.dragged=False

    def mouseMoveEvent(self,event):
        if self.press is not None:
            pos=np.array(event.position().toTuple())
            if np.linalg.norm(pos-self.press)>3:self.dragged=True
            if self.dragged:
                self.camera.pan(pos-self.last);self.selection.follow=False;self.update()
            self.last=pos

    def mouseReleaseEvent(self,event):
        if self.press is not None and not self.dragged and self.frame is not None:
            pos=self.camera.screen(self.frame.positions,(self.width(),self.height()))
            d=np.linalg.norm(pos-np.array(event.position().toTuple()),axis=1)
            visible=np.asarray(self.opacity)[self.frame.species]>.02
            d[~visible]=np.inf;i=int(np.argmin(d)) if len(d) else None
            self.selection.anchor=i if i is not None and d[i]<12 else None
            self.picked.emit(self.selection.anchor);self.update()
        self.press=self.last=None

    def receive(self,f,events):
        initial=self.frame is None;self.frame=f;self.empty.hide()
        if len(self.opacity)!=len(f.labels):self.opacity=np.ones(len(f.labels))
        now=time.monotonic()
        for event in events:self.flashes.append((event,now))
        while self.flashes and now-self.flashes[0][1]>.22:self.flashes.popleft()
        if initial:self.fit()
        if self.selection.follow:
            ids=self.selection.indices(f)
            if len(ids):self.camera.center=f.positions[ids].mean(axis=0).astype(float)
        self.update()


class MainWindow(Q.QMainWindow):
    def __init__(self,config=None,output='outputs/visualizer'):
        super().__init__();self.setWindowTitle('Chimie locale · Atelier de visualisation')
        self.resize(1480,940);self.setStyleSheet(STYLE)
        self.output=Path(output);self.source=None;self.packet=None;self.config=None;self.layer_labels=()
        self.viewport=Viewport();self.setCentralWidget(self.viewport)
        self.viewport.failure.connect(self.show_error);self.viewport.picked.connect(lambda _:self.inspect())
        self.make_toolbar();self.make_sidebar();self.make_menu()
        self.last_ui=0.;self.last_fps=time.monotonic();self.last_render_count=0;self.fps=0.
        self.timer=QtCore.QTimer(self);self.timer.timeout.connect(self.tick);self.timer.start(16)
        for key,slot in [('Space',self.toggle_pause),('N',self.single_step),('F',self.fit),('F11',self.fullscreen),('Tab',self.presentation)]:
            QtGui.QShortcut(QtGui.QKeySequence(key),self,activated=slot)
        if config is not None:self.load_config(config)

    def action(self,text,slot,checkable=False):
        a=QtGui.QAction(text,self);a.setCheckable(checkable);a.triggered.connect(slot);return a

    def make_toolbar(self):
        self.toolbar=Q.QToolBar();self.toolbar.setMovable(False);self.addToolBar(self.toolbar)
        self.toolbar.addAction(self.action('Ouvrir…',self.open_file))
        self.play=self.action('▶ Reprendre',self.toggle_pause);self.toolbar.addAction(self.play)
        self.toolbar.addAction(self.action('Un pas',self.single_step))
        self.toolbar.addAction(self.action('Recommencer',self.restart))
        self.toolbar.addSeparator();self.toolbar.addAction(self.action('Vue globale',self.fit))
        self.toolbar.addAction(self.action('Plein écran',self.fullscreen))
        self.toolbar.addAction(self.action('Image PNG…',self.save_image))
        self.toolbar.addSeparator();self.toolbar.addWidget(Q.QLabel('  Vitesse cible  '))
        self.speed=Q.QComboBox()
        for label,value in [('0,01 u/s',.01),('0,05 u/s',.05),('0,2 u/s',.2),('0,5 u/s',.5),('1 u/s',1.),('2 u/s',2.),('5 u/s',5.),('Maximum',0.)]:self.speed.addItem(label,value)
        self.speed.setCurrentIndex(3);self.speed.currentIndexChanged.connect(self.change_speed);self.toolbar.addWidget(self.speed)
        self.time_label=Q.QLabel('   Aucun scénario chargé');self.toolbar.addWidget(self.time_label)

    def make_sidebar(self):
        self.dock=Q.QDockWidget('EXPLORER',self);self.dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.dock)
        scroll=Q.QScrollArea();scroll.setWidgetResizable(True);body=Q.QWidget();body.setMinimumWidth(300)
        layout=Q.QVBoxLayout(body);layout.setSpacing(12)
        self.title=Q.QLabel('Choisir un scénario');self.title.setWordWrap(True);self.title.setStyleSheet('font-size:19px;font-weight:600;color:#e7f2fc;')
        layout.addWidget(self.title);self.description=Q.QLabel('Navigation : molette pour zoomer, glisser pour déplacer.');self.description.setWordWrap(True);layout.addWidget(self.description)
        self.context=Q.QLabel('Les couleurs et filtres agissent uniquement sur la vue.');self.context.setWordWrap(True);layout.addWidget(self.context)
        layer_box=Q.QGroupBox('Espèces · opacité');self.layers=Q.QVBoxLayout(layer_box)
        layout.addWidget(layer_box)
        select_box=Q.QGroupBox('Sélection et suivi');s=Q.QVBoxLayout(select_box)
        self.inspector=Q.QLabel('Cliquer une particule pour l’inspecter.');self.inspector.setWordWrap(True);s.addWidget(self.inspector)
        for title,name,default in [('Assemblage lié','assembly',True),('Suivre la sélection','follow',False),('Atténuer le reste du bain','focus',False),('Éclairer les partenaires liés','partners',True)]:
            check=Q.QCheckBox(title);check.setChecked(default);check.toggled.connect(lambda value,key=name:self.select_option(key,value));s.addWidget(check)
            setattr(self,'check_'+name,check)
        clear=Q.QPushButton('Effacer la sélection');clear.clicked.connect(self.clear_selection);s.addWidget(clear)
        layout.addWidget(select_box)
        display=Q.QGroupBox('Affichage');d=Q.QVBoxLayout(display)
        for title,name,default in [('Particules douces / halo','soft',True),('Repères spatiaux','grid',True),('Flashes de transformation','show_flashes',True)]:
            check=Q.QCheckBox(title);check.setChecked(default);check.toggled.connect(lambda value,key=name:self.display_option(key,value));d.addWidget(check)
        self.legend=Q.QLabel('● Vert : liaison créée\n● Corail : liaison rompue\n● Ambre : état libre / lié modifié\nFlashes ≈ 0,22 s à réception');self.legend.setWordWrap(True);d.addWidget(self.legend)
        layout.addWidget(display)
        history=Q.QGroupBox('Transformations récentes');h=Q.QVBoxLayout(history)
        self.events=Q.QListWidget();self.events.setMaximumHeight(155);self.events.itemClicked.connect(self.event_clicked);h.addWidget(self.events)
        layout.addWidget(history);layout.addStretch();self.note=Q.QLabel('Interface · lot 1\nRelecture vidéo, export vidéo et courbes : à venir.');self.note.setWordWrap(True);layout.addWidget(self.note)
        scroll.setWidget(body);self.dock.setWidget(scroll)

    def make_menu(self):
        file=self.menuBar().addMenu('Fichier')
        a=self.action('Ouvrir un scénario…',self.open_file);a.setShortcut('Ctrl+O');file.addAction(a)
        file.addAction(self.action('Exporter une image…',self.save_image))
        file.addAction(self.action('Sauver un checkpoint',lambda:self.command('checkpoint')))
        file.addAction(self.action('Quitter',self.close))
        view=self.menuBar().addMenu('Vue');view.addAction(self.dock.toggleViewAction())
        view.addAction(self.action('Mode présentation',self.presentation));view.addAction(self.action('Plein écran',self.fullscreen))

    def open_file(self):
        path,_=Q.QFileDialog.getOpenFileName(self,'Ouvrir un scénario','demonstrators/configs','Scénarios JSON (*.json)')
        if path:
            try:
                from simulator.config import load
                self.load_config(load(Path(path)))
            except Exception as exc:self.show_error(str(exc))

    def load_config(self,config):
        if self.source and not self.source.close():self.statusBar().showMessage('Ancien processus arrêté de force : vérifier ses sorties.')
        self.config=config;self.packet=None;self.viewport.frame=None;self.viewport.opacity=[];self.viewport.flashes.clear();self.viewport.selection=Selection()
        for name in ('assembly','focus','partners'):setattr(self.viewport.selection,name,getattr(self,'check_'+name).isChecked())
        self.viewport.empty.setText('Initialisation du moteur…');self.viewport.empty.show()
        self.events.clear();self.layer_labels=();self.title.setText(config['name']);self.description.setText(config.get('description',''))
        self.context.setText(f"Graine {config['seed']} · {config['model']}\ndt = {config['engine']['dt']:g} · lois inchangées par la vue")
        self.source=ProcessSource(config,self.output);self.source.command('speed',self.speed.currentData())
        self.statusBar().showMessage('Initialisation du moteur… La simulation démarrera en pause.')
        self.clear_selection();self.play.setEnabled(True);self.play.setText('▶ Reprendre')

    def command(self,action,value=None):
        if self.source:self.source.command(action,value)

    def toggle_pause(self):
        if self.packet:self.command('pause',not self.packet['paused'])

    def single_step(self):self.command('step')
    def restart(self):
        if self.config:self.load_config(self.config)
    def change_speed(self):self.command('speed',self.speed.currentData())
    def fit(self):self.viewport.fit();self.check_follow.setChecked(False)
    def fullscreen(self):self.showNormal() if self.isFullScreen() else self.showFullScreen()
    def presentation(self):
        visible=self.dock.isVisible();self.dock.setVisible(not visible);self.toolbar.setVisible(not visible);self.menuBar().setVisible(not visible);self.statusBar().setVisible(not visible)

    def select_option(self,key,value):setattr(self.viewport.selection,key,value);self.viewport.update();self.inspect()
    def display_option(self,key,value):setattr(self.viewport,key,value);self.viewport.update()
    def clear_selection(self):
        self.viewport.selection.anchor=None;self.check_follow.setChecked(False);self.viewport.update();self.inspect()

    def build_layers(self,f):
        while self.layers.count():
            item=self.layers.takeAt(0)
            if item.widget():item.widget().deleteLater()
        for i,label in enumerate(f.labels):
            container=Q.QWidget();v=Q.QVBoxLayout(container);v.setContentsMargins(0,0,0,3);v.setSpacing(1)
            row=Q.QHBoxLayout();dot=Q.QLabel('● '+label);color=QtGui.QColor.fromRgbF(*map(float,f.palette[i]))
            dot.setStyleSheet(f'color:{color.name()};');row.addWidget(dot);value=Q.QLabel('100 %');row.addWidget(value);v.addLayout(row)
            slider=Q.QSlider(QtCore.Qt.Horizontal);slider.setRange(0,100);slider.setValue(100)
            slider.valueChanged.connect(lambda x,index=i,text=value:self.set_opacity(index,x,text));v.addWidget(slider);self.layers.addWidget(container)
        self.layer_labels=f.labels

    def set_opacity(self,index,value,label):
        if index>=len(self.viewport.opacity):return
        self.viewport.opacity[index]=value/100;label.setText(f'{value} %');self.viewport.update()

    def inspect(self):
        f=self.viewport.frame;s=self.viewport.selection
        if f is None or s.anchor is None:
            self.inspector.setText('Cliquer une particule pour l’inspecter.');return
        ids=s.indices(f);partners=s.linked_partners(f,ids)
        links={group:int(np.count_nonzero(np.any(pairs==s.anchor,axis=1))) for group,pairs in f.bonds.items()}
        self.inspector.setText(f"Particule #{s.anchor} · {f.labels[f.species[s.anchor]]}\n"
            f"Sélection : {len(ids)} billes · {len(partners)} partenaires liés\n"+
            ' · '.join(f'{k} : {v}' for k,v in links.items()))

    def event_clicked(self,item):
        event=item.data(QtCore.Qt.UserRole)
        self.viewport.camera.center=np.mean(event.points,axis=0);self.viewport.selection.anchor=event.ids[0]
        self.check_follow.setChecked(False);self.inspect();self.viewport.update()

    def tick(self):
        if self.source:
            for packet in self.source.poll():
                if 'error' in packet:self.show_error(packet['error']);continue
                self.packet=packet;f=packet['frame'];self.viewport.receive(f,packet['events'])
                if self.layer_labels!=f.labels:self.build_layers(f)
                self.play.setEnabled(not f.done)
                self.play.setText('Terminée' if f.done else ('▶ Reprendre' if packet['paused'] else 'Ⅱ Pause'))
                self.time_label.setText(f'   t = {f.time:.3f} / {packet["config"]["duration"]:g}   ·   {len(f.positions):,} billes')
                for event in packet['events'][-100:]:
                    text={'bond_created':'+ liaison','bond_broken':'− liaison','state_changed':'↻ état'}[event.kind]
                    item=Q.QListWidgetItem(f't {event.time:.3f}  {text}  {event.group}  '+','.join(map(str,event.ids)))
                    item.setData(QtCore.Qt.UserRole,event);self.events.insertItem(0,item)
                while self.events.count()>100:self.events.takeItem(self.events.count()-1)
        now=time.monotonic()
        if now-self.last_fps>=1:
            self.fps=(self.viewport.render_count-self.last_render_count)/(now-self.last_fps)
            self.last_render_count=self.viewport.render_count;self.last_fps=now
        if self.packet and now-self.last_ui>.25:
            p=self.packet;f=p['frame'];state='Terminée' if f.done else ('Pause' if p['paused'] else 'En cours')
            self.statusBar().showMessage(f"{state}   ·   {p['rate']*p['config']['engine']['dt']:.3g} u/s   ·   {p['rate']:,.0f} pas/s   ·   {self.fps:.0f} images/s   ·   "
                f"rendu {self.viewport.paint_ms:.1f} ms   ·   événements non transmis : {p['dropped']}")
            self.inspect();self.check_follow.setChecked(self.viewport.selection.follow);self.last_ui=now
        self.viewport.update()

    def save_image(self,path=None):
        if not isinstance(path,(str,Path)):
            path,_=Q.QFileDialog.getSaveFileName(self,'Exporter la vue seule',f'capture_{datetime.now():%Y%m%d_%H%M%S}.png','PNG (*.png)')
        if not path:return
        path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
        if not self.viewport.grabFramebuffer().save(str(path)):self.show_error('Export PNG impossible.');return
        f=self.viewport.frame
        metadata=dict(simulated_time=None if f is None else f.time,step=None if f is None else f.step,
            camera=dict(center=self.viewport.camera.center.tolist(),scale=self.viewport.camera.scale),
            opacity=list(map(float,self.viewport.opacity)),soft_style=self.viewport.soft,
            selection=self.viewport.selection.anchor,config=self.config,
            renderer=self.viewport.ctx.info.get('GL_RENDERER') if self.viewport.ctx else None)
        path.with_suffix('.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        self.statusBar().showMessage(f'Vue exportée : {path}')

    def show_error(self,message):
        self.statusBar().showMessage('Erreur — '+message.splitlines()[-1]);Q.QMessageBox.critical(self,'Visualisation',message)

    def closeEvent(self,event):
        self.timer.stop()
        if self.source:self.source.close();self.source=None
        self.viewport.cleanup();event.accept()


def main():
    import argparse
    p=argparse.ArgumentParser(description='Atelier de visualisation Qt/OpenGL, moteur indépendant')
    p.add_argument('--config',type=Path);p.add_argument('--output',type=Path,default=Path('outputs/visualizer'))
    p.add_argument('--screenshot',type=Path);p.add_argument('--quit-after',type=float)
    args=p.parse_args();configure_gl();app=Q.QApplication.instance() or Q.QApplication([])
    config=None
    if args.config:
        from simulator.config import load
        config=load(args.config)
    window=MainWindow(config,args.output);window.showMaximized()
    if args.screenshot:
        def capture():
            if window.viewport.renderer and (window.packet or not config):
                window.grab().save(str(args.screenshot.with_name(args.screenshot.stem+'_interface.png')))
                window.save_image(args.screenshot)
            else:QtCore.QTimer.singleShot(100,capture)
        args.screenshot.parent.mkdir(parents=True,exist_ok=True);QtCore.QTimer.singleShot(500,capture)
    if args.quit_after:QtCore.QTimer.singleShot(round(args.quit_after*1000),window.close)
    return app.exec()
