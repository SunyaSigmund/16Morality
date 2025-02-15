import requests
import time

# Render에서 배포된 Flask 웹사이트의 URL (네 주소로 변경)
URL = "https://one6morality.onrender.com"

def keep_server_awake():
    while True:
        try:
            response = requests.get(URL)
            print(f"🔄 요청 보냄! 응답 코드: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 오류 발생: {e}")
        
        # 10분(600초)마다 요청 보내기
        time.sleep(600)

if __name__ == "__main__":
    keep_server_awake()
