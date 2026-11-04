"""Complete L3 result figure, using the same display/thresholds as L2."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.lipid_curvature_followup import latest
from simulator.campaign_io import read
from experiments.review_lipid_curvature import collect
from experiments.prepare_lipid_curvature import VARIANTS
from experiments.render_lipid_energy import plot


if __name__=='__main__':
    job=latest();r=collect(Path(read(job/'job.json')['campaigns'][0]));plot(r['rows'],VARIANTS,
        ('L2','Pose','Courbure','Combinés','Délié','Sans bonus','Sans outil'),ROOT/'research/BATCH_38_RESULTS.png',
        'L3 achevé · transitoire réduit, crible thermique encore refusé · références L2 réutilisées','L3')
