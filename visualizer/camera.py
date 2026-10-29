"""World/screen mapping independent of Qt and OpenGL."""
from dataclasses import dataclass,field
import numpy as np


@dataclass
class Camera:
    center: np.ndarray=field(default_factory=lambda:np.zeros(2,dtype=float))
    scale: float=60.

    def screen(self,world,size):
        return (np.asarray(world)-self.center)*[self.scale,-self.scale]+np.asarray(size)/2

    def world(self,screen,size):
        return (np.asarray(screen)-np.asarray(size)/2)/[self.scale,-self.scale]+self.center

    def zoom(self,steps,anchor,size):
        before=self.world(anchor,size)
        self.scale=float(np.clip(self.scale*1.18**steps,1e-5,1e7))
        self.center+=before-self.world(anchor,size)

    def pan(self,delta):
        self.center-=np.asarray(delta)/[self.scale,-self.scale]

    def fit(self,positions,size,box=None):
        if box is not None:lo,hi=np.zeros(2),np.asarray(box,dtype=float)
        elif len(positions):lo,hi=np.min(positions,axis=0),np.max(positions,axis=0)
        else:lo,hi=np.array([-5.,-5.]),np.array([5.,5.])
        self.center=(lo+hi)/2
        self.scale=float(np.min(np.maximum(np.asarray(size),1)/np.maximum((hi-lo)*1.15,1.)))
