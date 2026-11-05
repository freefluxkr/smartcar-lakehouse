"""
[Connected Car / SDV Big Data Lakehouse]
Ch 13. 센서 시계열 특성 기반 주행 사고 패턴 3-Class 심층 신경망(DNN) 분류기
Author: DMDG 출판부
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from download_dataset import download_datasets

DATA_PATH = "data/CarDrivingIncidentInfo.csv"

def run_dnn_classification():
    if not os.path.exists(DATA_PATH):
        download_datasets()

    print("=== [Ch 13] 주행 사고 센서 특성 기반 3-Class 심층 신경망(DNN) 분류기 ===")
    
    # 1. 데이터 로드 (헤더 첫 라인이 통계 메타정보인 경우 스킵)
    try:
        df = pd.read_csv(DATA_PATH, skiprows=1, header=None)
        # 컬럼 정의: 기상, 기온, 습도, 주변차량수, 시간대, 사고지역, 도로상태, 운전자상태, 차량속도, 조향각, 사고부위(타깃)
        df.columns = ['wea', 'temp', 'hum', 'arrCar', 'timeSlot', 'acciArea', 'drvCond', 'innCond', 'carSpd', 'steeAng', 'acciPos']
    except Exception as e:
        print(f"데이터 로드 재시도: {e}")
        df = pd.read_csv(DATA_PATH)

    print(f"데이터셋 형태: {df.shape} (총 {len(df):,}건 주행 사고 레코드)")
    
    # 2. 독립변수 / 종속변수 분리
    feature_cols = ['wea', 'temp', 'hum', 'arrCar', 'timeSlot', 'acciArea', 'drvCond', 'innCond', 'carSpd', 'steeAng']
    X = df[feature_cols].values
    
    # 레이블 인덱싱 (1, 2, 3 -> 0, 1, 2)
    y_raw = df['acciPos'].values
    min_y = min(y_raw)
    y = (y_raw - min_y).astype(int)
    num_classes = len(np.unique(y))
    print(f"사고 부위 클래스: {num_classes}개 (Class 0: 전면부, Class 1: 측면부, Class 2: 후면부)")

    # 3. Train / Validation / Test 분할
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. 정규화 (StandardScaler)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. TensorFlow Keras 모델 구축
    try:
        import tensorflow as tf
        from tensorflow.keras import layers, models

        print(f"\nTensorFlow 버전: {tf.__version__}")
        
        model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(num_classes, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("\n--- 심층 신경망(DNN) 아키텍처 요약 ---")
        model.summary()

        # 6. 학습 수행 (실습용 에포크 10회)
        print("\n--- 모델 학습 시작 ---")
        history = model.fit(
            X_train_scaled, y_train,
            epochs=10,
            batch_size=128,
            validation_split=0.2,
            verbose=1
        )

        # 7. 평가
        test_loss, test_acc = model.evaluate(X_test_scaled, y_test, verbose=0)
        print(f"\n[최종 테스트셋 평가]")
        print(f"  * Test Loss: {test_loss:.4f}")
        print(f"  * Test Accuracy (사고 부위 분류 정확도): {test_acc*100:.2f}%")

    except ImportError:
        print("\n[알림] TensorFlow가 설치되지 않은 환경입니다. Scikit-Learn MLPClassifier로 대체 평가를 진행합니다.")
        from sklearn.neural_network import MLPClassifier
        clf = MLPClassifier(hidden_layer_sizes=(128, 64, 32), max_iter=20, random_state=42)
        clf.fit(X_train_scaled, y_train)
        score = clf.score(X_test_scaled, y_test)
        print(f"Scikit-Learn MLP 테스트 정확도: {score*100:.2f}%")

if __name__ == "__main__":
    run_dnn_classification()

