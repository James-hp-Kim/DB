"""Fixed NAND retrieval payload benchmark, not billing-token measurement."""
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

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
    skill=(SKILL/'SKILL.md').read_text(encoding='utf-8')
    cards='\n'.join(p.read_text(encoding='utf-8') for p in sorted((SKILL/'packs/nand/cards').glob('*.md')))
    cases=[]
    with tempfile.TemporaryDirectory(prefix='nand-benchmark-') as tmp, patch.dict(os.environ,{'EXPERT_CONTEXT_DIR':tmp}):
        choice=kb.available('NAND',limit=1)
        context=choice['personas'][0]['context']
        for query,rid in [('retry epoch','nand:v12'),('LLR 포화','nand:v14'),('ONFI 6.0','nand:s01'),('P01','nand:p01')]:
            found=kb.lookup(query,context=context,max_chars=2400)
            details=kb.read([rid],context=context,sections=['conditions','limits'],max_chars=2400)
            refs=details['items'][0]['sources'][:1]
            source=kb.sources(refs,context=context,max_chars=1800)
            payload='\n'.join(dump(x) for x in [choice,found,details,source])
            cases.append({'query':query,'selected_id':rid,'expected_in_top3':rid in [r['id'] for r in found['matches']],
                          'lookup':count(dump(found)),'conditions_limits':count(dump(details)),
                          'source':count(dump(source)),'entry_plus_retrieval':count(skill+'\n'+payload)})
    print(json.dumps({'date':'2026-10-30','tokenizer':'o200k_base' if encoder else None,
       'scope':'Fixed queries and preselected relevant records; includes entry skill, persona search, lookup, conditions/limits and one source. Excludes prompts, input files, inference, answer, history and protocol/tool-definition overhead. Not overall billed tokens, autonomy or accuracy.',
       'entry_plus_all_nand_cards':count(skill+'\n'+cards),'cases':cases},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
