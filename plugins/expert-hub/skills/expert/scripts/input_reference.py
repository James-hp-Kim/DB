"""Bounded local topic routing; never a compiler, bug detector or ingestion path."""
import hashlib
import re
from pathlib import Path

import knowledge as kb
from qa_core import dump

MAX_BYTES = 2 * 1024 * 1024
EXTENSIONS = {'.sv', '.svh', '.v', '.sdc', '.upf', '.log', '.rpt', '.csv', '.json', '.md', '.txt', '.sp', '.spice', '.cir'}
# Fixed queries prevent file text/instructions from becoming tool instructions.
RULES = (
    ('verification-result', r'\bMISMATCH\b|\bRESULT[ \t]+(?:PASS|FAIL)\b|\bUVM_(?:ERROR|FATAL)\b', '독립 reference model scoreboard'),
    ('async-fifo', r'async\w*[_ -]?fifo|\bfifo\b|gray[_\w]*|비동기\s*FIFO', 'async FIFO 포인터 reset'),
    ('cdc-rdc', r'\b(?:CDC|RDC|metastability)\b|clock[_ -]crossing|reset[_ -]crossing|클록\s*도메인', 'CDC RDC clock reset crossing'),
    ('sta', r'\b(?:WNS|TNS|slack|setup|hold)\b|타이밍\s*위반', 'STA WNS TNS setup hold'),
    ('timing-exceptions', r'\bset_(?:false_path|multicycle_path|max_delay|bus_skew)\b', 'SDC false_path multicycle Gray bus'),
    ('refresh', r'\b(?:tREFI|tRFC|refresh|self_refresh)\b|리프레시', 'refresh self-refresh debt'),
    ('power-intent', r'\b(?:UPF|isolation|retention|set_isolation|set_retention)\b', 'UPF isolation retention'),
    ('coverage-formal', r'\b(?:vacuity|covergroup|coverpoint|assert|assume|coverage)\b|커버리지', 'vacuity formal assumptions functional coverage'),
    ('ecc', r'\b(?:ECC|parity|syndrome|uncorrectable)\b', 'ECC parity 오류 주입'),
    ('power-data', r'\b(?:num_bitflips|total_power_W|idd|ipp|read_GBs)\b', 'num_bitflips total_power_W 장치 매핑'),
    ('disturbance', r'\b(?:RowHammer|RowPress)\b|행\s*교란', 'RowHammer retention'),
    ('ppa', r'\b(?:PPA|clock_gating|cell_area|dynamic_power)\b', 'PPA baseline clock gating'),
    ('rtl-semantics', r'\b(?:always_ff|always_comb|posedge|negedge|endmodule)\b', '순차 조합 latch parameter'),
)
PATTERNS = [(topic, re.compile(pattern, re.I), query) for topic, pattern, query in RULES]
NAND_RULES = (
    ('read-retry', r'\bretry\b|retry_count|read.retry|재시도|retry_epoch', 'retry epoch'),
    ('llr-quantization', r'\bLLR\b|quantiz\w*|saturat\w*|양자화|포화', 'LLR 포화'),
    ('ecc-result', r'\b(?:LDPC|syndrome|miscorrection|uncorrectable)\b|오정정', 'syndrome miscorrection'),
    ('nand-interface', r'\b(?:ONFI|DQS|NV.DDR)\b|parameter.page|인터페이스', 'ONFI timing'),
    ('error-physics', r'\b(?:retention|disturb|vref|pe_count)\b|열화|보존', 'retention 온도'),
    ('cdc-rdc', r'\b(?:CDC|RDC)\b|async.fifo|clock.crossing|reset.crossing', 'CDC RDC'),
    ('metrics', r'\b(?:RBER|FER|UBER)\b|raw_bits_compared|host_latency_ns', 'RBER FER 분모'),
)
NAND_PATTERNS = [(topic, re.compile(pattern, re.I), query) for topic, pattern, query in NAND_RULES]
HBM_RULES = (
    ('warpage', r'\bwarpage\b|워페이지|휨|박리|delaminat\w*', 'warpage'),
    ('bonding', r'MR[ -]?MUF|TC[ -]?NCF|underfill|언더필|하이브리드.*본딩|hybrid.*bond', 'MR-MUF'),
    ('thermal', r'\b(?:Tj|Rth|thermal|hotspot)\b|junction_temperature|power_per_die|열저항|발열|온도', '열저항'),
    ('reliability', r'\b(?:censor\w*|Weibull|Arrhenius|reliability)\b|failed_devices|신뢰성|무고장|가속시험', '신뢰성'),
    ('tsv', r'\bTSV\b|실리콘관통|microbump|마이크로범프', 'TSV'),
    ('sensor-errors', r'\b(?:ECC|throttl\w*|sensor)\b|스로틀|센서|오류', '센서 스로틀'),
)
HBM_PATTERNS = [(topic, re.compile(pattern, re.I), query) for topic, pattern, query in HBM_RULES]


