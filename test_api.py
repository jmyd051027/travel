# .env 파일에서 키를 불러오는 도구 가져오기
import os
from dotenv import load_dotenv

# .env 파일 내용을 불러오기
load_dotenv()

# OPENAI_API_KEY라는 이름의 키를 꺼내오기
api_key = os.getenv("OPENAI_API_KEY")

# 키가 잘 들어왔는지 확인하기
if api_key:
    print("✅ 키를 잘 불러왔어요!")
    print("키 앞부분:", api_key[:10] + "...")  # 보안상 앞 10글자만 표시
else:
    print("❌ 키를 못 찾았어요. .env 파일을 확인해주세요.")