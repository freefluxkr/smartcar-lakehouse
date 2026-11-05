# 🚗 SDV & 커넥티드 카 빅데이터 레이크하우스 실습 킷
> **도서**: 《SDV & 커넥티드 카 빅데이터 레이크하우스 실무 가이드》  
> **저자/기획**: DMDG 출판부 (당목담글 스튜디오 Great AI 출판본부)  
> **공식 저장소**: [https://github.com/freefluxkr/smartcar-lakehouse](https://github.com/freefluxkr/smartcar-lakehouse)

---

## 🏗️ 1. 한눈에 보는 레이크하우스 엔드투엔드 파이프라인

![아키텍처 다이어그램](architecture_diagram.jpg)

```
[차량 텔레메트리 (OBD-II/GPS)] ➔ [Apache Kafka (9092)] ➔ [PyHive Pipeline Engine]
                                                                  │
                                                                  ▼
[TensorFlow 딥러닝 & Pydeck 3D] ◀── [Apache Hive (10000)] ◀── [Hadoop HDFS (9870)]
                                            │
                                            ▼
                               [PostgreSQL 메타스토어 (5432)]
```

---

## ⚡ 2. 초간단 3단계 실습 시작하기 (WSL2 / Ubuntu)

### Step 1. 저장소 클론 및 패키지 설치
```bash
git clone https://github.com/freefluxkr/smartcar-lakehouse.git ~/smartcar-pilot
cd ~/smartcar-pilot
poetry install
```

### Step 2. 빅데이터 에코시스템 컨테이너 기동
```bash
docker compose up -d
docker compose ps
```
> **팁**: Hive Server2가 완전히 부팅되어 10000 포트가 열릴 때까지 약 1~2분이 소요됩니다.

### Step 3. 실습 데이터셋 동기화
```bash
# GitHub 원격 저장소에서 1-Click 자동 다운로드 및 검증
poetry run python download_dataset.py
```

---

## 🧪 3. 핵심 실습 스크립트 실행 가이드

| 스크립트명 | 담당 파트 | 설명 |
| :--- | :--- | :--- |
| `smartcar_kafka_test.py` | Part 3 | 카프카 토픽(`smartcar-status`) 프로듀서 & 컨슈머 스트리밍 검증 |
| `smartcar_hive_test.py` | Part 4 | Hive Server2 연결 및 HDFS 파일 시스템 연동 검증 |
| `smartcar_pipeline.py` | Part 4 | 카프카 스트림 데이터를 실시간으로 읽어 Hive 테이블에 자동 적재 |
| `smartcar_regression.py` | Part 5 (Ch 12) | 모빌리티 제원 텔레메트리 기반 고객 프로파일링 & 소득 예측 회귀 모델 |
| `smartcar_dnn_classifier.py`| Part 5 (Ch 13) | 10대 센서 특성 기반 TensorFlow Keras 주행 사고 부위 심층 신경망 분류기 |

---

## 📜 라이선스
MIT License. 교육 및 실무 프로젝트에 자유롭게 활용하실 수 있습니다.
