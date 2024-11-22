import network
import socket
from time import sleep


def web_page():
    # 버튼 기반 HTML 추가
    html = """
            <!DOCTYPE html>
            <html>
            <head>
            <title>Robot Control</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
            <h1>Robot Control</h1>
            <form action="/forward">
                <input type="submit" value="Forward" style="height:100px; width:200px; font-size:20px" />
            </form>
            <form action="/backward">
                <input type="submit" value="Backward" style="height:100px; width:200px; font-size:20px" />
            </form>
            <form action="/left">
                <input type="submit" value="Left" style="height:100px; width:200px; font-size:20px" />
            </form>
            <form action="/right">
                <input type="submit" value="Right" style="height:100px; width:200px; font-size:20px" />
            </form>
            <form action="/stop">
                <input type="submit" value="Stop" style="height:100px; width:200px; font-size:20px" />
            </form>
            </body>
            </html>
           """
    return html


def handle_request(request):
    """
    HTTP 요청 처리 및 명령 수행
    """
    if '/forward' in request:
        print("Moving forward!")
    elif '/backward' in request:
        print("Moving backward!")
    elif '/left' in request:
        print("Turning left!")
    elif '/right' in request:
        print("Turning right!")
    elif '/stop' in request:
        print("Stopping!")


def ap_mode(ssid, password):
    """
    AP 모드 활성화 함수
    """
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while not ap.active():
        print("AP 설정 중...")
        sleep(1)

    print("AP Mode Is Active, You can Now Connect")
    print("IP Address To Connect to:: " + ap.ifconfig()[0])

    # 소켓 생성
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 재사용 설정
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print(f"Got a connection from {addr}")
        try:
            request = conn.recv(1024).decode('utf-8')
            print(f"Content = {request}")

            # 요청 처리
            handle_request(request)

            # HTML 응답 반환
            response = web_page()
            conn.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()


# AP 모드 실행
try:
    ap_mode('haha', '11111111')
except KeyboardInterrupt:
    print("Stopped by user.")


