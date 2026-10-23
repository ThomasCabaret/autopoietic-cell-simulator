import json
from pathlib import Path
from run_local_research import CopyObserver, VesicleObserver
from local_dynamics import copying, vesicle
c=json.loads(Path(__file__).with_name('config.json').read_text(encoding='utf-8'))
o=CopyObserver(c) if c['mode']=='copy' else VesicleObserver(c)
(copying if c['mode']=='copy' else vesicle)(c,c['seed'],o)
print(json.dumps(o.summary(),indent=2))
