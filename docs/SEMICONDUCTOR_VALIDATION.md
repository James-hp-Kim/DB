# 반도체 기초팩 검증 — 2026-10-30

## 확인한 범위

| 검사 | 결과 |
|---|---|
| 반도체 전용 회귀 | 8개 통과: 이관 대응, 조건·한계·출처, 범위 제한, 문자 예산, 파일 비노출, 입력 예외, CLI/MCP 동일 조회 |
| 고정 한영 검색 | 9개 질문에서 기대 ID가 상위 3개에 포함 |
| 공통 허브 회귀 | 별도 복사본에서 16개 통과 |
| 페르소나 게이트 | 별도 복사본에서 8개 통과 |
| 공식 MCP SDK stdio | 검색→요약→선택 절→출처, 범위 밖 접근 거절 통과 |
| 기본 의존성 | Python -S(site-packages 비활성)에서 catalog 및 합성 JSON 파일 조회 통과; 반환 1,636자 |
| Skill 형식 | skill-creator quick_validate 통과 |

Windows에서 Python 3.14.7(기본 회귀), Python 3.12.14 + MCP SDK 2.3.0(stdio), PyYAML 6.0.3(형식), tiktoken 0.14.0(참고 측정)을 사용했습니다. 한글·공백 경로를 포함합니다. 검증용 라이브러리는 사용자 기본 조회의 필수 의존성이 아닙니다.

공유 폴더가 동시에 갱신되어 정본과 DB 해시가 일시적으로 어긋난 상태에서의 전체 검사가 실패했습니다. 별도 검증 복사본에서 모든 DB를 재생성하고 당시 항목 수(760)를 명시적 release inventory에 반영한 뒤 공통 검사 16개가 통과했습니다. 최종 공유 배포본의 전체 팩·manifest 검증은 통합 담당 작업에서 다시 수행해야 합니다. 이 문서는 다른 팩의 전문 내용이나 전체 배포 승인까지 증명하지 않습니다.

## 참고 토큰 측정

동일 진입 Skill을 포함하고, 반도체 팩 전체 JSONL과 필요한 부분 조회를 비교했습니다. 각 예시에 페르소나 검색 1회, 최대 3개 요약, 선택 ID의 conditions/limits, 해당 출처 메타데이터를 포함합니다.

- 전체 반도체 팩 + 진입 Skill: **54,501 토큰**
- 선택 조회 + 진입 Skill: **2,162~2,428 토큰**
- 고정 4사례에서 참고 텍스트 기준 **95.5~96.0% 감소**

측정 원본: [SEMICONDUCTOR_BENCHMARK.json](SEMICONDUCTOR_BENCHMARK.json). o200k_base tokenizer이며 실제 Codex 모델의 과금·추론 토큰을 측정한 것이 아닙니다. 사용자 입력·원시 데이터·도구 정의·프로토콜·추론·답변·재시도·추가 팩은 제외했습니다. 선택 ID를 미리 정한 예시 비교이며 일반 검색 정확도나 실사용 절감률을 보장하지 않습니다. 측정 당시 Skill/팩 SHA-256을 기록했으며 이후 통합으로 진입 Skill이 바뀌면 다시 측정해야 합니다.

## 재현

```powershell
python -B -X utf8 scripts/build_knowledge.py
python -B -X utf8 -m unittest discover -s tests -p test_semiconductor.py -v
python -B -X utf8 tests/benchmark_semiconductor.py
# 공식 MCP SDK가 설치된 검증용 가상환경에서:
python -B -X utf8 tests/test_semiconductor_mcp_sdk.py
```

이관 범위는 반도체 151건 + 공통 계산식 1건이며 [대응표](SEMICONDUCTOR_IMPORT.json)로 원본 비출처 152건을 모두 추적합니다. 출처 33건은 기존 URL과 통합했습니다. 새로운 원문 웹 검토, fab/EDA 실행, 실리콘 측정, 회사 데이터 분석, 인증된 Codex 대화에서의 자동 페르소나 선택은 이번 이관에서 수행하지 않았습니다. 사용자 설정 변경과 GitHub 업로드도 하지 않았습니다.
