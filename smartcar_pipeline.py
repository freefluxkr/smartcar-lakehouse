"""
[Connected Car / SDV Big Data Lakehouse]
Real-time Kafka -> Hive / HDFS Stream & Batch Pipeline
Author: DMDG 출판부
"""

import json
import time
from kafka import KafkaConsumer
from pyhive import hive

KAFKA_TOPIC = "smartcar-status"
KAFKA_SERVERS = ["localhost:9092"]
HIVE_HOST = "localhost"
HIVE_PORT = 10000

def run_pipeline():
    print(f"=== [Kafka -> Hive Pipeline] 초기화 시작 ===")
    print(f"  * Kafka 브로커: {KAFKA_SERVERS}, 토픽: {KAFKA_TOPIC}")
    print(f"  * Hive Server2: {HIVE_HOST}:{HIVE_PORT}")

    # 1. Hive 연결 (SASL PLAIN)
    hive_conn = hive.Connection(host=HIVE_HOST, port=HIVE_PORT, username="hive")
    cursor = hive_conn.cursor()

    # 테이블 생성 보장
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS smartcar_logs (
        car_id STRING,
        speed DOUBLE,
        rpm INT,
        location STRING,
        event_time STRING
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    """
    cursor.execute(create_table_sql)
    print("  -> Hive 테이블 'smartcar_logs' 준비 완료.")

    # 2. Kafka 컨슈머 연결
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVERS,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="smartcar-pipeline-group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )

    print("\n[수신 대기 중...] 차량 텔레메트리 스트림 수신 대기 (종료: Ctrl+C)")
    try:
        for msg in consumer:
            car_data = msg.value
            car_id = car_data.get("car_id", "UNKNOWN")
            speed = float(car_data.get("speed", 0.0))
            rpm = int(car_data.get("rpm", 0))
            location = car_data.get("location", "SEOUL")
            ev_time = car_data.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))

            # Hive INSERT
            insert_sql = f"""
            INSERT INTO TABLE smartcar_logs
            VALUES ('{car_id}', {speed}, {rpm}, '{location}', '{ev_time}')
            """
            cursor.execute(insert_sql)
            print(f"[Hive 적재 완료] {ev_time} | 차번: {car_id} | 속도: {speed}km/h | RPM: {rpm} | 위치: {location}")

    except KeyboardInterrupt:
        print("\n파이프라인 중단 신호 감지.")
    finally:
        cursor.close()
        hive_conn.close()
        consumer.close()
        print("파이프라인 자원이 안전하게 해제되었습니다.")

if __name__ == "__main__":
    run_pipeline()

