from time import sleep
from machine import Pin, PWM, I2C
import neopixel

# ========== 1. 하드웨어 설정 ==========
# LED 매트릭스: GP16, 25개
matrix = neopixel.NeoPixel(Pin(16), 25)
BRIGHTNESS = 20

# 서보모터: GP2
servo = PWM(Pin(2))
servo.freq(50)

# 릴레이: GP6 (팬 제어)
relay = Pin(6, Pin.OUT)
relay.value(0) 

# AHT10: I2C0 (GP0: SDA, GP1: SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# ========== 2. 기능 함수 ==========

def set_matrix(temp, hum, status_ok, fan_on, blink):
    """
    blink: True면 상태줄 켬, False면 끔
    """
    matrix.fill((0, 0, 0))
    
    # 1. 온도 표시 (-10~40도, 10칸)
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
        
    # 3. 가운데 줄 (상태 표시)
    if not status_ok:
        # 센서 오류: 흰색 깜빡임
        s_color = (BRIGHTNESS, BRIGHTNESS, BRIGHTNESS) if blink else (0, 0, 0)
    elif fan_on:
        # 팬 작동 중: 초록색 깜빡임
        s_color = (0, BRIGHTNESS, 0) if blink else (0, 0, 0)
    else:
        # 대기 상태: 초록색 고정
        s_color = (0, BRIGHTNESS, 0)
        
    for i in [2, 7, 12, 17, 22]:
        matrix[i] = s_color
        
    matrix.write()

# ========== 3. 메인 루프 ==========
blink_toggle = True
HUMIDITY_THRESHOLD = 60

print("🚀 시스템 시작")

while True:
    try:
        # 센서 데이터 읽기
        i2c.writeto(0x38, b'\xAC\x33\x00')
        sleep(0.1)
        data = i2c.readfrom(0x38, 6)
        
        temp = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / 1048576 - 50
        hum = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / 1048576
        
        # 릴레이 제어
        is_fan_on = hum >= HUMIDITY_THRESHOLD
        relay.value(1 if is_fan_on else 0)
        
        # LED 업데이트
        set_matrix(temp, hum, True, is_fan_on, blink_toggle)
        
        # 서보 동작
        servo.duty_u16(8192 if temp >= 28 else 1638)
            
    except Exception as e:
        print("❌ 센서 오류:", e)
        set_matrix(0, 0, False, False, blink_toggle)
        relay.value(0)
        
    blink_toggle = not blink_toggle # 깜빡임 상태 반전
    sleep(0.5)
