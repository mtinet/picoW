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

# 릴레이: GP29 (팬 제어) - 29번으로 고정
relay = Pin(29, Pin.OUT)
relay.value(0) 

# AHT10: I2C0 (GP0: SDA, GP1: SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# ========== 2. 기능 함수 ==========

def set_matrix_fast(temp, hum, status_ok, fan_on, blink, fast_blink):
    matrix.fill((0, 0, 0))
    
    # 1. 온도 표시 (-10~40도, 10칸)
    t_val = (temp + 10) / 5  # -10도면 0.0, 28도면 7.6, 40도면 10.0
    t_count = int(t_val)     # 켜질 개수 (예: 7)
    t_rem = t_val - t_count  # 나머지 (예: 0.6)
    
    t_color = (BRIGHTNESS, 0, 0)
    indices_t = [20, 21, 15, 16, 10, 11, 5, 6, 0, 1]
    
    for i in range(10):
        if i < t_count:
            matrix[indices_t[i]] = t_color
        elif i == t_count and t_rem > 0: # 8번째 칸(인덱스 7)이 깜빡임
            matrix[indices_t[i]] = t_color if blink else (0, 0, 0)

    # 2. 습도 표시 (0~100%, 10칸)
    h_val = hum / 10         # 43%면 4.3
    h_count = int(h_val)     # 켜질 개수 (예: 4)
    h_rem = h_val - h_count  # 나머지 (예: 0.3)
    
    h_color = (0, 0, BRIGHTNESS)
    indices_h = [23, 24, 18, 19, 13, 14, 8, 9, 3, 4]
    
    for i in range(10):
        if i < h_count:
            matrix[indices_h[i]] = h_color
        elif i == h_count and h_rem > 0: # 5번째 칸(인덱스 4)이 깜빡임
            matrix[indices_h[i]] = h_color if blink else (0, 0, 0)
        
    # 3. 가운데 줄 (상태 표시)
    if not status_ok:
        s_color = (BRIGHTNESS, BRIGHTNESS, BRIGHTNESS) if blink else (0, 0, 0)
    elif fan_on:
        # 팬 작동 중: fast_blink 사용 (0.25초마다 반전되어 더 빠르게 깜빡임)
        s_color = (0, BRIGHTNESS, 0) if fast_blink else (0, 0, 0)
    else:
        s_color = (0, BRIGHTNESS, 0)
        
    for i in [2, 7, 12, 17, 22]:
        matrix[i] = s_color
    matrix.write()

# ========== 3. 메인 루프 ==========
blink_toggle = True
HUMIDITY_THRESHOLD = 60

print("🚀 시스템 시작 - 모니터링 중 (Relay: GP29)")

# ========== 3. 메인 루프 ==========
blink_toggle = True
fan_blink_toggle = True # 팬 작동 시 더 빠른 깜빡임용
HUMIDITY_THRESHOLD = 60
counter = 0 # 0.25초 단위 계산을 위한 카운터

print("🚀 시스템 시작 - 모니터링 중 (GP29: Relay)")

while True:
    try:
        # 센서 데이터 읽기
        i2c.writeto(0x38, b'\xAC\x33\x00')
        sleep(0.1)
        data = i2c.readfrom(0x38, 6)
        
        temp = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / 1048576 - 50
        hum = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / 1048576
        
        print(f"온도: {temp:.1f}°C | 습도: {hum:.1f}% | 팬 상태: {'ON' if hum >= HUMIDITY_THRESHOLD else 'OFF'}")
        
        is_fan_on = hum >= HUMIDITY_THRESHOLD
        relay.value(1 if is_fan_on else 0)
        
        # 팬이 켜져 있을 때만 fan_blink_toggle을 빠르게 반전
        if is_fan_on:
            fan_blink_toggle = not fan_blink_toggle
            
        # LED 업데이트 (상태줄에 fan_blink_toggle 전달)
        set_matrix_fast(temp, hum, True, is_fan_on, blink_toggle, fan_blink_toggle)
        
        # 서보 동작
        servo.duty_u16(8192 if temp >= 28 else 1638)
            
    except Exception as e:
        print("❌ 센서 오류:", e)
        set_matrix_fast(0, 0, False, False, blink_toggle, True)
        relay.value(0)
        
    blink_toggle = not blink_toggle 
    sleep(0.25) # 전체 주기를 0.25초로 줄여서 더 빠른 깜빡임 가능하게 함
