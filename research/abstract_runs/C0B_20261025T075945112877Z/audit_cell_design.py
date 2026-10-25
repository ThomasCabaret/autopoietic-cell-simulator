"""Conditional material/causal audit and 2D sizing, NOT molecular dynamics.

Named catalysts are specification roles only. No sequence-to-function lookup is
exported to the particle engine. Stocks and lengths are explicit assumptions.
"""
import argparse,copy,hashlib,json,math
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'research/minimal_cell_spec.json'


def load():return json.loads(SPEC.read_text(encoding='utf-8'))


def mass_sum(terms,masses):
    return [sum(n*masses[s][k] for s,n in terms.items()) for k in range(4)]


def network(spec,length=24):
    if length<2 or length%2:raise ValueError('Budget assumes positive even binary length')
    masses=copy.deepcopy(spec['masses_XYZ_carrier']);reactions=[]
    halves={0:length//2,1:length//2}
    roles=spec['roles']
    def add(rid,inputs,outputs,catalysts,kind,**extra):
        reactions.append(dict(id=rid,inputs=inputs,outputs=outputs,catalysts=catalysts,kind=kind,**extra))
    energy=spec['assembly_energy_per_dimer']
    for role in roles:
        for product in role['products']:
            ingredients={s:n for s,n in zip(('X','Y','Z'),masses[product][:3]) if n}
            ingredients['E']=energy
            add('make_'+product,ingredients,{product:1,'W':energy},[role['tool']],'synthesis')
    for role in roles:
        g,e=role['gene'],role['tool']
        masses[g]=mass_sum({'N0':halves[0],'N1':halves[1]},masses)
        masses[e]=mass_sum({'A0':halves[0],'A1':halves[1]},masses)
        for target,family,prefix in ((g,'genetic','copy_'),(e,'functional','express_')):
            inputs={s:halves[b] for b,s in enumerate(spec['monomer_families'][family])}
            cost=(length-1)*spec['polymerization_energy_per_bond']
            inputs['E']=cost
            add(prefix+target,inputs,{target:1,'W':cost},[g],'polymer',family=family)
    masses['L_surface']=list(masses['L'])
    if spec['insertion']['enabled']:
        cost=spec['insertion']['energy_per_lipid'];inputs={'L':1};outputs={'L_surface':1}
        if cost:inputs['E']=cost;outputs['W']=cost
        add('insert_L',inputs,outputs,[spec['insertion']['tool']] if spec['insertion']['tool'] else [],'insertion')
    seeds=[r[k] for r in roles for k in ('gene','tool')]+['L_surface']
    return dict(masses=masses,reactions=reactions,seeds=seeds,
        essentials=list(dict.fromkeys(['N0','N1','A0','A1','L','L_surface']+seeds)),
        length=length,roles=copy.deepcopy(roles))


def audit(spec,model=None):
    model=model or network(spec)
    masses=model['masses'];errors=[]
    for r in model['reactions']:
        unknown=(set(r['inputs'])|set(r['outputs'])|set(r['catalysts']))-set(masses)
        if unknown:errors.append('unknown_species:'+r['id']);continue
        if mass_sum(r['inputs'],masses)!=mass_sum(r['outputs'],masses):errors.append('mass:'+r['id'])
        if r['kind']=='synthesis' and not r['catalysts']:errors.append('uncatalyzed:'+r['id'])
        if r['kind']=='polymer':
            permitted=set(spec['monomer_families'][r['family']])|{'E'}
            if set(r['inputs'])-permitted:errors.append('wrong_monomer_family:'+r['id'])
    if set(spec['food'])-set(spec['allowed_food']):errors.append('premade_food')
    if not set(spec['food'])<=set(spec['imports']):errors.append('missing_import')
    if 'W' not in spec['exports']:errors.append('no_waste_export')
    available=(set(spec['food'])&set(spec['imports']))|set(model['seeds'])
    produced=set();enabled=set()
    while True:
        old=set(available)
        for r in model['reactions']:
            if set(r['inputs'])|set(r['catalysts'])<=available:
                produced.update(r['outputs']);available.update(r['outputs']);enabled.add(r['id'])
        if old==available:break
    missing=sorted(set(model['essentials'])-produced)
    hidden=sorted({s for r in model['reactions'] for s in r['catalysts']}-produced-set(spec['allowed_food']))
    return dict(conditionally_regenerable=not(errors or missing or hidden),errors=errors,
        not_regenerated=missing,nonregenerated_catalysts=hidden,enabled=sorted(enabled),
        meaning='AND dependencies, material consistency and renewable roles with constructed seeds; no physical or kinetic viability proof')


def sizing(spec,case,extra_roles=0):
    cfg=spec['sizing'];roles=len(spec['roles'])+extra_roles;length=case['length']
    gene_units=roles*case['gene_copies']*length;tool_units=roles*case['tool_copies']*length
    beads=dict(genes=2*gene_units,tools=2*tool_units,free_N=2*case['free_N'],
        free_A=2*case['free_A'],free_L=2*case['free_L'],raw_food=case['raw_food_inside'],
        fuel=case['fuel_inside'],waste=case['waste_cap'])
    interior=sum(beads.values());radius_area=cfg['effective_bead_diameter']/2*math.sqrt(interior/case['area_fraction'])
    radius=max(radius_area,(length-1)/2+1)+cfg['membrane_margin']
    h=cfg['lipid_thickness'];outer=cfg['outer_pitch']
    delta=h*outer/(radius+h/2)
    short=outer-delta;pitch=(outer+short)/2
    membrane=math.ceil(2*math.pi*radius/pitch)
    current_delta=outer-cfg['current_inner_pitch']
    current_radius=h*(outer+cfg['current_inner_pitch'])/(2*current_delta)
    current_units=math.pi/math.asin(current_delta/(2*h))
    return dict(id=case['id'],roles=roles,beads=beads,interior_beads=interior,
        gene_chains=roles*case['gene_copies'],tool_chains=roles*case['tool_copies'],
        free_compound_molecules=case['free_N']+case['free_A']+case['free_L'],
        content_radius=radius-cfg['membrane_margin'],membrane_radius=radius,
        membrane_molecules=membrane,membrane_beads=2*membrane,cell_beads=interior+2*membrane,
        outside_beads=case['outside_halo'],total_beads=interior+2*membrane+case['outside_halo'],
        needed_inner_pitch=short,needed_pitch_ratio=short/outer,
        current_preferred_radius=current_radius,current_preferred_units=current_units,
        current_curvature_fits=radius<=current_radius,
        surface_per_content_bead=2*math.pi*radius/interior,
        note='Geometric occupancy estimate, not an equilibrium or permeability prediction')


def replacement(spec,case,budget):
    model=network(spec,case['length']);rx={r['id']:r for r in model['reactions']}
    flux=Counter()
    for role in spec['roles']:
        flux['copy_'+role['gene']]=case['gene_copies']
        flux['express_'+role['tool']]=case['tool_copies']
    flux['insert_L']=budget['membrane_molecules']
    demand=Counter()
    for rid,v in flux.items():demand.update({s:n*v for s,n in rx[rid]['inputs'].items()})
    for s in ('N0','N1','A0','A1'):flux['make_'+s]=demand[s]
    flux['make_L']=budget['membrane_molecules']
    net=Counter()
    for rid,v in flux.items():
        for s,n in rx[rid]['inputs'].items():net[s]-=n*v
        for s,n in rx[rid]['outputs'].items():net[s]+=n*v
    assert all(net[s]==0 for s in ('N0','N1','A0','A1','L'))
    return dict(food={s:-net[s] for s in spec['food']},waste=net['W'],
        new_material={s:n for s,n in net.items() if n>0 and s!='W'},reaction_events=dict(flux),
        scope='One replacement of all chosen genes/tools and complete boundary, excluding free pools; not a turnover rate or an energy calibration')


def negative_controls(spec):
    rows={}
    model=network(spec)
    for role in spec['roles']:
        bad=copy.deepcopy(model);bad['reactions']=[r for r in bad['reactions'] if r['id']!='express_'+role['tool']]
        rows['missing_expression_'+role['tool']]=audit(spec,bad)
    bad=copy.deepcopy(spec);bad['insertion']['enabled']=False;rows['missing_insertion']=audit(bad)
    bad=copy.deepcopy(spec);bad['imports'].remove('X');rows['blocked_food']=audit(bad)
    bad=copy.deepcopy(spec);bad['exports']=[];rows['blocked_waste']=audit(bad)
    bad=copy.deepcopy(spec);bad['food'].append('N0');rows['premade_nucleotide_feed']=audit(bad)
    bad=copy.deepcopy(model);bad['reactions'][0]['inputs']['Z']=1;rows['wrong_mass']=audit(spec,bad)
    bad=copy.deepcopy(model);r=next(r for r in bad['reactions'] if r['id']=='express_EN')
    r['inputs']['N0']=r['inputs'].pop('A0');rows['isomass_wrong_family']=audit(spec,bad)
    bad=copy.deepcopy(model);bad['reactions'][0]['catalysts']=[];rows['uncatalyzed_nucleotide']=audit(spec,bad)
    assert all(not r['conditionally_regenerable'] for r in rows.values())
    return rows


def assess(spec):
    model=network(spec);check=audit(spec,model)
    if not check['conditionally_regenerable']:raise ValueError(check)
    budgets=[sizing(spec,c) for c in spec['sizing']['cases']]
    nominal=spec['sizing']['cases'][1]
    species=set(model['masses'])-{'L_surface'}
    return dict(kind='conditional_cell_design_audit_not_molecular_dynamics',audit=check,
        target_species=sorted(species),target_species_count=len(species),
        primitive_material_kinds=len(spec['primitive_material_kinds']),
        budgets=budgets,replacement=replacement(spec,nominal,budgets[1]),
        variants=[dict(id=v['id'],roles=len(spec['roles'])+len(v['extra_roles']),
            target_species_count=len(species)+2*len(v['extra_roles']),
            nominal=sizing(spec,nominal,len(v['extra_roles'])),
            status='counted dependency obligation, no molecular validation or additional-role reaction audit') for v in spec['variants']],
        negative_controls=negative_controls(spec))


def execute(spec_path,output):
    output.mkdir(parents=True,exist_ok=False)
    src=Path(__file__).read_bytes();spec_bytes=spec_path.read_bytes()
    (output/'audit_cell_design.py').write_bytes(src);(output/'config.json').write_bytes(spec_bytes)
    result=assess(json.loads(spec_bytes))
    (output/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    recipe=dict(recipe_version=1,kind='cell_design_audit',
        source_sha256={'audit_cell_design.py':hashlib.sha256(src).hexdigest()},
        config_sha256=hashlib.sha256(spec_bytes).hexdigest(),
        command='python audit_cell_design.py --spec config.json --output <new-folder>')
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2),encoding='utf-8')
    print(json.dumps(dict(folder=str(output),target_species=result['target_species_count'],
        budgets=[{k:b[k] for k in ('id','total_beads','membrane_molecules','membrane_radius','needed_inner_pitch')} for b in result['budgets']],
        negative_controls=len(result['negative_controls'])),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spec',type=Path,default=SPEC)
    p.add_argument('--output',type=Path)
    a=p.parse_args();out=a.output or ROOT/'research/abstract_runs'/('C0B_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    execute(a.spec.resolve(),out.resolve())
