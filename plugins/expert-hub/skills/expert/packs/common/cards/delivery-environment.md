# 사용 환경에 맞는 결과물·기술 선택

ID: `common:delivery-environment` | both | reference-only; no external tool installed

수신자의 인터넷·설치·저장·공유·출력 조건을 먼저 확인해 최소 완결 경로를 선택한다.

## conditions

누가 어디에서 어떤 결정을 위해 결과물을 쓰는지와 실제 실행 환경을 확인한다. 라이브러리 이름이나 개발자 선호만으로 기술을 고르지 않는다.

## procedure

인터넷 연결, 설치 권한, 사용 가능한 런타임, 데이터 유지 기간, 공동 열람, 필요한 출력 형식을 확인한다. 제공된 도구와 기존 코드를 우선해 입력에서 출력까지 작동하는 최소 경로를 만든다.

## verification

수신 환경에서 파일 열기·핵심 행동·저장 후 다시 열기·필요한 공유/출력을 확인한다. 다른 환경에서만 검사했다면 그 차이를 기록한다.

## limits

이 절차는 환경 확인 방법이며 특정 제품 설치·네트워크 접근·공유 게시의 권한을 부여하지 않는다. 예제 런타임 조건을 모든 프로젝트에 일반화하지 않는다.

## 출처

- [probe-stack — 공개 준비 지침의 일반 절차](https://github.com/PKJthecreator/probe-kit/blob/79f2f94917ad32a630fd7d13c728409d6ec3de8b/.agents/skills/probe-stack/SKILL.md) · public-preparation-guidance · 확인 2026-10-30
