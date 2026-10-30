"""Read-only package integrity, collision and synthetic-fixture checks (stdlib)."""
import argparse
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root, hub=None):
    root = root.resolve()
    errors, metrics = [], {}
    manifest = root / 'exam-kit/MANIFEST.sha256'
    entries, seen = [], set()
    for line in manifest.read_text(encoding='utf-8').splitlines():
        parts = line.split('  ', 1)
        if len(parts) != 2:
            errors.append('Malformed manifest line')
            continue
        expected, name = parts
        rel = PurePosixPath(name)
        allowed = name.startswith(('exam-kit/', '.agents/skills/prompt-refine/', '.agents/skills/fact-grounding/'))
        if (not re.fullmatch(r'[0-9a-f]{64}', expected) or rel.is_absolute()
                or '..' in rel.parts or '\\' in name or ':' in name or not allowed or name in seen):
            errors.append('Unsafe or duplicate manifest entry: ' + name)
            continue
        seen.add(name)
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file() or digest(path) != expected:
            errors.append('Missing, escaped or changed file: ' + name)
            continue
        entries.append(name)
        if hub is not None:
            target = (hub.resolve() / name).resolve()
            if not target.is_relative_to(hub.resolve()):
                errors.append('Target escapes repository: ' + name)
            elif target.exists() and (not target.is_file() or digest(target) != expected):
                errors.append('Different existing target; do not overwrite: ' + name)
    metrics['manifest_files'] = len(entries)
    if not entries:
        errors.append('Empty manifest')
    for owned in ('exam-kit', '.agents/skills/prompt-refine', '.agents/skills/fact-grounding'):
        for path in (root / owned).rglob('*'):
            if path.is_file():
                rel = path.relative_to(root).as_posix()
                if rel not in seen and rel != 'exam-kit/MANIFEST.sha256':
                    errors.append('Unlisted package file: ' + rel)

    global_body = (root / 'exam-kit/global/AGENTS.md').read_text(encoding='utf-8')
    metrics['global_characters_including_newline'] = len(global_body)
    if len(global_body) > 150:
        errors.append('Global instruction exceeds 150 characters')
    for name in ('fact-grounding', 'prompt-refine'):
        skill = root / f'.agents/skills/{name}/SKILL.md'
        text = skill.read_text(encoding='utf-8-sig')
        if not text.startswith('---\n') or f'\nname: {name}\n' not in text or '\ndescription:' not in text:
            errors.append('Invalid skill metadata: ' + name)
        metrics[name + '_characters'] = len(text)
        for label, link in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text):
            if '://' not in link and not (skill.parent / link).is_file():
                errors.append('Missing linked reference: ' + label)

    bench = root / 'exam-kit/benchmarks'
    cases = [json.loads(line) for line in (bench / 'cases.jsonl').read_text(encoding='utf-8').splitlines()]
    if len({x['id'] for x in cases}) != len(cases):
        errors.append('Duplicate evaluation case ids')
    for case in cases:
        for name in case['inputs']:
            path = (bench / name).resolve()
            if not path.is_relative_to(bench.resolve()) or not path.is_file():
                errors.append('Missing or escaped case input: ' + case['id'])
    metrics['evaluation_cases'] = len(cases)

    with (bench / 'fixtures/sales.csv').open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    unique = list({tuple(row.items()): row for row in rows}.values())
    kept = [row for row in unique if row['currency'] == 'KRW' and row['amount'] != '']
    totals = {}
    for row in kept:
        month = row['date'][:7]
        totals[month] = totals.get(month, Decimal(0)) + Decimal(row['amount'])
    actual = {'raw_rows':len(rows), 'exact_duplicates_removed':len(rows)-len(unique),
              'excluded_other_currency':sum(x['currency'] != 'KRW' for x in unique),
              'missing_amount_rows':sum(x['currency'] == 'KRW' and x['amount'] == '' for x in unique),
              'included_rows':len(kept), '2026-01_KRW':float(totals['2026-01']),
              '2026-02_KRW':float(totals['2026-02']),
              'growth_percent':float((totals['2026-02']/totals['2026-01']-1)*100)}
    expected = json.loads((bench / 'expected.json').read_text(encoding='utf-8'))
    for name, value in actual.items():
        if abs(value - expected['sales'][name]) > 1e-9:
            errors.append('Fixture expectation mismatch: ' + name)
    metrics['synthetic_sales'] = actual
    docs = [json.loads(x) for x in (bench/'fixtures/documents.jsonl').read_text(encoding='utf-8').splitlines()]
    if not any(x['id'] == expected['documents']['source_id'] and x['status'] == 'approved' for x in docs):
        errors.append('Missing approved evidence fixture')
    events = [json.loads(x) for x in (bench/'fixtures/events.jsonl').read_text(encoding='utf-8').splitlines()]
    successes = sorted({x['event_id'] for x in events if x['result'] == 'success'})
    if successes != expected['workflow']['successful_ids']:
        errors.append('Workflow fixture expectation mismatch')

    return {'passed':not errors, 'metrics':metrics, 'errors':errors,
            'limits':'Static integrity, collision and synthetic calculations only; not model quality, latency or token evaluation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hub', type=Path, help='Optional existing repository for read-only collision check')
    args = parser.parse_args()
    if args.hub is not None and not args.hub.is_dir():
        parser.error('--hub must be an existing repository directory')
    try:
        report = validate(ROOT, args.hub)
    except (OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
        report = {'passed':False, 'errors':[str(exc)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
