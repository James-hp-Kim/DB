# Skill·MCP·Plugin의 역할

ID: `common:skill-mcp-plugin` | both | reference-only

Skill은 작업 지침, MCP는 기능·자료를 연결하는 프로토콜/도구, Plugin은 배포 묶음이다. 이 허브의 MCP는 지식 조회를 제공하며 파일 존재와 실제 활성화를 구분한다.

## procedure

expert Skill 하나가 페르소나와 quick/deep 트랙을 선택한다. 통계·원본 보존 등 공통 지식은 한 번 저장하고 역할별로 참조한다.
이 허브의 MCP 도구는 expert_catalog, expert_lookup, expert_read, expert_source, expert_reference_input 다섯 개다. 마지막 도구는 지정 입력의 주제 단서와 범위 내 참고 근거를 반환하며 결함 판정은 아니다. 지식은 읽기 전용이고 catalog는 선택 영수증만 기록한다. 분석·수집·DB 수정은 로컬 CLI에서만 수행한다.
Plugin은 expert Skill과 MCP를 함께 배포한다. Skill 단독은 동일 CLI 검색을 이용하므로 MCP는 필수가 아니다.

## limits

사용자 Skill 설치와 Plugin 설치를 중복하지 않는다. 페르소나는 논리적 검색 범위를 선택하며 OS 계정 수준의 보안 경계를 대신하지 않는다.
GitHub는 정본·배포 파일 보관소다. SQLite 검색과 MCP는 내려받은 PC의 Python에서 실행한다. 일반 MCP 서버는 쓰기 기능을 가질 수 있다. 이 허브의 읽기 전용 특성을 모든 MCP에 일반화하지 않는다.

## interpretation

SKILL.md 포함, MCP 선언/구현, 플러그인 명세, 후보 언급, 실제 설치·연결·사용을 별도로 기록한다. 같은 명세의 복제본은 독립 증거로 세지 않는다. 이름이 같아도 출처·버전·본문이 다르면 구분한다.

## 출처

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) · primary · 확인 2026-10-29
- [OpenAI: Package your plugin](https://developers.openai.com/plugins/build/plugins) · primary · 확인 2026-10-29
- [MCP: stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) · primary · 확인 2026-10-29
- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
