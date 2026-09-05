# 필요한 도구들 가져오기
import argparse
import os
import requests                    # ← 카카오맵 요청용 추가!
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 로드 (.env 파일에서 API 키 불러오기)
load_dotenv()

# AI 클라이언트 준비 (전선 연결! ⚡)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 카카오 키 불러오기 ← 추가!
KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")


# 🗺️ 카카오맵 장소 검색 함수 ← 추가!
def search_places(keyword):
    """카카오맵에서 장소를 검색하는 함수"""
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    params = {"query": keyword}

    response = requests.get(url, headers=headers, params=params)
    return response.json()


# ① 사용자가 입력할 항목 정의하기
parser = argparse.ArgumentParser(description="AI 여행 추천 프로그램")
parser.add_argument("--date", required=True, help="여행 날짜 (예: 2025-06-15)")

# ② 입력한 값 꺼내오기
args = parser.parse_args()
date = args.date

# ③ 날짜 형식이 올바른지 확인하기
try:
    datetime.strptime(date, "%Y-%m-%d")
except ValueError:
    print("❌ 날짜 형식이 틀렸어요! 예시처럼 입력해주세요: 2025-06-15")
    exit()

# ④ 입력값 확인 출력
print(f"✅ 입력 완료!")
print(f"   여행 날짜: {date}")

# ⑤ 🤖 AI에게 도시 추천 요청하기
print("\n🤖 AI가 도시를 추천하는 중...")

response = client.chat.completions.create(
    model="gpt-5.5",  # 저렴하고 빠른 모델!
    messages=[
        {"role": "user", "content": f"{date}에 국내 여행하기 좋은 도시 1곳만 '도시이름'만 한 단어로 답해줘. 다른 말은 하지마."}
    ]
)

# ⑥ AI 답변 꺼내서 도시 이름 저장 ← 살짝 수정!
city = response.choices[0].message.content.strip()
print("\n✨ AI 추천 도시:", city)

# ⑦ 🗺️ 추천 도시로 카카오맵 검색! ← 추가!
print(f"\n🗺️ '{city}' 관광지를 검색하는 중...")

result = search_places(f"{city} 관광지")

# ⑧ 검색 결과에서 장소 이름 출력 ← 추가!
print("\n📍 추천 장소 목록:")
for place in result["documents"][:5]:   # 상위 5개만!
    print(f"   - {place['place_name']} ({place['address_name']})")