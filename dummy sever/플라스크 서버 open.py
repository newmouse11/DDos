
# 내부 접속주소는 127.0.0.1:8080 입니다. (localhost 기준)
# 외부 접속주소는 192.168.1.1(IPv4):8080 입니다. (포트포워딩 하셔야 외부 접속 가능합니다)



from flask import Flask, request
import time
import math

print("Made by sen1080")
print("서버 시작 중...")

app = Flask(__name__)

@app.route("/")
def index():
    cu_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("[" + cu_time + "] ip " + request.remote_addr + " 에서 GET요청을 함")
    return "hello wolrd!"

if __name__ == "__main__":
    print("서버가 시작됨")
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080, connection_limit=1000)
    #app.run(debug=True, host="0.0.0.0", port=25565)