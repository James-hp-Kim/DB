"""Resolve a readable policy guide; returning it never asserts model compliance."""
import hashlib
import os
from pathlib import Path


def policy(root):
    installed = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex') / 'skills/fact-grounding/SKILL.md'
    candidates = [(installed, 'installed-skill'), (Path(root) / 'references/fact-grounding.md', 'bundled-snapshot')]
    for path, origin in candidates:
        try:
            content = path.read_bytes()
            if not content.decode('utf-8-sig').strip():
                continue
        except (OSError, UnicodeError):
            continue
        return {
            'skill': 'fact-grounding',
            'expert_guide': str((Path(root)/'SKILL.md').resolve()),
            'optional_methods': 'Default off. Ask before optional skills/MCP use. Complex-only methods require explicit complex wording AND approval. See expert SKILL optional methods.',
            'guide': str(path.resolve()),
            'sha256': hashlib.sha256(content).hexdigest(),
            'origin': origin,
            'instruction': '사실 조사·분석·비교·실행 보고 전에 이 지침을 읽고 적용한다. 현재 작업에서 이미 읽은 유효한 버전은 재사용한다. 사실·추론·미확인을 구분하고 핵심 주장에 근거 위치와 확인 시점을 제시한다. 동봉 사본 사용 시 그 한계를 밝힌다.',
            'enforcement': 'instruction-only; guide resolution is not proof of reading, compliance or correctness',
        }
    raise FileNotFoundError('fact-grounding guide unavailable: restore the installed skill or bundled reference')
