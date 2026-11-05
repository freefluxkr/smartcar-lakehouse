import json
import time
from kafka import KafkaConsumer, KafkaProducer

TOPIC_NAME = "smartcar-status"
BOOTSTRAP_SERVERS = ["localhost:9092"]

def test_kafka():
    print("--- 1. Kafka Producer & Consumer 테스트 시작 ---")

    # 1. Producer 생성 (데이터 발행)
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # 샘플 스마트카 데이터 전송
    sample_data = {
        "car_id": "CAR-001",
        "speed": 85.5,
        "rpm": 2500,
        "location": "Seoul-Gangnam",
        "timestamp": time.time(),
    }

    print(f"데이터 전송 중: {sample_data}")
    producer.send(TOPIC_NAME, value=sample_data)
    producer.flush()  # 버퍼 강제 전송
    print("데이터 전송 완료!")

    # 2. Consumer 생성 (데이터 수신)
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="smartcar-group",
        consumer_timeout_ms=3000,  # 3초 동안 메시지가 없으면 자동 종료
    )

    print("Kafka 메시지 수신 대기 중...")
    received_count = 0
    for message in consumer:
        print(f"[수신 성공] 토픽: {message.topic}, 데이터: {message.value.decode('utf-8')}")
        received_count += 1
        if received_count >= 1:
            break

    consumer.close()
    print("--- Kafka 테스트 완료 ---\n")

if __name__ == "__main__":
    test_kafka()
