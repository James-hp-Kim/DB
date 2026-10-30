# 짧고 검증 가능한 결과 형식

ID: `common:review-output` | quick | reference-only

핵심 결론과 근거·한계를 먼저 제시한다. 짧게 쓰더라도 부정어·단위·숫자·식별자와 불확실성은 보존한다.

## procedure

Quick 권장: 핵심 판단 1문장 + 문제/근거/다음 조치 표. 불량률은 건수와 분모를 병기한다.
Deep 권장: 우선순위 3~5개 + 증거/가설 상태/검증 계획 + 재현 가능한 결과 파일. 세부 계산은 파일에 보관한다. 형식을 의무화하지 않고 질문에 필요한 길이로 작성한다. 코드·경로·오류 메시지·숫자·단위·부정어를 압축 과정에서 바꾸지 않는다. 설명은 자연스러운 한국어로 짧게 쓴다. 한 단계에는 한 동작을 둔다. 용어를 일관되게 쓰고 조건을 동작보다 먼저 제시한다. ASD-STE100 원칙을 느슨하게 참고하며 80% 준수를 측정했다고 표현하지 않는다.

## interpretation

관측 사실, 통계적 후보, 원인 가설, 검증된 원인을 구분한다. 판정 불가도 유용한 결과다.
예시 숫자와 실측 숫자를 섞지 않는다. 자료의 범위·누락·미검증 가정을 짧게 명시한다.

## limits

단순한 질문에 전체 기법 설명과 모든 정의를 반복하지 않는다. 사용자가 요청하면 깊이를 늘린다.

## 출처

- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
- [cofa-concise — 공개 준비 지침의 일반 절차](https://github.com/arcturus0637-rgb/cofa-prelim-kit/blob/28479b0820c3933c7d2aa5aa9efb529577a7e593/skills/cofa-concise/SKILL.md) · public-preparation-guidance · 확인 2026-10-30
- [caveman 선택 절차의 공개 근거](https://github.com/JuliusBrussee/caveman/blob/9b68f7ed12b05e7efaff18e65c5a3fc2849fd0a4/skills/caveman/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
