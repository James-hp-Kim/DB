# 반도체 AI 스킬 전문가 사용 안내

## Codex에 바로 요청하기

> 이 저장소의 expert Skill을 사용해 반도체 AI 스킬 전문가(semiconductor-ai)를 검색하고 선택해. 입력 파일은 [절대경로], 목적은 [증상/개선목표]야. reference-input으로 관련 주제만 추린 후 필요한 팩의 상위 2개 요약, 적용 조건과 한계만 조회해. 관측 사실·가설·대안·검증 방법·출처를 구분해서 답해. 자료 전체를 읽거나 DB 전체를 출력하지 마.

설치 전에도 저장소를 Codex 작업 폴더로 열고 위 요청을 사용할 수 있다. 자동 Skill 발견과 MCP 활성화는 설치/등록 후 새 대화에서 확인한다.

## 새 Windows PC

1. Codex와 Python 3.11 이상(SQLite FTS5 포함)을 설치한다. GitHub에서 ZIP을 받아 압축 해제하면 Git 설치는 필수가 아니다.
2. 저장소 루트에서 `python -B -X utf8 plugins/expert-hub/skills/expert/scripts/expert.py status`로 DB를 점검한다.
3. [설치 안내](../START_HERE_KO.md)의 Install.ps1로 Skill 또는 Plugin을 설치한다. MCP는 선택 구성이다. 이 배포 준비에서는 사용자 전역 설정을 변경하지 않았다.
4. 처음에는 `python -B -X utf8 plugins/expert-hub/skills/expert/scripts/expert.py catalog semiconductor-ai --limit 1`로 역할을 검색한다. 반환된 context를 후속 명령의 `--context`에 전달한다. 정확한 인수는 해당 명령의 `--help`를 확인한다.

검색은 Python 표준 라이브러리/SQLite만 사용하며 외부 벡터 서비스나 별도 API 키가 필요 없다. 실제 RTL 시뮬레이션·합성에는 Icarus/Verilator/Yosys 등 선택 도구가 별도로 필요하다. SPICE·물리 검증은 해당 도구와 모델/PDK/라이브러리가 필요하다. 설치만으로 signoff가 가능해지지 않는다.

## 데이터 구조와 입력

추가한 자료 102개: chip-review 17, chip-rtl 51, chip-memory 14, chip-analog 20. 정본은 각 packs/records.jsonl, 검색용 DB는 팩별 SQLite FTS5, 출처는 공유 sources.json/SQLite다. 요약/절/출처를 분리하므로 필요한 내용만 조회한다. 원문 전체와 과거 결과는 third_party/semiconductor-evidence-20261029.zip에 보존하고 일반 질문 때 자동 해제하지 않는다.

텍스트 입력은 최대 2 MiB이며 주제 키워드와 관련 행 번호만 노출한다. 파일 원문은 DB에 자동 저장하지 않는다. 이미지/PDF는 관련 화면/페이지를 별도 확인한다. 설계 파일 외에 목표 사양, PVT, 클록/리셋, 제약, 기존 테스트 결과가 있으면 함께 지정한다. 민감 자료는 공개 저장소 밖에 둔다.

조회 상한 예: 요약 2개/2000자, 적용 조건·한계 2400자. 부족하면 필요한 절만 다음 호출로 읽는다. 요약을 줄여 반례나 적용 조건을 숨기지 않는다. 문자 수·참고 tokenizer 결과는 전체 청구 토큰 절감률이 아니다.

## 근거 범위

이 대화에서 수집한 2026-10-29 공개 자료와 실험을 가져왔다. 이번 통합은 전체 웹 원문을 새로 재감사하지 않았다. 공개 PicoRV32의 알려진 변이 6종에 대한 탐지·수정 실험은 범위가 제한되고 비맹검이며, 일반 칩 진단 정확도/전문가 동등성/실제 실리콘 개선 효과로 일반화할 수 없다. 자체 작성 지침과 공식 출처·실험 근거의 등급은 레코드에서 구분한다.

GitHub 업로드는 하지 않았다. 저장소를 업로드할 때는 README와 THIRD_PARTY_NOTICES의 라이선스 및 외부자료 범위를 유지한다.