def reference_input(file, context=None, query=None, max_chars=3500):
    """Read at most 2 MiB locally; return only line locations and scoped summaries."""
    profile, stores = kb.scope(context)  # Gate must precede even file stat/open.
    pack = {'chip-design-verification': 'rtl', 'nand-expert': 'nand', 'hbm-expert': 'hbm'}.get(profile['id'])
    semiconductor = profile['id'] == 'semiconductor-ai'
    if semiconductor:
        pack = 'chip-review'
    if pack is None or pack not in stores:
        raise ValueError('Select chip-design-verification, nand-expert or hbm-expert through catalog first')
    kb.number(max_chars, 2000, 6000, 'max_chars')
    if query is not None and (not isinstance(query, str) or not query.strip() or len(query) > 300):
        raise ValueError('query: 1..300 characters required')
    if not isinstance(file, (str, Path)) or not str(file).strip():
        raise ValueError('file: an explicit local path is required')
    path = Path(file)
    if path.suffix.lower() not in EXTENSIONS:
        raise ValueError('Unsupported extension; provide a UTF-8 RTL/report/CSV excerpt')
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('Input exceeds 2 MiB; supply a focused excerpt, not a whole run')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Input grew beyond 2 MiB')
    text = raw.decode('utf-8-sig')
    if '\x00' in text:
        raise ValueError('Binary/NUL content is not supported')
    # Bounded evidence locations; never return original lines or other file content.
    found = []
    lines = text.splitlines()
    patterns = {'nand': NAND_PATTERNS, 'hbm': HBM_PATTERNS, 'rtl': PATTERNS, 'chip-review': PATTERNS}[pack]
    for topic, pattern, search in patterns:
        locations = []
        for lineno, line in enumerate(lines, 1):
            if pattern.search(line):
                locations.append(lineno)
                if len(locations) == 3: break
        if locations:
            found.append({'topic': topic, 'lines': locations, 'query': search})
    if semiconductor:
        if path.suffix.lower() in {'.sp', '.spice', '.cir'}:
            found.insert(0, {'topic': 'analog', 'lines': [], 'query': 'SPICE 회로 corner noise'})
            pack = 'chip-analog'
        elif any(x['topic'] in {'refresh', 'disturbance', 'power-data'} for x in found):
            pack = 'chip-memory'
        elif found or path.suffix.lower() in {'.v', '.sv', '.svh', '.sdc', '.upf'}:
            pack = 'chip-rtl'
        elif query and re.search(r'DRAM|HBM|NAND|SRAM|메모리', query, re.I):
            pack = 'chip-memory'
        elif query and re.search(r'SPICE|아날로그|회로', query, re.I):
            pack = 'chip-analog'
    selected = found[:3]
    search = query.strip() if query is not None else ' '.join(x['query'] for x in selected)[:300]
    result = {
        'persona': profile['id'],
        'selected_pack': pack,
        'input': {'suffix': path.suffix.lower(), 'bytes': len(raw), 'lines': len(lines),
                  'sha256': hashlib.sha256(raw).hexdigest()},
        'signals': [{'topic': x['topic'], 'lines': x['lines']} for x in selected],
        'other_topics': [x['topic'] for x in found[3:]],
        'query': search,
        'limits': '키워드 기반 참고자료 연결만 수행. 주석·문자열도 매칭됨; 결함 판정·RTL 파싱·STA·시뮬레이션 아님. 입력은 저장하지 않음.',
    }
    if not search:
        result['gap'] = '관련 주제를 찾지 못함. 블록·증상·검토 목적을 query로 지정하세요.'
        return result
    # Reserve the wrapper's actual serialized size, including escaped query text.
    budget = max_chars - len(dump({**result, 'retrieval': None})) - 16
    if budget < 1200:
        raise ValueError('Increase max_chars or shorten query')
    result['retrieval'] = kb.lookup(search, context=context, packs=[pack], max_chars=budget, limit=2 if pack == "hbm" else 3)
    if len(dump(result)) > max_chars:
        raise RuntimeError('Response budget invariant violated')
    return result
