import requests
import os
from dotenv import load_dotenv

# .env에서 키 불러오기
load_dotenv()
KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")

# Kakao 장소 검색 주소
url = "https://dapi.kakao.com/v2/local/search/keyword.json"

# 인증 정보 (헤더)
headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}

# 검색어
params = {"query": "경복궁"}

# 요청 보내기!
response = requests.get(url, headers=headers, params=params)

# 결과 출력
print(response.json())