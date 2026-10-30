"""Read one opt-in method. Flags declare consent, not independent authentication."""
import argparse
import json
from pathlib import Path
import knowledge as kb

ROOT = Path(__file__).resolve().parents[1]


def catalog():
    return json.loads((ROOT/'references/optional-methods.json').read_text(encoding='utf-8'))


def choices():
    return [{k: row[k] for k in ('name','function','complex_only')} for row in catalog().values()]


def read(name, context, approved=False, complex_problem=False):
    kb.scope(context)
    if approved is not True:
        raise ValueError('사용 동의가 필요합니다. 목적·범위·종료 조건을 알리고 답을 기다리세요.')
    rows = catalog()
    if name not in rows:
        raise ValueError('알 수 없는 방법입니다. list로 이름을 확인하세요.')
    requested = name
    name = rows[name].get('alias_of', name)
    row = rows[name]
    if row['complex_only'] and complex_problem is not True:
        raise ValueError('사용자가 복잡한 문제라고 표현한 경우에만 이 심화 방법을 사용할 수 있습니다.')
    return {'requested':requested, **row,
            'consent_limit':'Caller declaration only; not proof of human approval.',
            'execution_status':'Instructions returned; no upstream tool executed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    sub.add_parser('list')
    cmd = sub.add_parser('read')
    cmd.add_argument('name')
    cmd.add_argument('--context',required=True)
    cmd.add_argument('--approved',action='store_true')
    cmd.add_argument('--complex',dest='complex_problem',action='store_true')
    args = vars(parser.parse_args()); command = args.pop('command')
    try:
        result = choices() if command=='list' else read(**args)
        print(json.dumps(result,ensure_ascii=False,separators=(',',':')))
    except (ValueError,OSError) as exc:
        print(json.dumps({'error':str(exc)},ensure_ascii=False))
        return 2
    return 0


if __name__=='__main__':raise SystemExit(main())
