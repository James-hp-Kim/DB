# 교란과 구성비 변화: 상관을 원인으로 읽지 않기

ID: `common:confounding` | deep | reference-only

설비·제품·교대·LOT·시간이 함께 변하면 단순 비교의 방향이 뒤집힐 수 있다.

## procedure

전체 불량률 증가가 제품 구성비 변화 때문인지 동일 제품 내 악화인지 나눈다.
설비별로 처리 제품·레시피·재료 LOT·시간대가 다르면 층화 또는 적절한 조정 모형을 검토한다. 비교 가능한 조건이 없는 경우 통계가 인과를 복원해주지는 않는다.

## verification

원인 후보는 발생 전후 시간 관계, 대조 조건, 물리적 설명, 개입 결과로 검증한다.
가능하면 무작위화·블록·반복을 갖춘 DOE 또는 통제된 파일럿으로 확인한다. SHAP·상관계수·변수 중요도만으로 원인을 확정하지 않는다.

## 출처

- [NIST: Process improvement / DOE](https://www.itl.nist.gov/div898/handbook/pri/pri.htm) · primary · 확인 2026-10-29
- [NIST: Product and process comparisons](https://www.itl.nist.gov/div898/handbook/prc/prc.htm) · primary · 확인 2026-10-29
