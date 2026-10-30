# 자동 지침 연결 — 2026-10-31 검증 사본

- 이 사본은 Expert Hub 2.5.2에 지침 진입 연결을 추가했다. 새 공식 버전을 주장하지 않는다.
- 저장소를 내려받은 뒤 PowerShell에서 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Start-Exam.ps1`을 실행한다.
- 실행 모델은 `gpt-6.1-sol`이다. Codex 로그인과 해당 모델 사용 권한은 필요하다.
- 저장소 루트의 AGENTS.md가 supplements/prompt-workflow-kit-20261030/exam-kit/START.md를 첫 답변 전에 읽도록 연결한다. 문제마다 시작 문구를 붙이지 않는다.
- 다른 폴더에서도 적용하려면 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install-Instructions.ps1`을 한 번 실행하고 새 Codex 대화를 시작한다. 기존 전역 지침이나 override가 있으면 덮어쓰지 않는다.
- 저장소 폴더를 옮기면 전역 연결 경로도 다시 설정해야 한다.
- GitHub URL을 채팅에 붙이는 것만으로 다운로드·전역 설치가 완료되지는 않는다. 저장소를 로컬 작업 폴더로 여는 단계가 필요하다.
- 이 진입 연결은 스킬/MCP/플러그인 설치와 별개다. DB는 기존 expert Skill의 CLI 경로로 사용할 수 있다. 필요할 때 기존 설치 안내로 MCP 또는 Plugin을 선택한다.
- supplements 내부의 과거 검증·안내 문서는 당시 기록이다. 현재 진입 방식과 검증 상태는 이 안내와 별도 검증 보고서를 따른다.
- 한국어 설명에 ASD-STE100의 명료성 원칙을 참고한다. 영어 표준의 정식 적합성 인증을 뜻하지 않는다.

