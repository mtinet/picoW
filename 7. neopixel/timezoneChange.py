import urequests

def timeOfSeoul():
    # ✅ 올바른 시간 정보 가져오기
    url = "https://timejson.netlify.app/.netlify/functions/time"
    
    try:
        time_dict = urequests.get(url).json()
        
        # ✅ UTC 시간 가져오기
        utc_time_str = time_dict["time"]  # 예: "2025-03-08T13:20:20.850Z"
        date_str = time_dict["date"]  # 예: "2025-03-08"
        
        # ✅ 시간 추출 (ISO 8601 포맷 기준)
        year = int(date_str[:4])  # "2025-03-08" → 2025
        month = int(date_str[5:7])  # "2025-03-08" → 03
        day = int(date_str[8:10])  # "2025-03-08" → 08
        hour = int(utc_time_str[11:13])  # "2025-03-08T13:20:20.850Z" → 13
        minute = int(utc_time_str[14:16])  # "2025-03-08T13:20:20.850Z" → 20
        second = int(utc_time_str[17:19])  # "2025-03-08T13:20:20.850Z" → 20
        
        # ✅ KST 변환 (UTC+9)
        hour += 9
        if hour >= 24:
            hour -= 24
            day += 1  # 날짜 조정
        
        # ✅ 변환된 시간을 출력
        output_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} KST".format(year, month, day, hour, minute, second)
        return output_str

    except Exception as e:
        return f"❌ Error: {e}"

