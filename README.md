# 🗺️ AI 국내 여행 추천 프로그램

> **여행 날짜만 입력하면, AI가 도시·날씨·행사·맛집·일정을 한 번에 추천!**
>
> LLM API와 지도 API를 조합하여 **하나의 여행 리포트**로 만들어주는 CLI 프로그램입니다.

---

## 📌 프로그램 개요

Python에서 **여러 개의 API를 엮어** 인사이트를 만드는 프로젝트입니다.

```
[여행 날짜 입력]
      │
      ▼
[① LLM API] ──▶ 추천 도시 + 날씨 + 행사 + 이유 (JSON)
      │
      ▼
[② 지도 API] ──▶ 추천 도시의 맛집 5곳 검색
      │
      ▼
[③ LLM API] ──▶ 위 데이터를 합쳐 최종 리포트 생성
      │
      ▼
[결과 저장] ──▶ results/ 폴더에 JSON + Markdown
```

단일 API 호출이 아니라, **한 API의 출력이 다음 API의 입력이 되는 흐름**이 핵심입니다.

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 🤖 **도시 추천** | OpenAI API가 여행 시기에 맞는 도시를 추천 |
| 🌤️ **날씨 요약** | 해당 시기의 일반적인 날씨 정보 제공 |
| 🎉 **행사 안내** | 계절별 추천 행사/축제 1~3개 |
| 🍜 **맛집 검색** | Kakao Local API로 맛집 5곳 검색 (이름·주소·링크) |
| 📅 **일정 추천** | 오전 / 점심 / 오후 / 저녁 하루 코스 |
| 💾 **결과 저장** | JSON(원본 데이터) + Markdown(리포트) 자동 생성 |
| 🛡️ **에러 관리** | 오류 발생 시에도 중단 없이 진행하고 `errors`로 기록 |

---

## 🛠️ 설치 방법

```bash
# 1. 저장소 클론
git clone https://github.com/jmyd051027/travel.git
cd travel

# 2. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. 필요한 패키지 설치
pip install -r requirements.txt
```

> **요구 환경:** Python 3.10 이상

---

## 🔑 API 키 설정 방법

이 프로그램은 **2개의 API 키**가 필요합니다.

| 서비스 | 발급처 | 용도 |
|--------|--------|------|
| OpenAI | https://platform.openai.com | 도시·리포트 추천(LLM) |
| Kakao | https://developers.kakao.com | 맛집 검색(지도) |

### 📄 `.env` 파일 만들기 (권장)

프로젝트 루트에 `.env` 파일을 만들고 아래처럼 입력하세요.

```env
OPENAI_API_KEY=본인의_OpenAI_키
KAKAO_API_KEY=본인의_카카오_REST_API_키
```

### 💻 환경변수로 설정하기 (터미널 세션용)

```bash
# macOS / Linux (현재 세션에만 적용)
export OPENAI_API_KEY="YOUR_KEY"
export KAKAO_API_KEY="YOUR_KEY"

# Windows PowerShell (현재 세션에만 적용)
$env:OPENAI_API_KEY="YOUR_KEY"
$env:KAKAO_API_KEY="YOUR_KEY"
```

---

## 🚨 보안 주의 사항 (매우 중요!)

> ⚠️ **API 키는 절대 코드·README·결과 파일에 직접 작성하지 마세요!**

- ✅ 키는 **`.env` 또는 환경변수**에서만 읽어옵니다.
- ✅ `.env` 파일은 **`.gitignore`에 등록**하여 깃허브에 올라가지 않도록 합니다.
- ✅ 제출물(로그·JSON·Markdown)에 키가 노출되지 않게 확인하세요.

**왜 이렇게 관리하나요?**
1. 협업/공유 시 실수로 키가 공개되는 것을 막습니다.
2. 키를 교체해도 코드를 수정할 필요가 없습니다.
3. 과금·쿼터가 걸린 서비스에서 사고를 예방합니다.

```gitignore
# .gitignore 예시
.env
.venv/
results/
```

---

## 🚀 실행 방법

```bash
python main.py --date 2025-07-15
```

