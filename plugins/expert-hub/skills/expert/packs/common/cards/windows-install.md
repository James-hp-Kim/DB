# Windows 새 PC 설치 항목

ID: `common:windows-install` | both | reference-only

기본 사용은 Codex와 Python 3.11+만 필요하다. Git·MCP 등록·분석 패키지는 사용 방식에 따라 선택한다.

## conditions

GitHub 문서는 웹에서 읽고, 실행은 ZIP을 내려받아 Windows에서 한다. ZIP 방식에는 Git 설치가 필요 없다.
기본 검색·CSV 분석은 Codex와 Python 3.11+ 및 SQLite FTS5를 사용한다. 별도 API 키·벡터 DB·서버가 필요 없다.
Skill은 Install.ps1로 설치한다. Plugin 또는 MCP 등록 명령을 사용하려면 Codex CLI가 필요하다.
Excel은 openpyxl, 다변량 탐지는 PyOD를 선택 설치한다. 설치한 Python과 실제 실행 Python을 맞춘다.

## limits

MCP는 지식을 읽기 전용으로 조회한다. catalog는 로컬 선택 영수증만 기록한다. Codex 질문·결과의 서비스 전송까지 오프라인이라는 뜻은 아니다.

## procedure

처음에는 START_HERE_KO.md와 Test-Environment.ps1을 사용한다. 이번 배포 작업은 사용자의 전역 Codex 설정에 자동 설치하지 않는다.

## 출처

- [OpenAI: Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference) · primary · 확인 2026-10-29
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) · primary · 확인 2026-10-29
- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
