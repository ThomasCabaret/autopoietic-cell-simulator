"""Curated references to local research outputs; no experiment data in Git."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8'))
def inside(path,root):
    path=Path(path).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('Résultat hors du répertoire local de campagne.')
    return path


def available(root=ROOT):
    root=Path(root);outputs=root/'outputs';latest=outputs/'competitive_relaxation_mechanism_followups/latest.txt'
    if not latest.exists():return []
    job=inside(latest.read_text(encoding='utf-8').strip(),outputs);cfg=read(job/'job.json');rows=[]
    for campaign in cfg['campaigns']:
        folder=inside(campaign,job);manifest=folder/'manifest.json'
        if hashlib.sha256(manifest.read_bytes()).hexdigest()!=(folder/'manifest.sha256').read_text().strip():raise ValueError('Manifeste local modifié.')
        for task in read(manifest)['tasks']:
            if not task['label'].startswith('CR1_assembly_'):continue
            state_path=folder/'tasks'/task['id']/'state.json'
            if not state_path.exists():continue
            state=read(state_path)
            if not state.get('checkpoint'):continue
            checkpoint=inside(folder/state['checkpoint'],folder)
            if checkpoint.exists():rows.append(dict(label=task['label'],status=state['status'],
                checkpoint=str(checkpoint),config=task['scenario'],time=state.get('simulated_time'),
                note='Sous-système membrane : dimères H/T fournis, sans génétique ni maintien cellulaire.'))
    return rows
