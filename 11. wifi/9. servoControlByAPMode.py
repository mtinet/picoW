import network
import socket
from time import sleep
from machine import Pin, PWM

# 서보 핀 및 주파수 설정
servo = PWM(Pin(22))
servo.freq(50)

def set_angle(servo, angle):
    """
    서보 모터의 각도를 설정하는 함수
    """
    duty = int(((((angle) * 2) / 180) + 0.5) / 20 * 65535)
    servo.duty_u16(duty)
    print(f"Servo moved to {angle} degrees")

def web_page():
    """
    HTML 페이지 생성
    """
    html = """
            <!DOCTYPE html>
            <html lang="ko">
            <head>
            <meta charset="UTF-8">
            <title>서보모터 제어</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
            <h1>서보모터 제어</h1>
            <a href="/servo?angle=0"><button style="height:100px; width:200px; font-size:20px">0° (0도)</button></a>
            <a href="/servo?angle=45"><button style="height:100px; width:200px; font-size:20px">45° (45도)</button></a>
            <a href="/servo?angle=90"><button style="height:100px; width:200px; font-size:20px">90° (90도)</button></a>
            <a href="/servo?angle=135"><button style="height:100px; width:200px; font-size:20px">135° (135도)</button></a>
            <a href="/servo?angle=180"><button style="height:100px; width:200px; font-size:20px">180° (180도)</button></a>
            </body>
            </html>
           """
    return html

def handle_request(request):
    """
    HTTP 요청 처리 및 명령 수행
    """
    if '/servo?angle=' in request:
        try:
            # 요청에서 각도 값 추출
            angle = int(request.split("/servo?angle=")[1].split(" ")[0])
            set_angle(servo, angle)
        except Exception as e:
            print(f"Error parsing angle: {e}")

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

