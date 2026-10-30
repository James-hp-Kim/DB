"""Validate local documentation, source hashes, metadata and active skill links."""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

BASE=Path(__file__).resolve().parents[1]
errors=[]
for path in BASE.rglob('*.json'):
    if any(part in ('.venv','runs','private','__pycache__') for part in path.relative_to(BASE).parts): continue
    try: json.loads(path.read_text(encoding='utf-8-sig'))
    except (ValueError,UnicodeError) as exc: errors.append(f'{path.relative_to(BASE)}: {exc}')
for path in BASE.rglob('*.md'):
    if 'third_party' in path.relative_to(BASE).parts: continue
    text=re.sub(r'```.*?```','',path.read_text(encoding='utf-8'),flags=re.S)
    for ref in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
        if '://' in ref or ref.startswith('#'): continue
        target=unquote(ref.split('#')[0].strip('<>'))
        if not (path.parent/target).resolve().exists(): errors.append(f'{path.relative_to(BASE)} -> {target}')
snapshots=json.loads((BASE/'third_party/SNAPSHOTS.json').read_text(encoding='utf-8'))
for sid,src in snapshots.items():
    if hashlib.sha256((BASE/src['snapshot']).read_bytes()).hexdigest()!=src['snapshot_sha256']: errors.append('Source hash: '+sid)
for required in ['README_PERSONA_DB_AUTHORING.md','schemas/persona.schema.json','tests/test_persona_gate.py','README.md','START_HERE_KO.md','docs/VALIDATION.md','.agents/plugins/marketplace.json','plugins/expert-hub/plugin.json','plugins/expert-hub/.codex-plugin/plugin.json','plugins/expert-hub/mcp.json','plugins/expert-hub/.mcp.json']:
    if not (BASE/required).is_file(): errors.append('Missing: '+required)
if (BASE/'README_PERSONA_DB_AUTHORING.md').read_bytes()!=(BASE/'plugins/expert-hub/skills/expert/references/persona-authoring.md').read_bytes(): errors.append('Authoring README copies diverged')
print(json.dumps({'passed':not errors,'snapshot_hashes':len(snapshots),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
