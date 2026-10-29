"""Batched OpenGL 3.3 renderer. No Qt, engine, clocks or random state.

All time-dependent effects take an explicit presentation time, so the same
renderer can later target an offline video framebuffer at fixed output times.
"""
from pathlib import Path
import numpy as np
import moderngl
from .scene import style_arrays

SHADERS=Path(__file__).with_name('shaders')


class Batch:
    def __init__(self,ctx,program,quad,fmt,attributes,stride):
        self.ctx=ctx;self.program=program;self.quad=quad;self.fmt=fmt
        self.attributes=attributes;self.stride=stride;self.capacity=0;self.buffer=None;self.vao=None

    def draw(self,data):
        if not len(data):return
        data=np.ascontiguousarray(data,dtype='f4')
        if len(data)>self.capacity:
            if self.vao:self.vao.release();self.buffer.release()
            self.capacity=2**int(np.ceil(np.log2(max(16,len(data)))))
            self.buffer=self.ctx.buffer(reserve=self.capacity*self.stride*4,dynamic=True)
            self.vao=self.ctx.vertex_array(self.program,[(self.quad,'2f','corner'),
                (self.buffer,self.fmt,*self.attributes)])
        self.buffer.write(data.tobytes());self.vao.render(moderngl.TRIANGLE_STRIP,vertices=4,instances=len(data))

    def release(self):
        if self.vao:self.vao.release();self.buffer.release()


class Renderer:
    def __init__(self,ctx):
        self.ctx=ctx
        self.quad=ctx.buffer(np.array([[-1,-1],[1,-1],[-1,1],[1,1]],dtype='f4').tobytes())
        self.particle=ctx.program(vertex_shader=(SHADERS/'particle.vert').read_text(),fragment_shader=(SHADERS/'particle.frag').read_text())
        self.bond=ctx.program(vertex_shader=(SHADERS/'bond.vert').read_text(),fragment_shader=(SHADERS/'bond.frag').read_text())
        self.background=ctx.program(vertex_shader=(SHADERS/'background.vert').read_text(),fragment_shader=(SHADERS/'background.frag').read_text())
        self.background_vao=ctx.vertex_array(self.background,[(self.quad,'2f','corner')])
        self.particles=Batch(ctx,self.particle,self.quad,'2f 4f 1f /i',('position','color','emphasis'),7)
        self.bonds=Batch(ctx,self.bond,self.quad,'2f 2f 4f 1f /i',('start','end','color','width'),9)
        self.last_draw_calls=0

    def render(self,f,camera,size,opacity,selection,flashes=(),presentation_time=0.,soft=True,grid=True):
        ctx=self.ctx;ctx.viewport=(0,0,*map(int,size));ctx.disable(moderngl.DEPTH_TEST)
        ctx.enable(moderngl.BLEND);ctx.blend_func=(moderngl.SRC_ALPHA,moderngl.ONE_MINUS_SRC_ALPHA)
        self.last_draw_calls=1
        for program in (self.particle,self.bond,self.background):
            program['viewport'].value=tuple(map(float,size));program['center'].value=tuple(camera.center);program['scale'].value=camera.scale
        self.background['grid_enabled'].value=grid
        self.background_vao.render(moderngl.TRIANGLE_STRIP,vertices=4)
        if f is None:return
        rgba,emphasis,chosen,partners=style_arrays(f,opacity,selection)
        lines=[]
        for group,pairs in f.bonds.items():
            if not len(pairs):continue
            color={'scaffold':(.38,.59,.7),'backbone':(.56,.69,.79),'pairing':(.83,.64,.9)}.get(group,(.65,.7,.8))
            colors=np.tile([*color,.65],(len(pairs),1));colors[:,3]*=np.minimum(rgba[pairs[:,0],3],rgba[pairs[:,1],3])
            points=f.bond_positions[group] if f.bond_positions is not None else f.positions[pairs]
            lines.append(np.column_stack((points[:,0],points[:,1],colors,np.full(len(pairs),1.5 if group=='backbone' else .85))))
        if f.box is not None:
            x,y=f.box;corners=np.array([[0,0],[x,0],[x,y],[0,y]])
            lines.append(np.column_stack((corners,np.roll(corners,-1,axis=0),np.tile([.28,.4,.52,.35],(4,1)),np.ones(4))))
        if lines:self.bonds.draw(np.concatenate(lines));self.last_draw_calls+=1
        self.particle['soft_style'].value=soft
        self.particle['radius'].value=.14
        self.particles.draw(np.column_stack((f.positions,rgba,emphasis)));self.last_draw_calls+=1
        particle_flashes=[];bond_flashes=[]
        for event,arrived in flashes:
            age=presentation_time-arrived
            if not 0<=age<.22:continue
            alpha=(1-age/.22)**.6
            color={'bond_created':(.3,1.,.66),'bond_broken':(1.,.33,.38),'state_changed':(1.,.8,.3)}[event.kind]
            visible=max((rgba[i,3] for i in event.ids if i<len(rgba)),default=0.)
            if len(event.points)==2:bond_flashes.append([*event.points[0],*event.points[1],*color,alpha*visible,3.5])
            for p in event.points:particle_flashes.append([*p,*color,.75*alpha*visible,.5])
        if bond_flashes:self.bonds.draw(bond_flashes);self.last_draw_calls+=1
        if particle_flashes:
            self.particle['radius'].value=.25;self.particles.draw(particle_flashes);self.last_draw_calls+=1

    def release(self):
        self.particles.release();self.bonds.release();self.background_vao.release()
        self.particle.release();self.bond.release();self.background.release();self.quad.release()
