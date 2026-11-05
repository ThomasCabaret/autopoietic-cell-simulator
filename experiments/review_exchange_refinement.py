"""EN1 reuses the same declared gates, with EG1 as its fixed reference."""
from experiments.review_energy_exchange import collect as previous,decide as energy_decide
from simulator.campaign_io import write
from pathlib import Path


def decide(rows):
    result=energy_decide(rows)
    result['scope']='Three half-dt selected sensitivity checks against reused EG1. Fixed physical reaction/sample cadences; not numerical convergence, stochastic equivalence or fed maintenance.'
    return result


def collect(folder,require_complete=True):
    report=previous(folder,require_complete)
    if len(report['rows'])==3:report['decision']=decide(report['rows'])
    report['scope']='EN1 mechanical refinement only, EG1 chemistry and actual initial states unchanged.'
    write(Path(folder)/'exchange_refinement_review.json',report);return report
