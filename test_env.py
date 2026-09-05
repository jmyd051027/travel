import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
kakao_key = os.getenv("KAKAO_REST_API_KEY")

print("OpenAI:", "✅" if openai_key else "❌")
print("Kakao :", "✅" if kakao_key else "❌")
