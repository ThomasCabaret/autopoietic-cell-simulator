"""Compact progressive population report from saved evidence; never advances physics."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if __package__:
    from .campaign import validate, status
else:
    from campaign import validate, status
from simulator.campaign_io import read, write


def count(row, family, field):
    return sum(r[field] for r in row['types'] if r['family'] == family and
        r['topology'] == 'open' and r['length'] > 1 and r['sequence'] == row['_target'])


def summarize(population, config):
    target = min(population['target'], population['target'][::-1])
    records = population['state']['snapshots']
    if not records:
        return None
    family = 'F' if config['chemistry']['function_units'] else 'G'
    initial = records[0]['free_monomers_by_symbol'][family]
    series = []
    first_reserve_warning = None
    for record in records:
        row = dict(record, _target=target)
        stock = record['free_monomers_by_symbol'][family]
        if any(stock.get(symbol, 0) < .5*value for symbol, value in initial.items()):
            if first_reserve_warning is None: first_reserve_warning = record['time']
        new_polymer_units = sum(r['length']*r['new_count'] for r in record['types']
            if r['family'] == family and r['length'] > 1)
        new_polymer_chains = sum(r['new_count'] for r in record['types']
            if r['family'] == family and r['length'] > 1)
        exact = count(row, family, 'new_count')
        series.append(dict(time=record['time'], exact_new=exact,
            exact_new_detached=count(row, family, 'new_detached_count'),
            polymer_chains_new=new_polymer_chains, polymer_units_new=new_polymer_units,
            exact_fraction_of_polymer_units=exact*len(target)/new_polymer_units if new_polymer_units else None,
            free_monomers_by_symbol=stock, ligations=record['ligations'],
            crowd_contact_fraction=record['fraction_supports_in_core_contact'],
            categories=record['categories'][family]))
    cycles = [r for r in series if r['time'] > 0 and abs(r['time']/200-round(r['time']/200)) < 1e-7]
    last = records[-1]
    # A descriptive finite window only; no stationarity or true asymptote inferred.
    tail = cycles[-4:]
    flat = len(tail) == 4 and len({r['exact_new'] for r in tail}) == 1
    expected_units = len(target)+config['chemistry']['free_units']+config['chemistry']['function_units']
    for record in records:
        if sum(r['length']*r['count'] for r in record['types']) != expected_units:
            raise AssertionError('Saved population violates mass conservation')
        projected = {f: {} for f in ('G','F')}
        for item in record['types']:
            histogram = projected[item['family']];key = str(item['length'])
            histogram[key] = histogram.get(key, 0)+item['count']
        if projected != record['length_distribution']:
            raise AssertionError('Sequence and length distributions disagree')
    return dict(family=family, sampled_until=last['time'], snapshots=len(records),
        first_exact_sampled=population['first_passages'][family],
        first_reserve_below_half=first_reserve_warning,
        original_backbone_always_present=all(r['original_backbone_present'] for r in records),
        original_always_separate=all(r['original_still_separate'] for r in records),
        instantaneous_final=series[-1], cycle_boundaries=cycles,
        flat_exact_count_last_four_observed_cycles=flat,
        final_types=last['types'], final_length_distribution=last['length_distribution'],
        series=series)


def analyze(folder):
    folder = Path(folder).resolve(); manifest = validate(folder); snapshot = status(folder)
    rows = []
    for task, state in zip(manifest['tasks'], snapshot['tasks']):
        row = dict(task=task['id'], case=task['label'], seed=task['scenario']['seed'], phase=state['phase'],
            simulated_time=state.get('simulated_time', 0.), steps_per_second=state.get('steps_per_second'),
            eta_seconds=state.get('eta_seconds'), latest=state.get('population_latest'))
        if state.get('population') and (folder/state['population']).exists():
            # Atomic replacement by the worker makes progressive reads safe.
            population = read(folder/state['population'])
            row['population'] = summarize(population, task['scenario'])
        if state['phase'] == 'complete':
            evidence = read(folder/state['result'])
            expected = {k:v for k,v in manifest['source_sha256'].items() if k.startswith('simulator/')}
            if evidence['source_sha256'] != expected or evidence['scenario'] != task['scenario'] or not evidence['completed']:
                raise AssertionError('Result provenance differs from frozen task')
            p = row['population'];final = p['instantaneous_final']
            metrics = evidence['metrics'];key = 'translated_detached_ever' if p['family'] == 'F' else 'detached_copy_sets_ever'
            if final['exact_new_detached'] > metrics[key]:
                raise AssertionError('Current exact products exceed ever-made count')
            row['ever_exact_detached'] = metrics[key]
            row['certified_max_generation'] = metrics['certified_max_generation']
            row['elapsed_seconds'] = evidence['elapsed_seconds']
            row['source_verified'] = True
            if state.get('genetic_audit'):
                audit = read(folder/state['genetic_audit'])
                if audit['ligations'] != metrics['ligation_events']:
                    raise AssertionError('Ligation counters disagree')
                row['opportunity_exposure'] = audit['exposure']
        rows.append(row)
    report = dict(campaign=str(folder), counts=snapshot['counts'], controller_active=snapshot['controller_active'],
        complete_cohort=all(r['phase']=='complete' for r in rows), rows=rows,
        analysis_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limitations='G-only amplification and F-only expression are separate conditions. Strict symbol matching, irreversible backbones, finite stock and external release cycle. Finite plateaus are descriptive; first passages are sampled and no-event cases right-censored.')
    write(folder/'population_analysis.json',report)
    lines = ['# P10 — distribution des polymères', '',
        'Rapport progressif. Population instantanée ; le brin initial est exclu des nouveaux produits.',
        'Les passages sans événement restent censurés ; aucune asymptote ni viabilité déduite.', '',
        '| Essai | Graine | État | Temps recensé | Exacts nouveaux / libres | Polymères nouveaux | Monomères libres | Réserve <50% depuis |',
        '| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        p = row.get('population')
        if not p:
            lines.append(f"| {row['case']} | {row['seed']} | {row['phase']} | — | — | — | — | — |")
            continue
        final = p['instantaneous_final']
        lines.append(f"| {row['case']} | {row['seed']} | {row['phase']} | {p['sampled_until']:g} | {final['exact_new']} / {final['exact_new_detached']} | {final['polymer_chains_new']} | {sum(final['free_monomers_by_symbol'].values())} | {p['first_reserve_below_half']} |")
        lines += []
    lines += ['', 'Les séquences complètes, histogrammes de longueur et séries temporelles sont dans population_analysis.json.',
        'Les fichiers population.json de chaque essai contiennent le recensement intégral par type à chaque date.',
        'Un contact de cœur ne suffit pas à diagnostiquer un blocage par encombrement. Les contrôles de volume restent séparés.']
    (folder/'population_analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('\n'.join(lines),flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',nargs='?',type=Path)
    a = parser.parse_args()
    folder = a.folder or Path((ROOT/'outputs/campaigns/latest.txt').read_text(encoding='utf-8').strip())
    analyze(folder)
