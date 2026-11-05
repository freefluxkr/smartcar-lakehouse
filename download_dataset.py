"""
[Connected Car / SDV Big Data Lakehouse]
Dataset Auto Downloader & Verification Script
Author: DMDG 출판부
"""

import os
import sys
import urllib.request

REPO_RAW_URL = "https://raw.githubusercontent.com/freefluxkr/smartcar-lakehouse/main/data"

DATA_FILES = [
    "CarMaster2Income.txt",
    "CarMaster2Income_Test.txt",
    "CarDrivingIncidentInfo.csv",
    "CarDrivingIncidentInfo_Test.csv"
]

def download_datasets(target_dir="data"):
    os.makedirs(target_dir, exist_ok=True)
    print(f"=== [SDV Lakehouse] 실습 데이터셋 동기화 시작 (저장 경로: {target_dir}/) ===")
    
    for filename in DATA_FILES:
        target_path = os.path.join(target_dir, filename)
        file_url = f"{REPO_RAW_URL}/{filename}"
        
        if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
            print(f"[OK] 이미 존재하는 파일: {filename} ({os.path.getsize(target_path):,} bytes)")
            continue
            
        print(f"[다운로드 중] {filename} <- {file_url}")
        try:
            urllib.request.urlretrieve(file_url, target_path)
            size = os.path.getsize(target_path)
            print(f"  -> 완료! 크기: {size:,} bytes")
        except Exception as e:
            print(f"  -> [오류 발생]: {e}")
            print(f"     GitHub 저장소(https://github.com/freefluxkr/smartcar-lakehouse)를 직접 확인하세요.")

    print("\n=== 모든 실습 데이터셋 준비가 완료되었습니다. ===")

if __name__ == "__main__":
    download_datasets()

