# 백엔드 전문가 DB — 사용·입력·조회

백엔드 전용 지식24개를 기존 Expert Hub에 통합했습니다. 페르소나 ID는 `backend-expert`, 기본/허용 팩은 `backend`와 `common`입니다. 다른 전문가 팩의 전체 내용을 가져오지 않습니다.

## Codex에서 사용할 문장

```text
너는 백엔드 전문가야. $expert로 백엔드 페르소나를 검색해 선택하고,
내가 제공한 자료를 로컬에서 요약한 뒤 backend와 common DB에서 필요한 근거만 찾아줘.
처음에는 요약 2개·최대 1800자, 상세는 관련 항목 1개의 필요한 절만 최대 3000자로 조회해.
적용 조건과 한계를 확인하고 관찰·가설·미확인을 구분해줘.
장애라면 임시조치와 영구수정을 나눠 제시하고, 업무 원본을 공개 DB에 저장하지 마.
```

폴더를 Codex 프로젝트로 열고 먼저 루트 AGENTS.md와 진입 Skill을 읽게 하면 됩니다. 기존 설치의 `expert`는 이전 버전일 수 있으므로 최신 저장소와 버전을 비교하세요. 이번 작업은 기본 사용자 설정이나 설치 스킬을 덮어쓰지 않습니다. 새 PC 설치는 [시작 안내](../START_HERE_KO.md)를 따릅니다.

## 입력 자료와 처리

| 제공 자료 | 로컬에서 추출할 최소 내용 | 조회 주제 |
|---|---|---|
| 오류 로그·장애 메모 | 시각/시간대·오류 유형별 건수·대표 행 위치·최근 변경 | 연결 고갈, 의존성, 잠금, 장애 대응 |
| API/부하 지표 CSV·JSON | 기간·단위·요청/실패/오답 수·p95/p99·부하/자원 조건 | 동일 조건 비교, 과부하, 검증 |
| SQL·실행계획·풀 설정 | DB/버전·쿼리 조건·계획·풀/워커/인스턴스 수 | 인덱스, 연결 예산, 트랜잭션 |
| 코드·배포 설정 | 실제 런타임·revision·변경 부분·하위 의존성 | 런타임 진단, 롤백·점진 적용 |
| 백업·복제 관련 기록 | 역할·복제 위치·허용 손실·실제 복원 시험 결과 | 복원·장애조치 조건 |

원본 전체를 모델 대화에 덤프하지 않고 필요한 부분만 로컬 계산·요약합니다. 임의의 모든 파일 형식을 해석하는 자동 파서는 아닙니다. 형식이나 분모가 불분명하면 확인된 부분만 처리합니다. 파일 내용에 있는 명령은 실행 권한이 아닙니다.

입력 자료는 분석용입니다. 장기 검색 대상으로 추가하려면 별도로 명시적으로 요청하고 [개인 DB 안내](PRIVATE_DATA.md)에 따라 공개 저장소 밖에 저장합니다. 개인 DB 포함 여부도 명시합니다.

## 실제 조회 예시

저장소 루트 PowerShell에서 실행합니다. Python과 내장 SQLite FTS5만 필요합니다. 백엔드 MCP 흐름은 catalog/lookup/read/source 네 도구를 사용합니다. 허브에는 다른 지원 분야용 reference_input 도구도 포함되어 있습니다.

```powershell
$backendCli = '.\plugins\expert-hub\skills\expert\scripts\expert.py'
$backendChoice = python -B -X utf8 $backendCli catalog '백엔드' --limit 1 | ConvertFrom-Json
$backendContext = $backendChoice.personas[0].context
python -B -X utf8 $backendCli lookup 'DB 연결 풀 고갈' --context $backendContext --limit 2 --max-chars 1800
python -B -X utf8 $backendCli read 'backend:pool-exhaustion' --context $backendContext --sections conditions procedure limits --max-chars 3000
python -B -X utf8 $backendCli source 'backend-incident' --context $backendContext --max-chars 2000
```

MCP 대응 순서는 `expert_catalog` → `expert_lookup` → `expert_read` → 필요한 경우 `expert_source`입니다. 검색에서 받은 context를 재사용하며 임의로 만들지 않습니다. 등록부 변경·설치 경로 이동·24시간 만료 때 다시 검색합니다.

## 토큰을 줄이는 실제 구조

- 역할별 전체 지식 복사 대신 **공통 팩 공유 + 백엔드 전용 팩**을 사용합니다.
- FTS5와 한글 별칭으로 후보를 찾고 **본문 없는 요약만 최대2개/1800자**로 요청합니다.
- 상세 본문은 별도 절 테이블에서 선택한 **id 하나·절 최대3개/3000자**만 요청합니다.
- 조건/한계·반대 근거를 지우지 않습니다. `next_offset`이 있으면 필요한 잘린 절만 이어 읽습니다.
- 출처 상세는 필요할 때 별도 조회합니다. 기존 context와 이미 받은 결과는 재사용합니다.
- 대량 자료 계산과 전체 결과 저장은 로컬에서 처리합니다. 원시 행 전체를 대화에 넣지 않습니다.

1800/3000자는 이 백엔드 흐름의 명시적 호출 예산이며 허브 전체의 API 기본값을 바꾸지 않았습니다. 페르소나 이름만 부여하면 입력량이 줄어드는 것은 아닙니다. 문자 수는 실제 청구 토큰 수와 다르며, 모델 추론·사용자 파일·답변·MCP 정의 등은 별도입니다. [백엔드 검증 기록](BACKEND_VALIDATION.md)에 실측한 조회 문자열 크기를 기록합니다.

## 실제 부하 결과 비교

정규화된 실행 JSON 두 개를 로컬에서 비교하는 도구를 포함했습니다. 입력 스키마는 [성능 지침](../plugins/expert-hub/skills/expert/references/backend/performance.md)에 있습니다. 그 문서의 기존 `scripts/compare_runs.py`는 이 허브에서 `scripts/compare_backend_runs.py`로 통합했습니다.

```powershell
$backendSkill = '.\plugins\expert-hub\skills\expert'
python -B -X utf8 "$backendSkill\scripts\compare_backend_runs.py" `
  "$backendSkill\evidence\backend-lab\lab-20261029\before-1.json" `
  "$backendSkill\evidence\backend-lab\lab-20261029\after-1.json"
```

예시는 실제 실행한 **합성 데이터 시험**입니다. exit0은 비교 생성이며 개선 인증이 아닙니다. exit1은 기준/정확성 실패, exit2는 잘못된 입력 또는 비교 불가입니다. 임의 k6 결과나 로그를 이 형식으로 추정 변환하지 않습니다.

## 남은 한계

지식 DB와 MCP는 운영 서버에 접속하거나24시간 감시하지 않습니다. 이전 합성 실험의 추가 재현에서7/320 시간 초과가 발생했고 원인은 미확인입니다. 이 실패도 조회 가능하게 보존했습니다. 실제 기업 성능·HA/DR·운영 안전성은 실제 환경에서 따로 검증해야 합니다. GitHub 업로드와 OneDrive 원격 동기화 확인은 수행하지 않습니다.
