"""Native Qt/OpenGL checkpoint actions, immutable restart and actual local CR1 view."""
import json,sys,time,hashlib
from pathlib import Path
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from PySide6 import QtWidgets
from visualizer.app import MainWindow,configure_gl
from visualizer.local_runs import available
from simulator.engine import Simulation
from simulator.runner import make_observer
from simulator import checkpoint


def main():
    from datetime import datetime
    out=ROOT/'outputs/checkpoint_gui_qa'/datetime.now().strftime('%Y%m%d_%H%M%S%f');out.mkdir(parents=True)
    cfg=dict(schema_version=1,model='copy',seed=2,duration=.1,chemistry=dict(sequence='001',free_units=3),engine=dict(dt=.005,sample_every=5))
    ref=Simulation(cfg);obs=make_observer(ref.config,False);ref.listeners.append(obs);ref.advance(7)
    initial=ref.chemistry.pos.copy();original=out/'original.npz';checkpoint.save(original,ref,obs)
    configure_gl();app=QtWidgets.QApplication([]);errors=[]
    class Window(MainWindow):
        def show_error(self,message):errors.append(message)
    window=Window(output=out/'sessions');window.showMaximized()
    def wait(predicate):
        end=time.monotonic()+45.
        while time.monotonic()<end:
            app.processEvents();time.sleep(.005)
            if errors:raise AssertionError(errors)
            if predicate():return
        raise AssertionError('Checkpoint UI timeout')
    try:
        with patch.object(QtWidgets.QFileDialog,'getOpenFileName',return_value=(str(original),'')):
            window.open_checkpoint_action.trigger()
        wait(lambda:window.packet is not None);assert window.packet['paused'] and window.packet['frame'].step==7
        np.testing.assert_array_equal(window.packet['frame'].positions,initial.astype('f4'))
        imported=window.checkpoint_import;assert (Path(window.packet['path'])/'checkpoint_import.json').exists()
        ref.advance(ref.target_step);checkpoint.save(original,ref,obs);sha=hashlib.sha256(original.read_bytes()).hexdigest()
        window.restart();wait(lambda:window.packet is not None);assert window.packet['frame'].step==7
        assert window.checkpoint_import['snapshot']==imported['snapshot']
        window.toggle_pause();wait(lambda:window.packet['frame'].done)
        np.testing.assert_array_equal(window.packet['frame'].positions,ref.chemistry.pos.astype('f4'))
        assert hashlib.sha256(original.read_bytes()).hexdigest()==sha
        local=[];window.refresh_local_runs()
        for row in available():
            if row['status']!='complete':continue
            window.local_actions[row['label']].trigger();wait(lambda:window.packet is not None)
            assert window.packet['paused'];assert window.packet['frame'].done
            assert len(window.packet['frame'].positions)==104
            window.save_image(out/(row['label']+'.png'));window.grab().save(str(out/(row['label']+'_interface.png')))
            local.append(dict(label=row['label'],step=window.packet['frame'].step,beads=104))
        result=dict(paused_saved_step=True,restart_from_immutable_import=True,continuation_exact=True,
            original_preserved=True,native_qt_opengl=True,local_results=local,errors=errors,
            scope='Current checkpoint view and exact physical continuation, no historical trajectory replay or new chemical success claim.')
        (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(output=str(out),**result)))
    finally:window.close();app.processEvents()


if __name__=='__main__':main()
