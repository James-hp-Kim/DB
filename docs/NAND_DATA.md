# NAND 전문가에게 자료를 주는 방법

이 저장소를 Codex의 작업 폴더로 열고 다음처럼 요청하세요. 별도 페르소나 앱이나 모델을 설치하지 않습니다. expert 진입 skill과 기존 조회 도구를 사용합니다.

```text
이 폴더의 plugins/expert-hub/skills/expert/SKILL.md를 읽어.
너는 NAND 제어·인터페이스·ECC RTL 전문가 관점으로 검토해.
첨부 자료에서 판단에 필요한 조건과 증상만 추려 NAND DB를 조회해.
상위 3개 요약 → 필요한 조건/한계 → 검증 절 → 출처 순서로 읽고,
결론·근거 ID·추가로 필요한 자료만 먼저 알려줘.
```

페르소나는 검토 관점입니다. 전문성을 보증하거나 토큰을 자동으로 줄이는 장치가 아닙니다. 실제 전달량을 줄이는 부분은 팩 범위, 짧은 검색 결과, 절 선택, 결과 재사용입니다.

## 어떤 자료를 주면 되는가

|입력|처음 주면 좋은 정보|주요 조회 후보|
|---|---|---|
|현상·개선 질문|관심 블록, 증상, 목표, 제품 revision, 이미 확인한 것|input-contract, V*, E*|
|RTL 일부·검증 로그|문제 module/FSM, clock/reset, interface 계약, 재현 조건, 첫 실패 위치|CDC V08, RDC V09, FIFO V10, ECC V13–V16|
|retry/latency CSV|행 단위, read ID, baseline/후보, retry count, 단계별 시간, P/E·retention·온도|P01/P12, V12, E01, D_*|
|ECC 결과 표|H/code hash, K/N/rate, LLR 정의, iteration cap, 시험/실패 codeword, payload truth|P04, V13–V16, D_*|
|논문/규격 발췌|제목·URL·버전·관련 절과 원하는 비교|P*/S*, conditions/interpretation/limits|

P01 등은 이전 조사 ID이며, 새 허브의 정식 ID는 `nand:p01`입니다. 필드 ID는 예를 들어 `nand:d-raw-bits-compared`입니다. 숫자가 없는 항목은 미확보로 남깁니다. 필요한 정보를 한 번에 모두 요구하지 않고, 현재 결론에 영향을 주는 누락만 확인합니다.

CSV·텍스트·SystemVerilog 파일은 필요한 열/행/블록만 로컬에서 읽습니다. `expert_reference_input`은 사용자 지정 UTF-8 파일(최대 2 MiB)의 키워드와 행 위치만 추려 NAND 근거를 연결합니다. 원본 행을 반환하거나 저장하지 않으며 RTL 의미 분석기·불량 판정기는 아닙니다. Excel/PDF/파형은 환경에 맞는 도구가 있어야 내용을 추출할 수 있습니다. 기존 CSV 분석 기능의 단위·분모가 NAND 로그와 맞는지도 먼저 확인해야 합니다.

## 최소 입력 양식

```text
목적: retry가 늘어난 원인을 좁히고 RTL 검증안을 만들고 싶음
대상: [공개 가능한 NAND revision/인터페이스/관심 블록]
자료: [저장소 밖 파일 경로 또는 첨부]
행 단위·기간·단위: [예: host read 1건, ns, 동일 workload]
비교: [baseline/후보, 차이가 있는 설정]
증상·기존 확인: [관찰된 사실만]
미확보: [모르는 제품 조건·H matrix·온도 이력 등]
출력: 결론 3줄 + 근거 ID + 검증 항목 + 추가 자료
```

개인·업무자료는 공개 저장소 밖에 두세요. 질문에 첨부한 자료는 판단 입력이며 자동 DB 등록 대상이 아닙니다. 명시적인 저장 요청이 있을 때만 기존 private ingestion 절차를 적용합니다.

## 실제 조회 순서

MCP 이름은 expert_catalog, expert_lookup, expert_read, expert_source입니다. 설치 방식에 따라 도구 이름 접두어가 붙을 수 있습니다. 아래 명령은 저장소 루트 PowerShell에서 실행합니다.

```powershell
$expertCli = 'plugins/expert-hub/skills/expert/scripts/expert.py'
$found = python -B -X utf8 $expertCli catalog NAND --limit 1 | ConvertFrom-Json
$nandContext = $found.personas[0].context
python -B -X utf8 $expertCli lookup 'retry epoch' --context $nandContext --limit 3 --max-chars 2400
python -B -X utf8 $expertCli read nand:v12 --context $nandContext --sections conditions limits --max-chars 2400
python -B -X utf8 $expertCli read nand:v12 --context $nandContext --sections verification --max-chars 2400
```

검색 결과가 NAND 역할인지 먼저 확인합니다. 출처는 조회 결과의 sources ID만 사용합니다. 예를 들어 P01 원문 정보를 확인하려면:

```powershell
python -B -X utf8 $expertCli source nand-p01 --context $nandContext --max-chars 1800
```

통계 지침이 필요하면 `--packs common`을 명시합니다. NAND 기본 조회에는 common도 자동으로 섞이지 않습니다. 품질팩은 이 역할의 허용 범위에 없으며, 품질 관점으로 바꾸려면 해당 페르소나를 별도 검색합니다.

## 파일을 주고 관련 근거 찾기

```powershell
python -B -X utf8 $expertCli reference-input 'C:\NAND-work\retry.log' --context $nandContext --max-chars 2400
```

경로는 사용자가 준 실제 파일로 바꿉니다. MCP에서는 `expert_reference_input(file=실제경로, context=선택키, max_chars=2400)`를 사용합니다. 주제를 못 찾으면 `--query 'LLR 포화'`처럼 목적을 좁히세요. 지원 확장자는 .sv/.svh/.v/.sdc/.upf/.log/.rpt/.csv/.json/.md/.txt입니다. 키워드가 없으면 gap을 반환하며 전체 DB를 대신 읽지 않습니다. 이 함수는 행 단위 수치 분석·데이터 유효성 검사를 수행하지 않습니다.

## 전달량 제한

- 검색: 기본 3건, 전체 JSON 상한 3,500자. 단순 질문은 위 예처럼 2,400자로 좁힐 수 있습니다.
- 상세: 기본 6,000자. 한 ID의 필요한 1~3개 절만 요청합니다. limits/conditions를 자르고 적용을 확정하지 않습니다.
- 잘린 내용: next_offset으로 같은 ID·절의 나머지만 읽습니다. 출처의 omitted_ids도 확인합니다.
- 같은 context와 이미 읽은 근거는 대화 안에서 재사용합니다. context는 24시간 또는 등록부/경로 변경 시까지입니다.
- 대량 로그 전체, 전체 카드, 모든 출처를 응답에 넣지 않습니다. 로컬 집계와 대표 오류 행만 사용합니다.

실제 모델 토큰·비용은 질문/첨부/추론/답변에도 영향을 받습니다. [전달량 시험](NAND_VALIDATION.md)은 고정 질문의 조회 텍스트만 비교하며 전체 과금 절감률을 보장하지 않습니다.
