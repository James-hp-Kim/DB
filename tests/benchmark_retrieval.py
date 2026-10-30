"""Reference payload sizes, not actual model usage or billing tokens."""
import json
import statistics
import sys
import time
import os
import tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
from qa_core import dump
import knowledge as kb
from mcp_server import TOOLS
try:
    import tiktoken
    encoder=tiktoken.get_encoding('o200k_base')
except ImportError:
    encoder=None


def count(text):
    return {'characters':len(text),'reference_tokens':len(encoder.encode(text)) if encoder else None}


base=(SKILL/'SKILL.md').read_text(encoding='utf-8')
cards='\n'.join(p.read_text(encoding='utf-8') for p in sorted((SKILL/'packs').glob('*/cards/*.md')))
receipt_dir=tempfile.TemporaryDirectory(prefix='expert-benchmark-')
os.environ['EXPERT_CONTEXT_DIR']=receipt_dir.name
choice=kb.available('품질보증',limit=1)
context=choice['personas'][0]['context']
cases=[]
for query,rid in [('불량률 분모','common:data-contract'),('미세 드리프트 EWMA','quality:ewma'),('Western Electric 8점','quality:weco-rules'),('측정시스템 MSA','quality:msa')]:
    timings=[]
    for _ in range(10):
        start=time.perf_counter()
        found=kb.lookup(query,context=context)
        detail=kb.read([rid],context=context,sections=['conditions','procedure','limits'])
        timings.append((time.perf_counter()-start)*1000)
    payload=dump(choice)+'\n'+dump(found)+'\n'+dump(detail)
    cases.append({'query':query,'expected_in_top3':rid in [r['id'] for r in found['matches']],'selected_record':rid,'retrieval_only':count(payload),'entry_plus_retrieval':count(base+'\n'+payload),'median_local_ms':round(statistics.median(timings),3)})
print(json.dumps({'date':'2026-10-30','tokenizer':'o200k_base' if encoder else None,'scope':'Includes one persona-search response per case (conservative; context normally reused). Reference text comparison: fixed selected records/sections; not autonomous reasoning, end-to-end latency or total billing. Excludes prompt, analysis files, inference, answers and protocol overhead. Local timing excludes process startup.', 'entry_skill':count(base),'entry_plus_all_cards':count(base+'\n'+cards),'tool_definitions_separate':count(dump(TOOLS)),'cases':cases},ensure_ascii=False,indent=2))

receipt_dir.cleanup()
