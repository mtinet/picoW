import time
from neopixel import Neopixel

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 25
PIO = 0
Pin = 16

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(150)

# 각 문자의 5x5 매트릭스 정의 ('L', 'O', 'V', 'E')
letters = {
    'L': [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    'O': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ],
    'V': [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
    ],
    'E': [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ]
}

# 문자를 매트릭스에 출력하는 함수
def display_letter(letter, color):
    for y in range(5):
        for x in range(5):
            if letters[letter][y][x] == 1:
                strip.set_pixel(y * 5 + x, color)
            else:
                strip.set_pixel(y * 5 + x, (0, 0, 0))
    strip.show()

# 문자열을 흘러가게 하는 함수
def scroll_text(text, color, wait):
    for letter in text:
        display_letter(letter, color)
        time.sleep(wait)
        clear_matrix()
        
# 매트릭스 초기화 함수
def clear_matrix():
    for i in range(numpix):
        strip.set_pixel(i, (0, 0, 0))
    strip.show()

# 애니메이션 실행
while True:
    scroll_text("LOVE", (255, 0, 0), 0.5)  # 빨간색 "LOVE" 텍스트, 0.5초 간격으로 이동
