# 공개 후보 평가: PyOD od-expert

ID: `quality:pyod-assessment` | both | reference-only

이상탐지 실행 도구와 연결되지만 원본 스킬의 설정 문법·Codex 경로 안내를 그대로 쓰지 않는다.

## limits

원본 SKILL.md description 문자열 안의 콜론 뒤 공백이 YAML 파싱 오류를 만든다. 보관본 검증에서 이 오류를 확인한다.
원본 설치 문서의 ./skills 경로/사용자 전역 경로 설명은 현재 Codex 공식 문서와 다르다. 이 패키지 설치기는 공식 발견 경로 또는 Plugin marketplace를 사용한다.
여러 탐지기의 동의는 정답 근거가 아니다. 후보 검토, 실제 불량 판정, 원인 확정을 각각 구분한다.

## procedure

전체 autonomous 탐색/반복 루프 대신 필요한 수치 분석만 고정된 classic API로 실행해 읽기와 불필요한 모델 비교를 줄인다.

## conditions

PyOD는 선택 의존성이다. 기본 지식 검색과 quick 분석은 PyOD 설치 없이 작동한다.

## 출처

- [yzhao062/pyod: pyod/skills/od_expert/SKILL.md](https://github.com/yzhao062/pyod/blob/7e1330e10ac5c56ed402fbbaa41b225efb4bbc5c/pyod/skills/od_expert/SKILL.md) · community-source · 확인 2026-10-29
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) · primary · 확인 2026-10-29
- [scikit-learn: Novelty and outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html) · primary · 확인 2026-10-29
