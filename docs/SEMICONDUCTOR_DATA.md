# 반도체기초전문가 — 입력과 최소 조회

이 허브의 `semiconductor-basics`는 반도체 물리·소자·회로·제조·메모리·패키지를 연결하는 판단 관점입니다. 별도 모델이나 전문가 자격이 아닙니다. 기본 팩은 `semiconductor`이며 통계는 `common`, NAND 제어·ECC 심화는 `nand`를 명시적으로 추가합니다. 다른 팩 전체를 자동으로 읽지 않습니다.

## 무엇이 들어 있는가

2026-10-29에 작성한 공개 연구 패키지에서 기초 장 20개, 발표 수치 36건, 최적화 후보 26개, 미실행 실험안 15개, 입력 필드 37개, 직무 탐색 제안 10개, 교육용 계산식 8개를 이관했습니다. 총 152개 중 실패 0건의 이항 상한 계산식은 공통 팩에 1회 저장하고, 151개를 반도체 팩에 저장했습니다. 원본의 출처 카드 33개는 본문으로 중복 저장하지 않고 기존 출처 레지스트리와 URL 기준으로 통합했습니다.

반도체 물리, PN 접합, MOSFET·CMOS, SRAM·DRAM·NAND, HBM, IGZO, 누설 기전, 전력·면적 상충관계, 제조 공정, 실험·신뢰성·직무 학습을 다룹니다. 통계의 공통 절차는 `common:doe`, `common:data-contract`, `common:rate-interval`을 재사용합니다.

이관 대응표와 입력 파일 SHA-256은 [SEMICONDUCTOR_IMPORT.json](SEMICONDUCTOR_IMPORT.json)에 있습니다. `reviewed`는 원본 연구 기준일이며 이관일의 웹 재확인 날짜가 아닙니다. 원문 접근 제한, 세대·조건 제한은 출처 메타데이터와 항목의 `limits`에 남아 있습니다. 원문 논문 전체, 사내 PDK, 생산 규격, 실제 측정 데이터는 포함하지 않습니다. 학습 일정과 필드 정의는 작성자의 제안입니다.

## Codex에 그대로 입력

```text
$expert 반도체기초전문가 관점에서 첨부 자료를 검토해줘.
먼저 expert_catalog에서 '반도체기초전문가'를 검색하고 반환된 context를 재사용해.
기본 semiconductor 팩에서 관련 요약 최대 3건을 찾고,
필요한 1~2건의 conditions와 limits를 먼저 읽어.
원인 구분에 필요한 procedure 또는 verification만 추가해.
관찰 사실 / 원인 가설 / 개선 후보와 부작용 / 필요한 추가 데이터 / 근거 ID 순으로 짧게 답해.
원시 데이터 전체를 대화에 출력하거나 지식 DB에 자동 저장하지 마.
```

기존 설치본에는 새 팩이 자동 동기화되지 않습니다. 현재 저장소를 연 경우 `plugins/expert-hub/skills/expert/SKILL.md`를 읽도록 요청하면 설치 없이 이 복사본을 사용할 수 있습니다. 개인 Skill 설치는 [시작 안내](../START_HERE_KO.md)를 따릅니다. 설치 스크립트는 기존 설치를 덮어쓰지 않습니다.

## 어떤 자료를 주면 좋은가

| 질문 | 최소 입력 | 필요한 경우 추가 | 처음 찾을 키워드 |
|---|---|---|---|
| 누설전류가 커졌다 | 소자/회로 구분, Id/Ig/Ib/Ioff 중 측정량, 단위, Vgs/Vds/Vbs, 온도, baseline | W/L, 계측 바닥, settle time, guard, sweep 방향, 공정 코너 | 누설전류, GIDL, 단일 소자 누설 분해 |
| DRAM retention이 나쁘다 | 제품·구조, 온도, 전압, 대기시간, 패턴, 실패수/시험수 | 셀 위치, 반복 시점, VRT, Ccell/Cbl, refresh 조건 | DRAM, retention, 셀 누설 예산 |
| NAND 오류율이 높다 | 세대, P/E, 보존시간, 온도 이력, page/layer, raw/ECC 후 구분 | Vref, retry, code/rate, 분모, read 횟수 | NAND, retention, 오류율 |
| HBM 전력·열 문제 | 세대, 스택 구성, 대역폭·활동률, 전압, 온도 위치 | pJ/bit의 포함 범위, 열 경계, 패키지·보드 조건 | HBM, 열, 대역폭 |
| 면적·전력을 줄이고 싶다 | 변경 블록, 기존 구조, 목표, 유지할 지연·속도·오류 한계 | PVT, workload, 셀 라이브러리, IR drop, EM, wake-up 비용 | high-Vt, power gating, 자원 공유 |
| 직무를 탐색하고 싶다 | 관심 직무나 모르는 개념, 학습 목적 | 현재 지식·시간 | 소자 개발, 회로 설계, 학습 순서 |