| 옵션 | 설명 | 필수 |
|------|------|:---:|
| `--date` | 여행 날짜 (`YYYY-MM-DD` 형식) | ✅ |

> 날짜 형식이 올바르지 않으면 사용법을 안내하고 종료합니다.

### 🖥️ 실행 예시

```
✅ 입력 완료!
   여행 날짜: 2025-07-15

🤖 AI가 여행 정보를 분석하는 중...
✨ AI 추천 결과:
   🏙️  추천 도시: 강릉
   🌤️  날씨: 7월 중순의 강릉은 덥고 습하지만 바닷바람이...
   🎉 행사: ['경포해수욕장 여름 개장', ...]

🍜 '강릉' 맛집을 검색하는 중...
🍽️ 추천 맛집 목록: (5곳)

💾 저장 완료! → results/강릉_2025-07-15.json
📝 리포트 완성! → results/강릉_2025-07-15.md
```

---

## 📂 결과물 확인 방법

실행하면 `results/` 폴더에 **2개 파일**이 생성됩니다.

```
results/
├── 강릉_2025-07-15.json   # 원본 데이터
└── 강릉_2025-07-15.md     # 최종 여행 리포트
```

### 📄 `도시_날짜.json` — 원본 데이터

```json
{
  "recommendation": { "recommended_city": "...", "weather": "...", "events": [...], "reason": "..." },
  "restaurants": [ { "name": "...", "address": "...", "url": "..." } ],
  "errors": []
}
```

### 📝 `도시_날짜.md` — 최종 리포트

```bash
cat results/강릉_2025-07-15.md
```

추천 지역·이유 / 날씨 / 행사 / 맛집 / 1일 일정이 보기 좋게 정리되어 있습니다.

---

## ✅ 미션 요구사항 충족 체크리스트

| # | 요구사항 | 충족 |
|:-:|----------|:---:|
| 1 | `argparse` 기반 CLI + `--date` 필수 옵션 | ✅ |
| 1 | 날짜 형식 검증 실패 시 사용법 출력 후 종료 | ✅ |
| 2 | LLM: **OpenAI** / 지도: **Kakao Local** 사용 | ✅ |
| 3 | 1차 LLM 출력 JSON 스키마 (`recommended_city`, `weather`, `events`, `reason`) | ✅ |
| 4 | 추천 도시 기준 맛집 5곳 검색 (name·address·url) | ✅ |
| 4 | 맛집 0건이어도 중단 없이 진행 | ✅ |
| 5 | 최종 리포트 Markdown 생성 (지역·날씨·행사·맛집·1일 일정) | ✅ |
| 6 | `try-except`로 API/파싱 오류 처리 | ✅ |
| 6 | API 키 미설정 시 즉시 종료 + 안내 | ✅ |
| 6 | 지도 API 실패 시 "데이터 없음"으로 리포트 계속 진행 | ✅ |
| 6 | LLM JSON 파싱 실패 시 재시도 (최대 1회) | ✅ |
| 6 | 오류를 `errors` 배열로 관리 | ✅ |
| 7 | API 키를 코드에 직접 작성하지 않고 `.env`/환경변수 사용 | ✅ |
| 8 | `results/` 폴더에 JSON(추천+맛집+errors) + `.md` 저장 | ✅ |
| - | Python 3.10 이상, 터미널 실행 | ✅ |

---

## 🎓 이 프로젝트로 배운 것

- **REST API의 요청/응답 구조**와 `GET`/`POST` 메서드의 차이
- **LLM 출력을 JSON으로 구조화**하여 다음 단계(지도 검색) 입력으로 연결하는 흐름
- 외부 API의 대표 오류(**인증 / 쿼터 / 네트워크 / 파싱**)와 대응 원칙
- API 키를 **`.env`/환경변수로 관리**해야 하는 이유

---

## 🧰 사용 기술

- **Python 3.10+**
- **OpenAI API** (LLM)
- **Kakao Local API** (장소 검색)
- `argparse`, `python-dotenv`, `requests`

---

<div align="center">

**Made with ❤️ — 여행 추천 프로그램**

</div>
