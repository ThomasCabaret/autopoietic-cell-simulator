"""Ten-symbol amplification and expression under unchanged T7 local chemistry."""
import argparse
import copy
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SEQUENCE = '0010110101'  # five 0 and five 1, neither uniform nor palindromic


def scenario(mode='copy', seed=0, scale=1, duration=3200., dilute=False):
    if mode not in ('copy', 'expression') or scale not in (1, 2):
        raise ValueError('Unknown population condition')
    cfg = json.loads((ROOT/'demonstrators/configs/demo_binary_copy.json').read_text(encoding='utf-8'))
    cfg.update(name=f'P10_{mode}_reserve{scale}'+('_dilute' if dilute else ''), branch='P10', seed=seed, duration=duration,
        description='Single ten-symbol prepared G strand, abundant composite monomers; passive complete population census.', expected={})
    g = cfg['chemistry']
    g.update(sequence=SEQUENCE, free_units=400*scale if mode == 'copy' else 0,
        function_units=400*scale if mode == 'expression' else 0,
        box=[24*math.sqrt(scale*(2 if dilute else 1)), 18*math.sqrt(scale*(2 if dilute else 1))], initial_assemblies=[])
    return cfg


def plan(pilot=False):
    conditions = [(mode, seed, 1) for mode in ('copy', 'expression') for seed in range(3)]
    conditions += [(mode, 0, 2) for mode in ('copy', 'expression')]
    if pilot:
        conditions = [('copy', 0, 1), ('expression', 0, 1)]
    return dict(name='P10 pilot throughput and census' if pilot else 'P10 ten-symbol population distribution',
        workers=2, checkpoint_seconds=30., kinetic_window=50., record_trajectory=False,
        genetic_audit=True, population_audit=True, population_interval=10.,
        comparison_policy='Frozen T7 laws and parameters. One prepared G10 only. Prepared composite monomers bypass synthesis. G-only replication vs F-only expression are separate baths, not coupled cell function. Reserve2 doubles monomers and area at the same nominal supply density; one selected diagnostic seed, not a robustness cohort. All main seeds share horizon3200 (16 release cycles), no result-dependent extension.',
        tasks=([dict(scenario=scenario(mode, seed, scale, 50. if pilot else 3200.))
               for mode, seed, scale in conditions]+
               ([] if pilot else [dict(scenario=scenario(mode, dilute=True)) for mode in ('copy', 'expression')])))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pilot', action='store_true')
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(plan(a.pilot), indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
