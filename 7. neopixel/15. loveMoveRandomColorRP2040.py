import time
import random
from neopixel import Neopixel

# 네오픽셀의 셀 갯수, PIO상태, 핀번호 정의 
numpix = 25
PIO = 0
Pin = 16

# 네오픽셀이 RGB타입일 때 네오픽셀 수, PIO상태, 핀번호, 네오픽셀 타입 순으로 선택, 밝기 지정 
strip = Neopixel(numpix, PIO, Pin, "RGB")

# 밝기 설정(0~255)
strip.brightness(30)

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
def display_letter(letter, color, offset_x):
    for y in range(5):
        for x in range(5):
            if 0 <= x + offset_x < 5:  # 매트릭스 범위 내에서만 표시
                if letters[letter][y][x] == 1:
                    strip.set_pixel(y * 5 + (x + offset_x), color)
                else:
                    strip.set_pixel(y * 5 + (x + offset_x), (0, 0, 0))

# 무작위 색상을 생성하는 함수
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# 문자열을 흘러가게 하는 함수
def scroll_text(text, wait):
    total_length = len(text) * 5  # 전체 문자열의 길이 (각 글자는 5열)
    
    for offset in range(total_length + 5 + 5):  # 문자열이 완전히 지나갈 때까지 (5는 매트릭스의 넓이)
        clear_matrix()
        
        current_char_index = (offset // 5) - 1  # 현재 표시할 문자 인덱스 (시작을 오른쪽 끝에서 하기 위해 -1)
        char_offset = offset % 5  # 현재 문자의 x축 오프셋

        # 새로운 랜덤 색상 생성
        color = random_color()

        if current_char_index >= 0 and current_char_index < len(text):
            display_letter(text[current_char_index], color, -char_offset)
        
        if current_char_index + 1 < len(text) and char_offset > 0:
            display_letter(text[current_char_index + 1], color, 5 - char_offset)
        
        strip.show()
        time.sleep(wait)

# 매트릭스 초기화 함수
def clear_matrix():
    for i in range(numpix):
        strip.set_pixel(i, (0, 0, 0))
    strip.show()

# 애니메이션 실행
while True:
    scroll_text("LOVE", 0.1)  # 0.1초 간격으로 이동
