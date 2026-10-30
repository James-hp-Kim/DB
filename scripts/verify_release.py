"""Verify every file listed in the bundled release manifest (standard library)."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
errors=[]
checked=0
for line in (ROOT/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
    expected,name=line.split('  ',1)
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        errors.append({'path':name,'error':'missing or outside release'})
    elif hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
        errors.append({'path':name,'error':'checksum mismatch'})
    checked+=1
print(json.dumps({'passed':not errors,'files':checked,'errors':errors},ensure_ascii=False))
raise SystemExit(bool(errors))
