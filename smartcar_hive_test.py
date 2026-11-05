from pyhive import hive

def test_hive():
    print("--- 2. Hive Server2 연동 테스트 시작 ---")
    try:
        # Hive Server2 연결 (기본 SASL PLAIN 인증, auth='NOSASL' 불필요)
        conn = hive.Connection(
            host="localhost",
            port=10000,
            username="hive",
            database="default"
        )
        cursor = conn.cursor()

        # 1. 샘플 테이블 생성 (존재하지 않는 경우)
        create_table_query = """
        CREATE TABLE IF NOT EXISTS smartcar_logs (
            car_id STRING,
            speed DOUBLE,
            rpm INT,
            location STRING
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        """
        print("Hive 테이블 생성 중...")
        cursor.execute(create_table_query)
        print("테이블 생성 완료!")

        # 2. 데이터 조회 쿼리 실행
        print("Hive 테이블 목록 조회:")
        cursor.execute("SHOW TABLES")
        for result in cursor.fetchall():
            print(f"- {result}")

        cursor.close()
        conn.close()
        print("--- Hive 테스트 완료 ---")

    except Exception as e:
        print(f"[연결 실패] 에러 내용: {e}")
        print("팁: Hive Server가 아직 완전히 부팅되지 않았거나 컨테이너 로그를 확인해 보세요.")

if __name__ == "__main__":
    test_hive()
