# 실제 모델 비교는 별도로 수행

이 자료는 가상 평가 사례이며 실제 시험 문제나 성능 실측 결과가 아니다. cases.jsonl·expected.json은 평가자가 읽고, 풀이 채팅에는 해당 prompt와 inputs만 제공한다. 사례의 fixtures 경로는 이 benchmarks 폴더 기준이다.

같은 모델·설정·데이터·도구·네트워크 조건에서 기존 Hub만 적용한 기준 실행과 보완 패키지를 적용한 실행을 각각 새 채팅에서 비교한다. 설치·스킬 본문 변경은 채팅 시작 전에 완료한다. 순서를 교차하고 가능하면 각 사례를 3회 반복한다. 실제 요청 전 사례 전체·정답을 풀이 모델에 제공하지 않는다.

먼저 정답·근거 적합성·필수 조건·권한 경계를 통과했는지 평가하고 그 다음 속도·토큰을 비교한다. 빠르지만 잘못된 실행은 개선으로 세지 않는다. 완전한 답변까지 걸린 시간, 사용자 확인 왕복, 도구 호출 수, 읽은 파일과 절, 실제 입력/출력/캐시 토큰을 구분해 기록한다. 토큰을 얻을 수 없으면 null로 남기고 문자 수로 대체 추정하지 않는다.

run_id, case_id, variant, model, settings, elapsed_seconds, input_tokens, output_tokens, cached_tokens, tool_calls, user_round_trips, correctness_pass, evidence_pass, scope_pass, notes를 실행 기록에 남긴다. 문제 유형별 결과를 비교하고 표본 수·실패 사례를 함께 보고한다. 본 패키지는 유료 모델 호출이나 실제 외부 발송을 자동 실행하지 않는다.

check_bundle.py의 fixture 계산 검사는 기대값의 일관성 검사다. 모델이 해당 답을 냈다는 증거가 아니다. C11·C12는 실제 Hub가 필요하며, C05는 예측 품질 측정보다 과장 억제·범위 설정을 평가한다.
