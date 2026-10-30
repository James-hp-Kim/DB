# 토큰 절약: 검색·선별·계산·재사용

ID: `common:token-strategy` | both | bounded search/get + result cache

짧은 스킬 1개, 검색 후 필요한 카드만 읽기, 원본은 코드로 계산, 동일 입력은 결과 캐시를 재사용한다.

## procedure

진입 Skill을 읽고 catalog로 필요한 페르소나만 검색한다. 선택 context는 24시간 재사용한다. 선택한 역할은 lookup 응답에 포함되며 모든 역할의 장문을 읽지 않는다.
lookup 기본 3건 요약 후 read로 관련 항목 1~2개와 필요한 절만 연다. deep도 당면 쟁점부터 확장한다.
CSV/XLSX 원시 행은 로컬에서 계산하고 제한된 요약·근거 위치만 대화로 전달한다. 전체 결과는 파일에 보존한다.

## verification

같은 입력 SHA-256·옵션·도구 버전이면 분석 결과를 재사용한다. DB 자료가 바뀌면 기존 근거를 다시 확인한다.

## limits

출력 길이 제한은 JSON 문자 수이며 실제 모델 토큰 상한이 아니다. 근거·반례·적용 한계를 생략해 결론을 왜곡하지 않는다.
검색 카드·절의 텍스트 토큰량과 실제 대화·추론·도구 전체 사용량을 구분한다. 다중 에이전트를 기본 경로에 넣지 않는다.

## 출처

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) · primary · 확인 2026-10-29
- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
