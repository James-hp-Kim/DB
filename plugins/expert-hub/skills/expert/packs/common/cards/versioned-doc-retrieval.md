# 버전별 문서와 제한된 외부 조회

ID: `common:versioned-doc-retrieval` | both | reference-only; optional procedures require user consent

라이브러리의 실제 버전과 질문을 먼저 특정하고 필요한 문서만 읽는다. Context7은 선택 가능한 문서 조회 수단이다.

## conditions

버전에 따라 API나 설치법이 달라지고 기존 근거로 해결되지 않을 때 적용한다. Context7 사용은 먼저 동의를 받는다.

## procedure

의존성 파일에서 버전을 확인한다. 알려진 libraryId를 재사용하고 필요한 질문 하나로 query-docs를 호출한다. 연결이 없으면 공식 문서를 확인하고 대체 방법을 밝힌다.

## verification

문서의 버전·실제 코드·지원 파일이 일치하는지 대조한다. 조회 결과의 출처를 보존하고 실제 연동은 별도로 시험한다.

## limits

Context7 서버 설치·인증·연결은 이 DB가 수행하지 않는다. 최신 문서 반환이 코드 정확성이나 실행 성공의 증거는 아니다.

## 출처

- [context7 선택 절차의 공개 근거](https://github.com/upstash/context7/blob/c964733a3d87e89acd177cc4b24ebef4a7662f06/README.md) · upstream-technical-guidance · 확인 2026-10-30
