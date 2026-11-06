"""Immutable local checkpoint imports; no archived code execution or migration."""
from datetime import datetime,timezone
from io import BytesIO
from pathlib import Path
import hashlib,json,os,time,uuid
import numpy as np


def snapshot_checkpoint(path,parent,expected_config=None):
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
        if meta['source_sha256']!=source_hashes():
            raise ValueError('Version du moteur différente : ouvrir ce résultat avec les sources archivées de son expérience.')
        if expected_config is not None and meta['config']!=expected_config:raise ValueError('Le checkpoint ne correspond pas à la tâche sélectionnée.')
        if not np.isfinite(data['positions']).all():raise ValueError('Positions du checkpoint invalides.')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'_'+uuid.uuid4().hex[:8]
    folder=Path(parent).resolve()/'imports'/stamp;folder.mkdir(parents=True)
    target=folder/'source.npz';target.write_bytes(payload)
    provenance=dict(source=str(path),snapshot=str(target),sha256=hashlib.sha256(payload).hexdigest(),
        step=meta['step'],time=meta['step']*meta['config']['engine']['dt'],config=meta['config'],
        scope='Copied local checkpoint, paused physical continuation with the principal observer. '
              'Auxiliary campaign audit protocols are not automatically extended by this visual session. No past trajectory replay.')
    (folder/'import.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return provenance
