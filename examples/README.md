# 합성 예제

모든 CSV는 테스트용으로 만든 합성 자료입니다. 회사/생산 실측 자료가 아닙니다.

- quick-counts.csv: M1 15/1500=1%, M2는 동일 행이 반복되어 16/200=8%로 계산하며 중복 후보를 남깁니다. M3 0/0은 계산 불가입니다.
- deep-stream.csv: 독립 개별 관측을 가정한 합성 평균 이동. 예제 기준 평균 10, 표준편차 0.1.
- deep-features.csv: 마지막 행에 큰 편차를 주입한 수치 데이터. 탐지 순위 테스트이며 실제 정확도 측정이 아닙니다.

패키지 루트에서 실행 예시:

```powershell
$qa = '.\plugins\expert-hub\skills\expert\scripts\expert.py'
python -X utf8 $qa scan .\examples\quick-counts.csv --groups machine --numerator defective --denominator inspected --out .\runs\quick-01
python -X utf8 $qa monitor .\examples\deep-stream.csv --value value --mean 10 --sigma 0.1 --order timestamp --baseline-validated --out .\runs\monitor-01
# 선택 PyOD 환경을 만든 뒤:
.\.venv\Scripts\python.exe -X utf8 $qa anomalies .\examples\deep-features.csv --values thickness pressure temperature --top 5 --out .\runs\multivariate-01
```

`--baseline-validated`는 이 합성 자료의 알려진 생성 조건에 대한 확인입니다. 실제 자료의 안정성을 자동 검정해주는 옵션이 아닙니다. 각 실행의 전체 근거는 해당 출력 폴더의 `result.json`, `findings.csv`에 남습니다.

M2의 반복 행은 원본 오류인지 실제 반복 검사인지 알 수 없으므로 임의로 삭제하지 않습니다. 불량률·구간 역시 해당 표본 구조가 확인되기 전까지 잠정 결과입니다. [검증 결과](../docs/VALIDATION.md)에 기대값과 해석을 정리했습니다.
