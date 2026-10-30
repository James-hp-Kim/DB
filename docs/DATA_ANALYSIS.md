# 빅데이터·매출·시계열 분석 사용법

추가 분야: `analytics` 10개, `sales` 14개. 기존 공통 통계와 품질 지식을 복사하지 않고 공유합니다.
지식 DB는 분석 방법과 출처를 보관합니다. 사용자가 제공하는 업무 데이터는 별도 로컬 파일로 분석하며 자동 저장·업로드하지 않습니다.

## Codex에 그대로 요청하기

```text
이 프로젝트의 expert 스킬을 사용해 빅데이터·데이터 분석 전문가 관점으로 분석해줘.
내 데이터의 경로는 [파일 경로], 목적은 [현황 비교/매출 예측/모델 개선]이야.
전체 원시 행을 대화에 넣지 말고 필요한 열의 로컬 프로파일부터 확인해.
페르소나 검색에서 받은 context로 관련 팩의 요약 3개 이내를 찾고,
적용 조건·절차·한계 중 필요한 절만 조회해. 같은 근거는 다시 읽지 마.
분모·기간·집계 단위가 불명확하면 먼저 근거를 확인해.
예측이라면 개발 백테스트와 최종 홀드아웃을 분리해.
전체 계산은 로컬 파일에 남기고 핵심 결과·근거 ID·미확인 사항만 알려줘.
```

이 저장소를 Codex 작업 폴더로 열면 AGENTS.md가 스킬 진입점을 안내합니다. 다른 프로젝트에서 자동 선택하려면 START_HERE_KO.md의 설치 절차를 사용합니다. 이 확장 작업은 전역 설치를 수행하지 않습니다.

## 어떤 데이터를 줄 수 있나

|입력|처리 경로|주의|
|---|---|---|
|CSV|`profile`로 선택 열과 앞부분을 순차 요약|기본 100000행; 전체 통계로 확대하지 않음|
|XLSX|기존 convert_xlsx.py로 필요한 시트만 로컬 CSV 변환 후 profile|openpyxl 선택 설치; 수식/캐시값 상태 확인|
|Parquet·SQL|질문에 필요한 열·기간만 로컬 조회 후 요약|DuckDB/Polars 등 선택 설치·별도 코드 필요|
|PDF·문서·이미지|관련 페이지·표를 추출하고 원문 위치를 붙여 검토|자동 범용 문서 변환기는 미포함|

파일만으로 매출 의미·단위·통화를 확정하지 않습니다. 목적, 대상 금액/수량, 시점 열, 품목/고객 단위, 예측기간을 알 수 있으면 함께 제공하세요. 실제 자료는 저장소 밖에 두세요.

## 설치 없이 시작하는 조회 예시

저장소 루트의 PowerShell에서 실행합니다. Python 3.11+가 필요하며 이 경로는 표준 라이브러리만 사용합니다.

```powershell
$cli = '.\plugins\expert-hub\skills\expert\scripts\expert.py'
$choices = python -B -X utf8 $cli catalog '빅데이터' --limit 1 | ConvertFrom-Json
$choices.personas  # 역할을 확인하고 선택
$ctx = $choices.personas[0].context

# 공개 합성 예제. 회사 파일을 쓸 때는 경로와 열 이름을 바꿉니다.
python -B -X utf8 $cli profile '.\plugins\expert-hub\skills\expert\examples\synthetic-monthly.csv' --columns unique_id ds y --date-column ds --task forecast
python -B -X utf8 $cli lookup '백테스트' --context $ctx --packs sales --limit 3 --max-chars 2500
python -B -X utf8 $cli read sales:backtest --context $ctx --packs sales --sections conditions procedure limits --max-chars 3000
python -B -X utf8 $cli source da-fpp --context $ctx --packs sales
```

`profile`는 실제 지식 조회가 아니라 로컬 데이터 요약입니다. 다음 조회에 쓸 검색어와 팩을 제안할 뿐, context를 만들거나 조회 경계를 우회하지 않습니다. MCP에서도 같은 context로 `expert_lookup/read/source`를 사용합니다.

## 최소 조회 구조

