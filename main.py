# 필요한 도구들 가져오기
import argparse
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# 환경변수 로드 (.env 파일에서 API 키 불러오기)
load_dotenv()

# API 키 확인 (없으면 즉시 종료!)
if not os.getenv("OPENAI_API_KEY"):
    print("❌ OPENAI_API_KEY가 없어요!")
    print("💡 .env 파일에 키를 설정해주세요:")
    print('   OPENAI_API_KEY="your-key-here"')
    exit()

if not os.getenv("KAKAO_REST_API_KEY"):
    print("❌ KAKAO_REST_API_KEY가 없어요!")
    print("💡 .env 파일에 키를 설정해주세요:")
    exit()

# AI 클라이언트 준비 (전선 연결! ⚡)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 카카오 키 불러오기 ← 추가!
KAKAO_KEY = os.getenv("KAKAO_REST_API_KEY")

def search_places(keyword):
    """카카오맵에서 장소를 검색하는 함수"""
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_KEY}"}
    params = {"query": keyword, "size": 5}

    try:
        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        restaurants = []
        for place in result["documents"]:
            restaurant = {
                "name": place["place_name"],
                "address": place["address_name"],
                "category": place["category_name"],
                "url": place["place_url"],
                "x": place["x"],
                "y": place["y"]
            }
            restaurants.append(restaurant)

        return restaurants  # 성공하면 목록 반환

    except Exception as e:
        print(f"⚠️ 맛집 검색 실패: {e}")
        return []  # 실패해도 빈 목록 반환 (안 죽음!)

    # 📦 필요한 정보만 깔끔하게 정리!
    restaurants = []
    for place in result["documents"]:
        restaurant = {
            "name": place["place_name"],
            "address": place["address_name"],
            "category": place["category_name"],
            "url": place["place_url"],
            "x": place["x"],
            "y": place["y"]
        }
        restaurants.append(restaurant)

    return restaurants

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

# ⑤ 🤖 AI에게 여행 정보 요청하기 (JSON으로!)
print("\n🤖 AI가 여행 정보를 분석하는 중...")

# AI에게 JSON 형식으로 답하라고 요청! ⭐
prompt = f"""
{date}에 국내 여행하기 좋은 도시를 추천해줘.
반드시 아래 JSON 형식으로만 답해줘. 다른 말은 하지마.

{{
  "recommended_city": "도시이름",
  "weather": "이 시기의 일반적인 날씨 요약",
  "events": ["행사1", "행사2"],
  "reason": "추천 이유 2~4문장",
  "schedule": {{
    "morning": "오전 일정",
    "lunch": "점심 추천",
    "afternoon": "오후 일정",
    "evening": "저녁 일정"
  }}
}}
"""

 # errors 목록 준비! (요구사항 6, 8번)
errors = []

# JSON 파싱 시도 (실패하면 1번 재시도!)
travel_info = None

for attempt in range(2):  # 0, 1 → 총 2번 시도
    try:
        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[{"role": "user", "content": prompt}]
        )
        answer_text = response.choices[0].message.content.strip()
        travel_info = json.loads(answer_text)  # 변환 시도!
        break  # 성공하면 반복 끝!

    except json.JSONDecodeError:
        print(f"⚠️ JSON 파싱 실패 (시도 {attempt + 1}/2)")
        if attempt == 0:
            print("   다시 요청할게요...")
        else:
            errors.append("LLM JSON 파싱 최종 실패")

    except Exception as e:
        print(f"⚠️ AI 요청 실패: {e}")
        errors.append(f"AI 요청 실패: {e}")
        break

# 2번 다 실패하면? 프로그램 종료!
if travel_info is None:
    print("❌ AI 추천을 받지 못했어요. 종료합니다.")
    exit()


# ⑦ 변환된 정보 꺼내서 확인
city = travel_info["recommended_city"]
weather = travel_info["weather"]
events = travel_info["events"]
reason = travel_info["reason"]
schedule = travel_info["schedule"]

print("\n✨ AI 추천 결과:")
print(f"   🏙️  추천 도시: {city}")
print(f"   🌤️  날씨: {weather}")
print(f"   🎉 행사: {events}")
print(f"   💬 이유: {reason}")

# ⑧ 🍜 추천 도시로 맛집 검색! (관광지 → 맛집)
print(f"\n🍜 '{city}' 맛집을 검색하는 중...")

restaurants = search_places(f"{city} 맛집")

# ⑨ 맛집 목록 출력 (지도 링크 포함!)
print("\n🍽️ 추천 맛집 목록:")
for r in restaurants:
    print(f"   - {r['name']}")
    print(f"     📍 {r['address']}")
    print(f"     🔗 {r['url']}")

    # ⑩ 📁 결과를 파일로 저장하기!
import os

# results 폴더 없으면 만들기
os.makedirs("results", exist_ok=True)

# 저장할 내용 하나로 모으기
save_data = {
    "date": date,              # 여행 날짜
    "travel_info": travel_info, # AI 추천 정보
    "restaurants": restaurants  # 맛집 목록
}

# 파일 이름 만들기 (도시_날짜.json)
filename = f"results/{city}_{date}.json"

# JSON 파일로 저장! (한글 깨짐 방지!)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(save_data, f, ensure_ascii=False, indent=2)

print(f"\n💾 저장 완료! → {filename}")

# ⑪ 📝 예쁜 여행 리포트 만들기 (Markdown)
md_filename = f"results/{city}_{date}.md"

with open(md_filename, "w", encoding="utf-8") as f:
    f.write(f"# 🗺️ {city} 여행 가이드\n\n")
    f.write(f"**📅 여행 날짜:** {date}\n\n")
    
    f.write(f"## 🌤️ 날씨\n{travel_info['weather']}\n\n")
    
    f.write(f"## 🎉 추천 행사\n")
    for event in travel_info['events']:
        f.write(f"- {event}\n")
    f.write("\n")
    
    f.write(f"## 💬 추천 이유\n{travel_info['reason']}\n\n")
    
    f.write(f"## 📅 추천 일정\n")
    f.write(f"- 🌅 **오전:** {schedule['morning']}\n")
    f.write(f"- 🍽️ **점심:** {schedule['lunch']}\n")
    f.write(f"- ☀️ **오후:** {schedule['afternoon']}\n")
    f.write(f"- 🌙 **저녁:** {schedule['evening']}\n\n")
    
    f.write(f"## 🍽️ 추천 맛집\n")
    for r in restaurants:
        f.write(f"### {r['name']}\n")
        f.write(f"- 📍 {r['address']}\n")
        f.write(f"- 🔗 [지도 보기]({r['url']})\n\n")

print(f"📝 리포트 완성! → {md_filename}")