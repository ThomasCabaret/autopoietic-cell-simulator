"""Native Qt/OpenGL interaction and image-export check, not a biology demonstrator."""
import json
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
from PySide6 import QtWidgets,QtCore,QtGui,QtTest
from visualizer.app import MainWindow,configure_gl
from visualizer.scene import Transition
from simulator.config import load
from simulator.engine import Simulation


def main():
    out=ROOT/'outputs/visualizer_qa';out.mkdir(parents=True,exist_ok=True)
    configure_gl();app=QtWidgets.QApplication([]);errors=[]
    class Window(MainWindow):
        def show_error(self,message):errors.append(message)
    cfg=load(ROOT/'demonstrators/configs/construction.json');cfg['duration']=.1;cfg['expected']={}
    window=Window(cfg,out/'interaction_runs');window.showMaximized()
    def wait(predicate,seconds=40):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            app.processEvents();time.sleep(.005)
            if errors:raise AssertionError(errors)
            if predicate():return
        raise AssertionError('Qt interaction check timed out')
    try:
        wait(lambda:window.packet is not None and window.viewport.renderer is not None)
        view=window.viewport;size=(view.width(),view.height());anchor=QtCore.QPointF(300,300)
        world=view.camera.world(anchor.toTuple(),size).copy()
        wheel=QtGui.QWheelEvent(anchor,anchor,QtCore.QPoint(),QtCore.QPoint(0,120),
            QtCore.Qt.NoButton,QtCore.Qt.NoModifier,QtCore.Qt.ScrollUpdate,False)
        app.sendEvent(view,wheel);np.testing.assert_allclose(view.camera.world(anchor.toTuple(),size),world)
        before=view.camera.center.copy();QtTest.QTest.mousePress(view,QtCore.Qt.LeftButton,pos=QtCore.QPoint(300,300))
        QtTest.QTest.mouseMove(view,QtCore.QPoint(350,320),10);QtTest.QTest.mouseRelease(view,QtCore.Qt.LeftButton,pos=QtCore.QPoint(350,320))
        assert not np.array_equal(before,view.camera.center)
        window.fit();app.processEvents();p=view.camera.screen(view.frame.positions[0],size)
        QtTest.QTest.mouseClick(view,QtCore.Qt.LeftButton,pos=QtCore.QPoint(*map(int,np.rint(p))))
        assert view.selection.anchor==0
        window.check_follow.setChecked(True);window.check_focus.setChecked(True)
        sliders=window.dock.findChildren(QtWidgets.QSlider);sliders[0].setValue(25)
        assert view.opacity[0]==.25 and view.selection.follow and view.selection.focus
        view.camera.zoom(1.2,p,size)
        # Explicit display-only fixture for the flash path; never called a physical event.
        points=tuple(tuple(map(float,q)) for q in view.frame.positions[:2])
        view.receive(view.frame,[Transition('bond_created','display_test',(0,1),points,view.frame.time)])
        app.processEvents();window.save_image(out/'inspection.png');window.grab().save(str(out/'inspection_interface.png'))
        assert (out/'inspection.png').stat().st_size>10000
        window.fullscreen();app.processEvents();assert window.isFullScreen()
        window.fullscreen();app.processEvents();assert not window.isFullScreen()
        window.single_step();wait(lambda:window.packet['frame'].step==1)
        assert window.packet['paused']
        window.speed.setCurrentIndex(7);window.toggle_pause();wait(lambda:window.packet['frame'].done)
        ref=Simulation(cfg);ref.advance(ref.target_step)
        np.testing.assert_array_equal(window.packet['frame'].positions,ref.chemistry.pos.astype('f4'))
        report=dict(native_qt=True,opengl=view.ctx.info['GL_RENDERER'],pointer_zoom=True,mouse_pan=True,
            selection=True,tracking=True,opacity=True,fullscreen=True,single_step=True,
            exact_final_positions=True,scene_only_png=True,errors=errors,
            caveat='Display-only flash fixture, not a chemistry result; real reaction event invariance covered by unit tests.')
        (out/'interaction_report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report))
    finally:window.close();app.processEvents()


if __name__=='__main__':main()
