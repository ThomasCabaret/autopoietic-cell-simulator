"""Open all curated presets through real Qt actions, preserving paused initial states."""
import json
from pathlib import Path
import sys
import time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PySide6 import QtWidgets,QtCore
from visualizer.app import MainWindow,configure_gl


def main():
    out=ROOT/'outputs/demo_qa';out.mkdir(parents=True,exist_ok=True)
    configure_gl();app=QtWidgets.QApplication([]);errors=[]
    class Window(MainWindow):
        def show_error(self,message):errors.append(message)
    window=Window(output=out/'sessions');window.showMaximized();rows=[]
    def wait(predicate,seconds=45):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            app.processEvents();time.sleep(.005)
            if errors:raise AssertionError(errors)
            if predicate():return
        raise AssertionError('Demo menu timed out')
    try:
        window.current_demo_action.trigger();wait(lambda:window.packet is not None)
        assert window.active_demo['variant']['id']==window.catalog.data['recommended']
        for key in window.catalog.variants:
            window.demo_actions[key].trigger()
            wait(lambda:window.packet is not None)
            packet=window.packet;f=packet['frame'];variant=window.active_demo['variant']
            assert packet['paused'] and f.step==0 and len(f.positions)==variant['beads']
            assert packet['config']['seed']==variant['seed']
            assert window.tabs.currentIndex()==0 and window.speed.currentData()==0.
            assert (Path(packet['path'])/'demo.json').exists()
            assert packet['observations']['time']==0.
            rows.append(dict(id=key,beads=len(f.positions),seed=packet['config']['seed'],paused_initial_state=True))
            if key in ('integrated_s2','integrated_s2_langevin','current_cell_s2','current_free_s2','current_probes_s2'):
                initial=f.positions.copy();window.single_step();wait(lambda:window.packet['frame'].step==1)
                assert window.packet['paused'];window.toggle_pause()
                wait(lambda:window.packet['frame'].time>=.1)
                window.command('pause',True);wait(lambda:window.packet['paused'])
                assert window.packet['observations']['rows']
                if key.startswith('current_'):
                    from simulator.engine import Simulation
                    headless=Simulation(window.packet['config']);headless.advance(window.packet['frame'].step)
                    np.testing.assert_array_equal(headless.chemistry.pos.astype(np.float32),window.packet['frame'].positions)
                window.save_image(out/f'{key}.png');window.grab().save(str(out/f'{key}_interface.png'))
                window.restart();wait(lambda:window.packet is not None)
                assert window.active_demo['variant']['id']==key and window.packet['paused']
                np.testing.assert_array_equal(window.packet['frame'].positions,initial)
        report=dict(menu_actions=rows,integrated_step_play_pause=True,restart_exact_initial_state=True,
            native_qt_opengl=True,current_frames_equal_headless=True,errors=errors,
            scope='Initial-state and short playback checks only. No full-horizon success or new biological evidence claimed.')
        (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
    finally:window.close();app.processEvents()


if __name__=='__main__':main()
