import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 사용 가능한 모델 목록 출력
models = client.models.list()
for m in models.data:
    print(m.id)