1. **역할 선택**: `data-analyst`의 기본 범위는 common+analytics. 매출·예측일 때만 sales, 품질일 때만 quality를 명시합니다.
2. **자료 요약**: 선택 열·최대 행 수로 읽기와 반환량을 제한합니다. raw 예제 값은 반환하지 않습니다. 숫자 범위·기간도 업무 정보이므로 사용자의 Codex 이용 정책을 따릅니다.
3. **요약 검색**: 기본 상위 3개/3500자. 2500자로 더 줄일 수 있습니다. 본문은 아직 보내지 않습니다.
4. **절 조회**: id와 conditions/procedure/limits 등 필요한 절을 지정합니다. 본문이 잘리면 next_offset만 이어 읽습니다.
5. **반복 계산**: 전처리·모델 학습·탐색은 로컬 코드가 수행합니다. 동일 근거는 재조회하지 않고 결과 파일은 필요한 진단 부분만 읽습니다.

기본적으로 거대한 JSONL·SQLite·카드 전체를 대화에 읽지 않습니다. 문자 상한은 실제 과금 토큰 상한이 아니며, 역할 선언 자체가 비용을 낮추는 것은 아닙니다. 실제 최소 토큰의 수학적 최적해를 보장하지 않습니다.

## 실행 가능한 예측 예제

스킬 폴더를 기준으로 `scripts/backtest.py`, `scripts/tune.py`를 실행합니다. 입력은 모든 제품이 같은 연속 달력을 가진 `unique_id,ds,y` CSV입니다. 일별 D 또는 월초 MS만 지원합니다. 백테스트의 상세 계약은 [forecasting](../plugins/expert-hub/skills/expert/references/forecasting.md)에 있습니다.

```powershell
$skill = '.\plugins\expert-hub\skills\expert'
# 개발 구간 기준모델 비교. 실제 업무 결과는 공개 저장소 밖의 새 폴더에 저장합니다.
python -B -X utf8 "$skill\scripts\backtest.py" --input "$skill\examples\synthetic-monthly.csv" --config "$skill\examples\backtest-config.json" --out '..\sales-runs\baseline'

# Ridge/Optuna를 사용할 때만 선택 가상환경에 설치합니다.
python -m venv .venv-forecast
.\.venv-forecast\Scripts\python.exe -m pip install -r requirements-forecast.txt
.\.venv-forecast\Scripts\python.exe -B -X utf8 "$skill\scripts\tune.py" --input "$skill\examples\synthetic-monthly.csv" --config "$skill\examples\backtest-config.json" --out '..\sales-runs\tuning' --trials 20 --seconds 120

# 모델 선택이 고정됐을 때만 실행합니다.
.\.venv-forecast\Scripts\python.exe -B -X utf8 "$skill\scripts\backtest.py" --input "$skill\examples\synthetic-monthly.csv" --config "$skill\examples\backtest-config.json" --selection '..\sales-runs\tuning\selection.json' --evaluate-holdout --out '..\sales-runs\final'
```

모델·데이터·설정·엔진 버전을 기록하며 같은 실험을 재개할 때만 `--resume`을 붙입니다. timeout은 진행 중 trial을 강제 종료하지 않습니다. Torch/GPU/MLForecast 모델 연결·계층 조정·예측구간·분산 학습은 추가 구현이 필요한 지침입니다. 합성 자료의 오차를 실제 회사 성능으로 제시하지 않습니다.

## 대용량과 안전한 해석

profile은 선택 열당 서로 다른 값의 해시를 최대 256개 보관하므로 행 전체를 메모리에 쌓지 않습니다. 기본 파일 선두 표본은 랜덤 표본이 아닙니다. rare category와 뒤쪽 오류를 놓칠 수 있습니다. `--max-rows 0`은 명시적으로 전체를 읽지만 처리시간은 행 수에 따라 증가합니다.
기본 QA `scan`과 forecasting 실행기는 대용량 분산 엔진이 아닙니다. 대규모 조인·정렬·고카디널리티 집계는 메모리/디스크를 확인하고 별도 엔진을 선택하세요.

자료의 자동 수집·지속 감시·모델 배포·GitHub 업로드는 포함하지 않습니다. 검증 결과와 참조 토큰 측정은 [데이터 분석 검증 기록](DATA_ANALYSIS_VALIDATION.md)을 확인하세요.
