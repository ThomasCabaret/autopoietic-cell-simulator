"""Versioned local demo catalog. Presets are inputs, never prerecorded outcomes."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def simulator_hashes():
    return {'simulator/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted((ROOT/'simulator').glob('*.py'))}


def dynamics_hash(cfg):
    from simulator.config import resolve
    resolved=resolve(cfg)
    payload={k:resolved[k] for k in ('model','seed','duration','engine','chemistry')}
    if 'mechanics' in resolved:payload['mechanics']=resolved['mechanics']
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


class DemoCatalog:
    def __init__(self,path=None):
        self.path=Path(path) if path else ROOT/'demonstrators/catalog.json'
        self.data=json.loads(self.path.read_text(encoding='utf-8'))
        if self.data['version']!=1:raise ValueError('Version de catalogue non prise en charge')
        self.demos={d['id']:d for d in self.data['demos']}
        self.variants={v['id']:v for v in self.data['variants']}
        if len(self.demos)!=len(self.data['demos']) or len(self.variants)!=len(self.data['variants']):
            raise ValueError('Identifiants de démo dupliqués')

    def get(self,key):
        from simulator.config import load
        if simulator_hashes()!=self.data['simulator_sha256']:
            raise ValueError('Le code du moteur a changé : réexaminer les démos puis régénérer le catalogue')
        variant=self.variants[key];path=(ROOT/variant['config']).resolve()
        if not path.is_relative_to(ROOT):raise ValueError('Scénario hors catalogue local')
        cfg=load(path)
        if dynamics_hash(cfg)!=variant['dynamics_sha256']:raise ValueError('Le scénario de démo a changé : régénérer et vérifier le catalogue')
        if cfg['seed']!=variant['seed']:raise ValueError('Graine incohérente')
        info=dict(self.demos[variant['demo']])
        presentation=variant.get('presentation',{})
        if set(presentation)-{'conditions','observe','evidence'}:
            raise ValueError('Champs de présentation de variante inconnus')
        info.update(presentation)
        return dict(variant),info,cfg
