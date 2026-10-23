"""Windows launchers use the same CLI as automated runs."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

try:
    if len(sys.argv)==3 and sys.argv[1]=='--archived-demo':
        from reconstruct_experiment import archived_demo
        archived_demo(sys.argv[2])
    else:
        from simulator.cli import main
        main()
except ModuleNotFoundError as exc:
    print('\nDependance absente : '+str(exc))
    print('Lancez demonstrators/installer.bat une fois, puis relancez la demonstration.')
    raise SystemExit(1)
