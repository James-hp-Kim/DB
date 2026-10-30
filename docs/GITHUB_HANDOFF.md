> 2026-10-31 지침 연결 수정 사본: 먼저 [AUTO_START_KO.md](../AUTO_START_KO.md)를 확인하세요. 기존의 수동 START 문구 안내보다 이 연결 절차를 우선합니다.

# GitHub 업로드 인수인계

현재 파일은 로컬에 준비되었고 GitHub 업로드는 수행하지 않았습니다.

이 폴더의 **내용 전체를 저장소 루트**에 놓습니다. 루트에 README.md, Install.ps1, .agents/, plugins/가 있어야 합니다. .agents/와 .codex-plugin/ 등 점으로 시작하는 폴더도 필요합니다. ZIP 파일 하나만 올리는 경우에는 웹에서 카드·정본을 직접 검색하거나 marketplace로 등록할 수 없으므로 압축을 푼 파일 구조를 업로드합니다.

포함: 코드·지침·공개 지식 정본·SQLite DB·Markdown 색인·라이선스·합성 예제·검증 스크립트.

제외: 실제 회사 원본·개인 DB·분석 결과·가상환경·캐시·인증 파일·API 키. 개인 DB는 저장소 밖에 두는 구조입니다. .gitignore도 함께 제공합니다.

## 새 PC

가장 쉬운 경로: GitHub Code → Download ZIP → 압축 해제 → START_HERE_KO.md → Codex/Python 확인 → Skill 설치. Git은 필요하지 않습니다.

Plugin 등록은 업로드 후 실제 저장소와 배포 태그를 사용합니다. 아래는 자리표시자입니다.

```powershell
codex plugin marketplace add James-hp-Kim/DB --ref main
codex plugin add expert-hub@expert-local
```

같은 버전을 쉽게 재현하도록 테스트한 태그/커밋으로 배포하는 편이 좋습니다. GitHub가 실행 서버가 되는 것은 아니며 MCP는 사용자 PC의 Python에서 동작합니다. 선택 Python 패키지는 PC마다 새로 설치합니다.

## 설치를 Codex에 맡기는 문장

```text
이 저장소의 START_HERE_KO.md를 읽고 Windows에서 사용할 수 있도록 확인해줘.
먼저 환경과 지식 DB를 검증한 뒤 Skill 단독 방식으로 설치해줘.
기존 expert Skill이 있으면 덮어쓰지 말고 버전 차이를 알려줘.
설치 후 품질보증 관점의 “불량률 분모” 검색과 필요한 절 조회를 확인해줘.
GitHub 업로드나 개인 자료 수집은 하지 마.
```

업로드 전/다운로드 후 `python -B -X utf8 scripts/verify_release.py`로 무결성을 확인합니다. 코드를 변경하거나 다시 빌드하면 체크섬을 새로 생성하고 새 배포 버전으로 검증하세요. 루트 docs를 가리키는 출처는 전체 저장소 사본에서 열 수 있습니다. Skill 단독 설치에서 그 문서가 필요하면 GitHub 저장소의 같은 상대 경로를 참고하세요.
