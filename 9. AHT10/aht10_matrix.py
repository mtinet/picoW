from time import sleep
from machine import Pin, PWM, I2C
import neopixel

# LED 설정 (핀 16, 25개)
matrix = neopixel.NeoPixel(Pin(16), 25)
BRIGHTNESS = 20

# 서보 및 I2C 설정
servo = PWM(Pin(2))
servo.freq(50)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

def set_matrix(temp, hum, status_ok, blink_state):
    matrix.fill((0, 0, 0))
    
    # 1. 온도 표시 (-10~40도, 10칸)
    # temp -10 -> 0칸, temp 40 -> 10칸
    t_count = min(10, max(0, int((temp + 10) / 5))) 
    t_color = (BRIGHTNESS, 0, 0)
    indices_t = [20, 21, 15, 16, 10, 11, 5, 6, 0, 1]
    for i in range(t_count):
        matrix[indices_t[i]] = t_color

    # 2. 습도 표시 (0~100%, 10칸)
    h_count = min(10, max(0, int(hum / 10)))
    h_color = (0, 0, BRIGHTNESS)
    indices_h = [23, 24, 18, 19, 13, 14, 8, 9, 3, 4]
    for i in range(h_count):
        matrix[indices_h[i]] = h_color
        
    # 3. 가운데 줄 (시스템 상태)
    # 정상: 초록색 / 오류: 흰색 깜빡임(blink_state에 따라 켬/끔)
    if status_ok:
        s_color = (0, BRIGHTNESS, 0)
    else:
        s_color = (BRIGHTNESS, BRIGHTNESS, BRIGHTNESS) if blink_state else (0, 0, 0)
        
    for i in [2, 7, 12, 17, 22]:
        matrix[i] = s_color
        
    matrix.write()

# ========== 메인 루프 ==========
blink = True
while True:
    try:
        i2c.writeto(0x38, b'\xAC\x33\x00')
        sleep(0.1)
        data = i2c.readfrom(0x38, 6)
        temp = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / 1048576 - 50
        hum = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / 1048576
        
        print(f"온도: {temp:.1f}°C | 습도: {hum:.1f}%")
        set_matrix(temp, hum, True, True)
        
        # 서보 동작 (예시: 28도 기준)
        servo.duty_u16(8192 if temp >= 28 else 1638)
            
    except Exception as e:
        print("❌ 센서 오류:", e)
        set_matrix(0, 0, False, blink)
        blink = not blink # 상태 반전
        
    sleep(0.5) # 깜빡임을 위해 주기 단축
