"""
[Connected Car / SDV Big Data Lakehouse]
Ch 12. 모빌리티 제원 텔레메트리 기반 고객 프로파일링 & 소득 예측 회귀 모델링
Author: DMDG 출판부
"""

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from download_dataset import download_datasets

DATA_PATH = "data/CarMaster2Income.txt"

def run_regression_analysis():
    # 데이터 없으면 자동 다운로드
    if not os.path.exists(DATA_PATH):
        download_datasets()

    print("=== [Ch 12] 모빌리티 제원 기반 소득 예측 OLS 회귀 모델링 ===")
    
    # 1. 데이터 로드 (파이프 구분자 '|')
    df = pd.read_csv(DATA_PATH, sep='|', encoding='utf-8')
    print(f"데이터셋 형태: {df.shape} (레코드: {len(df):,}개, 컬럼: {df.columns.tolist()})")
    
    # 2. 전처리 및 독립변수/종속변수 정의
    # 수치형 변수: 배기량(capacity), 연령(age), 연식(year)
    # 범주형 원-핫 인코딩: 성별(sex), 결혼(marriage), 차종(type)
    feature_cols = ['capacity', 'age', 'year']
    X = df[feature_cols].copy()
    
    # 더미 변수 추가
    dummies = pd.get_dummies(df[['sex', 'marriage', 'type']], drop_first=True)
    X = pd.concat([X, dummies], axis=1).astype(float)
    y = df['income'].astype(float)

    # 3. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Statsmodels OLS 다중 회귀 모델 적합
    X_train_sm = sm.add_constant(X_train)
    ols_model = sm.OLS(y_train, X_train_sm).fit()

    print("\n--- [OLS 회귀 분석 요약 결과] ---")
    print(ols_model.summary().tables[0])
    print("\n주요 계수 및 p-value:")
    print(ols_model.pvalues)

    # 5. 테스트셋 평가
    X_test_sm = sm.add_constant(X_test)
    y_pred = ols_model.predict(X_test_sm)
    
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"\n[모델 성능 지표]")
    print(f"  * 테스트 R^2 (결정계수): {r2:.4f}")
    print(f"  * RMSE (평균제곱근오차): {rmse:.2f} 만원")

    # 6. 실무 예측 시뮬레이션
    sample_car = pd.DataFrame([{
        'capacity': 3000,
        'age': 45,
        'year': 2024,
        'sex_여': 0,
        'marriage_미혼': 0,
        'type_B': 1,
        'type_C': 0
    }], columns=X.columns).fillna(0).astype(float)
    
    sample_sm = sm.add_constant(sample_car, has_constant='add')
    predicted_income = ols_model.predict(sample_sm)[0]
    print(f"\n[실전 예측 시뮬레이션] 45세 / 3000cc / 2024년식 / 기혼 남성 예상 연소득: {predicted_income:,.0f} 만원")

if __name__ == "__main__":
    run_regression_analysis()

