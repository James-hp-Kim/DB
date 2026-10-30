"""Bounded local evidence routing for semiconductor inputs; no data ingestion."""
import argparse
import hashlib
import re
from pathlib import Path

import knowledge as kb
from qa_core import dump

MAX_BYTES = 2 * 1024 * 1024
RULES = (
    ('leakage', r'누설|\b(?:Ioff|Vgs|Vds|Vbs|leakage|drain_off_current|GIDL)\b', '단일 소자 누설 분해'),
    ('dram', r'\bDRAM\b|리프레시|\b(?:tREFI|tRFC|VRT)\b', 'DRAM retention'),
    ('nand', r'\b(?:NAND|P/E|RBER|LDPC|ECC)\b|낸드|재시도', 'NAND 보존'),
    ('hbm', r'\b(?:HBM|TSV)\b|스택|열저항', 'HBM 열과 전원'),
    ('igzo', r'\b(?:IGZO|2T0C)\b', 'IGZO retention'),
    ('power', r'동적전력|\b(?:dynamic_power|DVFS|power.gating)\b|게이팅', '동적전력 전원 차단'),
    ('sense', r'\b(?:Ccell|Cbl)\b|전하 공유|센싱', '전하공유 셀 누설 예산'),
)


def reference(file, context, query=None, max_chars=3500):
    profile, stores = kb.scope(context)
    if profile['id'] != 'semiconductor-basics' or 'semiconductor' not in stores:
        raise ValueError('Search and select semiconductor-basics through catalog first')
    kb.number(max_chars, 2000, 6000, 'max_chars')
    if query is not None and (not isinstance(query, str) or not query.strip() or len(query) > 300):
        raise ValueError('query: 1..300 characters required')
    path = Path(file)
    if path.suffix.lower() not in {'.csv', '.json', '.txt', '.md', '.log', '.rpt', '.cir', '.sp'}:
        raise ValueError('Provide a UTF-8 CSV/JSON/text/report excerpt')
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('Input exceeds 2 MiB; provide a focused excerpt')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Input grew beyond 2 MiB')
    text = raw.decode('utf-8-sig')
    if '\x00' in text:
        raise ValueError('Binary/NUL input is unsupported')
    lines = text.splitlines()
    found = []
    for topic, pattern, search in RULES:
        regex = re.compile(pattern, re.I)
        locations = [n for n, line in enumerate(lines, 1) if regex.search(line)][:3]
        if locations:
            found.append({'topic': topic, 'lines': locations, 'query': search})
    selected = found[:3]
    search = query.strip() if query else ' '.join(item['query'] for item in selected)[:300]
    result = {'persona': profile['id'],
              'input': {'bytes': len(raw), 'lines': len(lines), 'sha256': hashlib.sha256(raw).hexdigest()},
              'signals': [{'topic': x['topic'], 'lines': x['lines']} for x in selected],
              'other_topics': [x['topic'] for x in found[3:]], 'query': search,
              'limits': '키워드 연결만 수행. 수치·단위 검증이나 원인 판정이 아님. 원문은 반환·등록하지 않음. 신호가 없으면 질문을 query로 지정.'}
    if not search:
        result['gap'] = 'No matching topic; provide an explicit query'
        return result
    budget = max_chars - len(dump({**result, 'retrieval': None})) - 16
    if budget < 1200:
        raise ValueError('Increase max_chars or shorten query')
    result['retrieval'] = kb.lookup(search, context=context, packs=['semiconductor'], limit=3, max_chars=budget)
    if len(dump(result)) > max_chars:
        raise RuntimeError('Response exceeded character budget')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--context', required=True)
    parser.add_argument('--query')
    parser.add_argument('--max-chars', type=int, default=3500)
    args = parser.parse_args()
    try:
        print(dump(reference(**vars(args))))
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
