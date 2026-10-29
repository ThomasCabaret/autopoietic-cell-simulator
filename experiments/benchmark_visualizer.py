"""GPU rendering benchmark only: synthetic scenes, no biological simulation claim."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import moderngl
from visualizer.renderer import Renderer
from visualizer.camera import Camera
from visualizer.scene import Frame,Selection


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'outputs/visualizer_qa')
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    ctx=moderngl.create_standalone_context(require=330);target=ctx.simple_framebuffer((1920,1080));target.use()
    renderer=Renderer(ctx);rows=[]
    for n in (2000,10000,100000):
        rng=np.random.default_rng(0);pos=rng.uniform(0,100,(n,2)).astype('f4')
        pairs=np.column_stack((np.arange(n-1),np.arange(1,n)))
        # Short synthetic bonds; do not fill the entire image with long diagonals.
        pos=np.column_stack((np.arange(n)%500,np.arange(n)//500)).astype('f4')*.2
        f=Frame(pos,np.arange(n,dtype=np.int16)%3,('A','B','C'),np.array([[.3,.9,.7],[.8,.5,.9],[.9,.7,.4]],dtype='f4'),
            dict(backbone=pairs),0.,0,False,revision=1)
        camera=Camera();camera.fit(pos,(1920,1080));selection=Selection()
        for _ in range(5):renderer.render(f,camera,(1920,1080),[1,1,1],selection);ctx.finish()
        elapsed=[]
        for _ in range(10):
            start=time.perf_counter();renderer.render(f,camera,(1920,1080),[1,1,1],selection);ctx.finish()
            elapsed.append(time.perf_counter()-start)
        rows.append(dict(particles=n,bonds=n-1,median_ms=1000*statistics.median(elapsed),
            frames_per_second=1/statistics.median(elapsed),draw_calls=renderer.last_draw_calls))
    report=dict(renderer=ctx.info['GL_RENDERER'],vendor=ctx.info['GL_VENDOR'],resolution=[1920,1080],
        rows=rows,scope='Static synthetic scenes, instanced bonds and particles, buffer uploads and GPU finish included. '
            'No Qt event handling, simulation, IPC, tracking or event capture costs; not a complete-cell benchmark.',
        sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in list((ROOT/'visualizer').glob('*.py'))+list((ROOT/'visualizer/shaders').glob('*'))})
    out=args.output/('render_benchmark_'+str(time.time_ns())+'.json');out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report));renderer.release();target.release();ctx.release()


if __name__=='__main__':main()
