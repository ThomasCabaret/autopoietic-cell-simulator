"""Small versioned JSON format; chemistry is configured by its registered hook."""
import copy
import json
import math
from pathlib import Path

COPY_DEFAULTS = dict(sequence="001011", alphabet="01", free_units=30, function_units=0,
    activation=True, release="cycle", period=60., release_time=10., template=True,
    backbone_angle=5., box=[10.,7.], monomer_only_capture=False, product_cooperativity=False,
    functional_cosines={}, seed_family=0, caps_symbol=-1, initial_min_separation=.60,
    local_off_rate=.2, ligation_rate=12., ligation=True, temperature=.6,
    functional_bend_cosines={},functional_bend_strength=100.,food_pairs=0,
    food_ligand_energy=2.,food_ligand_width=.6,food_binding_radius=.25,
    food_binding_rate=20.,food_unbinding_rate=.1,food_reaction_radius=.25,food_reaction_rate=.2,
    food_activation=False,dual_faces=False)
MEMBRANE_DEFAULTS = dict(units=16, initial="straight", short_length=.75, bonding=True,
    end_attraction=4., cooperative_rows=False, oriented_ports=False, port_epsilon=.6,
    temperature=.06, face_docking=False, dock_energy=4., dock_width=.25,
    dock_capture=.25, dock_rate=25., bond_off_rate=.01, break_extension=.35)


def resolve(raw):
    raw = copy.deepcopy(raw)
    allowed = {"schema_version","name","description","model","seed","duration","chemistry","engine","expected","branch"}
    if set(raw)-allowed:
        raise ValueError("Unknown scenario keys: " + str(sorted(set(raw)-allowed)))
    if raw.get("schema_version") != 1:
        raise ValueError("Expected schema_version 1")
    model = raw.get("model")
    from .registry import MODELS
    if model not in MODELS:
        raise ValueError("Unknown chemical hook: " + str(model))
    defaults = copy.deepcopy(MODELS[model][1])
    chemistry = raw.get("chemistry", {})
    if set(chemistry) - set(defaults) - {"box", "fragment_size"}:
        raise ValueError("Unknown chemistry keys: " + str(sorted(set(chemistry)-set(defaults)-{"box","fragment_size"})))
    defaults.update(chemistry)
    engine = {"dt": .005 if model=="copy" else .002, "spatial":"tree", "skin":.25,
              "sample_every":100 if model=="copy" else 200}
    if set(raw.get("engine",{}))-set(engine):
        raise ValueError("Unknown engine setting")
    engine.update(raw.get("engine",{}))
    raw.update(chemistry=defaults,engine=engine)
    raw.setdefault("seed",0)
    raw.setdefault("duration",180. if model=="copy" else 100.)
    raw.setdefault("name",model)
    for key,val in [("dt",engine["dt"]),("duration",raw["duration"])]:
        if not isinstance(val,(int,float)) or not math.isfinite(val) or val<=0:
            raise ValueError(key+" must be finite and positive")
    if abs(raw["duration"]/engine["dt"]-round(raw["duration"]/engine["dt"]))>1e-7:
        raise ValueError("duration must be an integer multiple of dt")
    if not isinstance(raw['seed'],int) or raw['seed'] < 0:
        raise ValueError("seed must be a nonnegative integer")
    if not isinstance(engine['sample_every'],int) or engine['sample_every']<1:
        raise ValueError("sample_every must be a positive integer")
    if engine['spatial'] not in ('tree','brute') or not isinstance(engine['skin'],(int,float)) or not math.isfinite(engine['skin']) or engine['skin']<0:
        raise ValueError('invalid spatial backend or neighbor skin')
    if any(isinstance(v,(int,float)) and not math.isfinite(v) for v in defaults.values()):
        raise ValueError('chemistry parameters must be finite')
    if defaults.get('temperature',0)<0:
        raise ValueError('temperature must be nonnegative')
    if 'box' in defaults and (len(defaults['box'])!=2 or any(not math.isfinite(x) or x<=1.2 for x in defaults['box'])):
        raise ValueError('box requires two lengths greater than 1.2')
    if model=='copy':
        if not defaults['sequence'] or set(defaults['sequence'])-set('012'):
            raise ValueError('sequence uses symbols 0, 1, 2')
        if not defaults['alphabet'] or set(defaults['alphabet'])-set('012'):
            raise ValueError('alphabet uses symbols 0, 1, 2')
        if defaults['period']<=0 or not 0<=defaults['release_time']<=defaults['period']:
            raise ValueError('invalid association/release cycle')
        if any(not isinstance(defaults[k],int) or defaults[k]<0 for k in ('free_units','function_units')):
            raise ValueError('monomer counts must be nonnegative integers')
        if defaults['release'] not in ('cycle','never','local'):
            raise ValueError('release must be cycle, never or local')
        if defaults['seed_family'] not in (0,1) or any(k not in ('0','1','2') or not math.isfinite(v) or not -1<=v<=1 for k,v in defaults['functional_cosines'].items()):
            raise ValueError('invalid family or native angle cosine')
        if not isinstance(defaults['food_pairs'],int) or defaults['food_pairs']<0:
            raise ValueError('food_pairs must be a nonnegative integer')
        if any(k not in ('0','1','2') or not math.isfinite(v) or not -1<=v<=1 for k,v in defaults['functional_bend_cosines'].items()):
            raise ValueError('invalid functional bend cosine')
        if any(defaults[k]<=0 for k in ('food_ligand_width','food_binding_radius','food_reaction_radius')) or any(defaults[k]<0 for k in ('functional_bend_strength','food_ligand_energy','food_binding_rate','food_unbinding_rate','food_reaction_rate')):
            raise ValueError('invalid functional substrate parameters')
    elif model=='membrane':
        if not isinstance(defaults['units'],int) or defaults['units']<2 or not isinstance(defaults.get('fragment_size',1),int) or defaults.get('fragment_size',1)<1:
            raise ValueError('invalid membrane size')
        if defaults['initial'] not in ('straight','dispersed_fragments','dispersed_units') or defaults['short_length']<=0:
            raise ValueError('invalid membrane geometry')
        defaults.setdefault('fragment_size',defaults['units'])
        if defaults['initial']=='dispersed_units': defaults['fragment_size']=1
        if defaults['dock_width']<=0 or defaults['dock_capture']<=0 or any(defaults[k]<0 for k in ('dock_energy','dock_rate','bond_off_rate','break_extension')):
            raise ValueError('invalid local docking parameters')
    for key,criterion in raw.get('expected',{}).items():
        if not isinstance(criterion,(int,float,dict)) or isinstance(criterion,dict) and (not criterion or set(criterion)-{'min','max','eq'}):
            raise ValueError('Expected metric '+key+' needs min/max/eq thresholds')
    return raw


def load(path):
    return resolve(json.loads(Path(path).read_text(encoding="utf-8")))


def legacy(config):
    c = dict(config)
    model = "copy" if c.pop("mode")=="copy" else "membrane"
    engine={k:c.pop(k) for k in ("dt",) if k in c}
    raw=dict(schema_version=1,model=model,engine=engine,seed=c.pop('seed',0),
             duration=c.pop('duration',180. if model=='copy' else 100.),
             name=c.pop('case',model),branch=c.pop('branch','W0'),chemistry=c)
    return resolve(raw)


def observer_config(config):
    return {**config['chemistry'], 'mode':'copy' if config['model']=='copy' else 'vesicle',
            'case':config['name'], 'seed':config['seed']}
