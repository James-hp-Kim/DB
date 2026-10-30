# MAD 기반 이상치 후보 탐색

ID: `common:robust-outliers` | quick | scan --values

중앙값과 MAD로 극단값 후보를 찾되, 후보를 불량이나 오류로 확정하지 않는다.

## procedure

중앙값 m, MAD=median(|x-m|), 수정 z=0.67448975(x-m)/MAD를 사용한다. |z|>3.5는 탐색용 기준이다.

## limits

본 스크립트는 표본 8개 미만 또는 MAD=0일 때 이 검사를 생략하고 이유를 출력한다. 이는 이상 없음이 아니다.
다봉 분포, 이산 측정, 다른 제품 혼합, 자기상관, 정상 공정 변경은 별도 분석이 필요하다.
공정 평균의 작은 지속 변화는 이 검사로 놓칠 수 있으므로 시간 흐름이 중요하면 EWMA/CUSUM으로 심층 검토한다.

## verification

원본 값을 수정·삭제하지 않고 원본 레코드와 값을 남긴다. 규격 이탈, 통계 이상, 데이터 오류를 구별한다.

## 출처

- [NIST: Detection of outliers](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm) · primary · 확인 2026-10-29
