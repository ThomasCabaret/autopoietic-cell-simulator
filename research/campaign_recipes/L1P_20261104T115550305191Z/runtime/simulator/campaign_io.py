"""Atomic campaign records and OS-released locks; no simulation dynamics."""
import json,os,time,uuid
from contextlib import contextmanager
from pathlib import Path


def read(path,default=None):
    p=Path(path)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default


def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    tmp.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    # Windows readers/antivirus can briefly deny rename of an otherwise writable
    # destination. Retry this one atomic IO transaction, never a simulation task.
    for attempt in range(7):
        try:
            tmp.replace(path);return
        except PermissionError:
            if os.name!='nt' or attempt==6:raise
            time.sleep(.01*2**attempt)


@contextmanager
def lock(path):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('a+b') as f:
        if f.tell()==0:f.write(b'0');f.flush()
        f.seek(0)
        if os.name=='nt':
            import msvcrt
            msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:yield
        finally:
            f.seek(0)
            if os.name=='nt':msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(f,fcntl.LOCK_UN)


def busy(path):
    try:
        with lock(path):return False
    except OSError:return True
