"""Compare reference payloads; never claims billing or general search accuracy."""
import json
import hashlib
import os
import sys
import tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
SKILL=BASE/'plugins/expert-hub/skills/expert'
sys.path.insert(0,str(SKILL/'scripts'))
import knowledge as kb
from qa_core import dump
try:
    import tiktoken
    encoder=tiktoken.get_encoding('o200k_base')
except ImportError:
    encoder=None


def count(text):
    return {'characters':len(text),'reference_tokens':len(encoder.encode(text)) if encoder else None}


def main():
    entry=(SKILL/'SKILL.md').read_text(encoding='utf-8')
    whole=(SKILL/'packs/semiconductor/records.jsonl').read_text(encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory(prefix='semi-benchmark-') as tmp:
        os.environ['EXPERT_CONTEXT_DIR']=tmp
        for query,rid in [('단일 소자 누설 분해','semiconductor:e01'),('동적전력','semiconductor:k01'),
                          ('HBM 대역폭','semiconductor:k06'),('IGZO retention','semiconductor:n32')]:
            catalog=kb.available('반도체기초전문가',limit=1)
            ctx=catalog['personas'][0]['context']
            hits=kb.lookup(query,context=ctx,max_chars=2500)
            detail=kb.read([rid],context=ctx,sections=['conditions','limits'],max_chars=2500)
            refs=detail['items'][0]['sources']
            source=kb.sources(refs,context=ctx)
            payload='\n'.join(dump(x) for x in [catalog,hits,detail,source])
            cases.append({'query':query,'selected_id':rid,'expected_in_top3':rid in [x['id'] for x in hits['matches']],
                          'selected_sections':['conditions','limits'],'retrieval_with_catalog_and_sources':count(payload),
                          'entry_plus_retrieval':count(entry+'\n'+payload)})
    result={'date':'2026-10-30','tokenizer':'o200k_base' if encoder else None,
            'scope':'Four fixed examples, known selected IDs. Includes fresh catalog, lookup, conditions/limits and cited source metadata. Comparison is entry Skill plus whole semiconductor JSONL vs entry Skill plus selected retrieval. Excludes user input, raw data, analysis/answer tokens, protocol, tool definitions, retries and other pack retrieval. Not billing savings or production search accuracy.',
            'entry_sha256':hashlib.sha256(entry.encode('utf-8')).hexdigest(),'pack_sha256':hashlib.sha256(whole.encode('utf-8')).hexdigest(),'entry_skill':count(entry),'entry_plus_full_semiconductor_pack':count(entry+'\n'+whole),'cases':cases}
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