값이 없으면 `null` 또는 '미확보'로 표시합니다. 누설 A와 A/µm, raw BER과 ECC 후 오류율, Gb와 GB, bit와 die의 시험 분모를 섞지 않습니다. 검출한계 미만은 0으로 대입하지 않습니다. 보고서·CSV·JSON·RTL·타이밍 리포트를 주어도 읽을 수 있는 범위가 다르며, 이 팩 자체에는 TCAD/SPICE/STA 실행기가 없습니다.

합성 입력 예시: [semiconductor_input.example.json](../examples/semiconductor_input.example.json). 실제 회사 파일은 이 공개 저장소 밖에 둡니다. 사용자가 자료를 준 것은 조회·분석 요청이며 영구 지식 등록 허가는 아닙니다.

## PowerShell에서 확인

저장소 루트에서 실행합니다. `python`은 Python 3.11 이상과 SQLite FTS5를 제공해야 합니다. 조회는 표준 라이브러리만 사용하므로 별도 API 키·벡터 DB·클라우드 서버가 필요하지 않습니다.

```powershell
$picked = & .\expert.ps1 catalog '반도체기초전문가' --limit 1 | ConvertFrom-Json
$ctx = $picked.personas[0].context
& .\expert.ps1 lookup '단일 소자 누설 분해' --context $ctx --limit 3 --max-chars 2000
& .\expert.ps1 read semiconductor:e01 --context $ctx --sections conditions limits --max-chars 2000
& .\expert.ps1 read semiconductor:e01 --context $ctx --sections procedure verification --max-chars 2000
# lookup/read에 반환된 sources 중 필요한 ID로 source 명령을 호출한다.
# 통계가 필요한 경우에만 같은 context로 --packs common 을 지정한다.
& .\expert.ps1 read common:zero-failure-upper --context $ctx --packs common --sections conditions procedure limits
```

## 토큰을 줄이는 동작

1. 처음 한 번 페르소나를 선택하고 context를 재사용합니다. 등록부 변경·이동·24시간 만료 후에는 다시 선택합니다.
2. 질문의 대상·증상·조건에서 검색어 2~5개를 만듭니다. 첫 검색은 최대 3개 요약이며 전체 본문을 반환하지 않습니다.
3. 필요한 1~2개 ID의 조건·한계를 읽은 뒤, 가설을 구분할 절만 추가합니다. `next_offset`이 있으면 해당 절의 다음 부분만 읽습니다.
4. 원시 행은 로컬 계산에 사용하고 대화에는 행 수·분모·단위·결과와 파일 위치만 전달합니다. 숫자 조건과 반대 근거를 절약 대상으로 잘라내지 않습니다.
5. 출처는 필요할 때만 가져옵니다. 반복 질문에서 이미 읽은 동일 근거를 재출력하지 않습니다.

기본 JSON 문자 상한은 lookup 3,500, read 6,000, source 5,000입니다. 문자 수와 모델 토큰 수는 다릅니다. 페르소나 명칭만으로 토큰 절약이 생기지 않으며, 팩 범위·짧은 요약·절 선택·context 재사용이 실제 전달량을 제한합니다. 실제 과금 절감률은 보장하지 않습니다.

## 적용 경계

제조사 발표값은 해당 제품·발표 시점의 값입니다. 연구용 IGZO의 최선 retention과 가장 작은 gate 길이의 결과를 같은 소자로 합치지 않습니다. 교육용 64 ms, 20 fF, 90 mV/dec 등은 예시 입력이며 사내 기준이 아닙니다. 이 팩은 누설 원인과 설계 대안을 검토할 근거를 제공하지만 양산 설계 승인이나 실리콘 성능을 증명하지 않습니다.

## 파일에서 바로 DB 근거 찾기

위 PowerShell 예제에서 확보한 `$ctx`를 사용합니다. UTF-8 파일 최대 2 MiB를 로컬에서 읽고 주제별 행 위치와 요약만 반환합니다. 수치 판독·진단은 별도 단계입니다.

```powershell
python -B -X utf8 plugins/expert-hub/skills/expert/scripts/semiconductor_reference.py examples/semiconductor_input.example.json --context $ctx --max-chars 2500
```

이 전용 보조 명령은 Skill에서 사용합니다. MCP에서는 기존 expert_catalog → expert_lookup → expert_read → expert_source로 같은 팩을 조회합니다. 다른 도메인의 expert_reference_input과 혼동하지 마세요.
