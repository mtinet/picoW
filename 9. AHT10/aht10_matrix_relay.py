from time import sleep
from machine import Pin, PWM, I2C
import neopixel

# ========== 1. 하드웨어 설정 ==========
matrix = neopixel.NeoPixel(Pin(16), 25)
BRIGHTNESS = 20

# 서보모터: GP2
servo = PWM(Pin(2))
servo.freq(50)

# 릴레이 제어: GP6
# 초기값은 LOW(꺼짐)로 설정
relay = Pin(6, Pin.OUT)
relay.value(0) 

# AHT10: I2C0 (GP0: SDA, GP1: SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# ========== 2. 기능 함수 ==========

def set_matrix(temp, hum, status_ok, blink_state):
    matrix.fill((0, 0, 0))
    
    # 온도 표시 (-10~40도, 10칸)
    t_count = min(10, max(0, int((temp + 10) / 5))) 
    t_color = (BRIGHTNESS, 0, 0)
    indices_t = [20, 21, 15, 16, 10, 11, 5, 6, 0, 1]
    for i in range(t_count):
        matrix[indices_t[i]] = t_color

    # 습도 표시 (0~100%, 10칸)
    h_count = min(10, max(0, int(hum / 10)))
    h_color = (0, 0, BRIGHTNESS)
    indices_h = [23, 24, 18, 19, 13, 14, 8, 9, 3, 4]
    for i in range(h_count):
        matrix[indices_h[i]] = h_color
        
    # 상태줄 표시
    if status_ok:
        s_color = (0, BRIGHTNESS, 0)
    else:
        s_color = (BRIGHTNESS, BRIGHTNESS, BRIGHTNESS) if blink_state else (0, 0, 0)
    for i in [2, 7, 12, 17, 22]:
        matrix[i] = s_color
    matrix.write()

# ========== 3. 메인 루프 ==========
blink = True
HUMIDITY_THRESHOLD = 60 # 습도 60% 이상이면 팬 가동

while True:
    try:
        i2c.writeto(0x38, b'\xAC\x33\x00')
        sleep(0.1)
        data = i2c.readfrom(0x38, 6)
        temp = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / 1048576 - 50
        hum = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / 1048576
        
        print(f"온도: {temp:.1f}°C | 습도: {hum:.1f}%")
        set_matrix(temp, hum, True, True)
        
        # 팬 제어 (릴레이)
        if hum >= HUMIDITY_THRESHOLD:
            relay.value(1) # 팬 켜기 (HIGH)
            print("💨 습도 높음: 팬 가동")
        else:
            relay.value(0) # 팬 끄기 (LOW)
            
        # 서보 동작
        servo.duty_u16(8192 if temp >= 28 else 1638)
            
    except Exception as e:
        print("❌ 센서 오류:", e)
        set_matrix(0, 0, False, blink)
        relay.value(0) # 오류 시 안전을 위해 팬 정지
        blink = not blink
        
    sleep(0.5)
