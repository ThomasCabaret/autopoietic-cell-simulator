"""Immutable local checkpoint imports; no archived code execution or migration."""
from datetime import datetime,timezone
from io import BytesIO
from pathlib import Path
import hashlib,json,os,time,uuid
import numpy as np


def snapshot_checkpoint(path,parent,expected_config=None,inspection=False):
    from simulator.checkpoint import source_hashes
    path=Path(path).resolve()
    for attempt in range(7):
        try:payload=path.read_bytes();break
        except PermissionError:
            if os.name!='nt' or attempt==6:raise
            time.sleep(.01*2**attempt)
    with np.load(BytesIO(payload),allow_pickle=False) as data:
        meta=json.loads(str(data['metadata']))
        if meta.get('checkpoint_version')!=1:raise ValueError('Version de checkpoint non prise en charge.')
        if inspection:
            if (expected_config is None or expected_config['model']!='lipid_synthesis'
                or expected_config['chemistry']['tool_count']!=0):
                raise ValueError('Inspection historique réservée aux résultats de membrane du catalogue local.')
        elif meta['source_sha256']!=source_hashes():
            raise ValueError('Version du moteur différente : ouvrir ce résultat avec les sources archivées de son expérience.')
        if expected_config is not None and meta['config']!=expected_config:raise ValueError('Le checkpoint ne correspond pas à la tâche sélectionnée.')
        if not np.isfinite(data['positions']).all():raise ValueError('Positions du checkpoint invalides.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'_'+uuid.uuid4().hex[:8]
    folder=Path(parent).resolve()/'imports'/stamp;folder.mkdir(parents=True)
    target=folder/'source.npz';target.write_bytes(payload)
    provenance=dict(source=str(path),snapshot=str(target),sha256=hashlib.sha256(payload).hexdigest(),
        step=meta['step'],time=meta['step']*meta['config']['engine']['dt'],config=meta['config'],
        inspection=inspection,
        scope='Copied local checkpoint, paused physical continuation with the principal observer. '
              'Auxiliary campaign audit protocols are not automatically extended by this visual session. No past trajectory replay.')
    if inspection:
        provenance['scope']='Read-only geometry and lipid links. No archived code execution or simulation continuation.'
    (folder/'import.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return provenance


class MembraneInspectionSource:
    """Publish a frozen display frame from a curated membrane checkpoint."""

    def __init__(self, imported):
        from types import SimpleNamespace
        from simulator.linked_lipids import LinkedLipids
        from .scene import frame

        path=Path(imported['snapshot'])
        with np.load(path,allow_pickle=False) as data:
            meta=json.loads(str(data['metadata']))
            pos=data['positions'].copy()
        cfg=imported['config'];chemistry=cfg['chemistry'];count=chemistry['food_units']
        if pos.shape!=(2*count,2) or not np.isfinite(pos).all():
            raise ValueError('Géométrie historique de membrane invalide.')
        lipids=LinkedLipids()
        lipids.restore(meta['chemistry']['lipids'])
        if any(not (0<=a<count<=b<2*count) for a,b in lipids.rungs.items()):
            raise ValueError('Identifiants historiques de lipides invalides.')
        scene=SimpleNamespace(pos=pos,lipids=lipids,host=None,prefix=0,
            ligand_types=np.repeat([0,1],count),box=chemistry['box'],config=chemistry,bonds=lipids.bonds)
        sim=SimpleNamespace(chemistry=scene,time=imported['time'],step_index=imported['step'],done=True)
        self.packet=dict(frame=frame(sim),events=[],dropped=0,paused=True,rate=0.,
            path=str(path.parent),config=cfg,observations=dict(time=imported['time'],
            rows=[('Lipides',len(lipids.rungs)),('Liaisons latérales',len(lipids.links))]))

    def command(self, action, value=None):
        pass

    def poll(self):
        if self.packet is None:return []
        packet,self.packet=self.packet,None
        return [packet]

    def close(self):
        return True
