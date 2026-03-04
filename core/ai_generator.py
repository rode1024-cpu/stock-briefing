import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate_briefing(market_data, top_gainers, top_losers, news_items, session_type="Morning"):
    """Generate a briefing using Gemini API with specific templates for Morning/Midnight."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY not found. Please set it in .env file."

    client = genai.Client(api_key=api_key)
    
    # Base instructions for beginner-friendly formatting
    formatting_base = """
당신은 주식 초보자들을 위한 친절한 경제 가이드입니다. 아래 규칙을 반드시 지켜서 작성해 주세요.

[초보자 배려 및 표기 규칙]
1. **용어 설명**: 어려운 주식/경제 용어는 **'한글 용어(영문 용어)'** 형식으로 쓰고, 바로 뒤에 초보자도 이해할 수 있게 아주 쉽게 설명해 주세요. 그리고 그 용어가 이번 이슈에서 **왜 중요한지** 반드시 덧붙여 주세요.
2. **기업명 표기**: 모든 기업은 **'기업명 한글(영어)'** 형식으로 쓰고, 해당 기업이 무엇을 하는 회사인지 한 문장으로 친절하게 설명해 주세요. 어떤 이슈로 주가가 변했는지 구체적으로 말해 주세요.
3. **기관 표기**: 연준 같은 기관은 **'기관명(한국어 읽는법)'** 형식으로 쓰세요 (예: Fed(연준)). 해당 기관의 행보(말, 정책 등)가 시장에 왜 중요한지 이유를 설명해 주세요.
4. **가독성(중요)**: 
   - 문장이 너무 길어지지 않게 **50~70자 내외마다 줄바꿈(<br>)**을 넣어주세요.
   - 내용이 바뀔 때나 설명이 길어질 때는 **단락(<p>)을 자주 나누어** 여유 공간을 만드세요.
5. **디자인**: 
   - 전체는 흰색 배경의 HTML <div>로 감싸세요.
   - 섹션은 '1️⃣' 등 숫자 이모지와 왼쪽 수직 바(|) 디자인을 사용하세요.
   - 상승은 빨간색(#ff4d4d), 하락은 파란색(#4d94ff) 인라인 CSS를 사용하세요.
   - 마크다운 기호 없이 오직 HTML 태그만 사용하세요.
"""

    if session_type == "Morning":
        # Morning (6 AM) Template
        session_prompt = f"""
[오전 6시 브리핑 템플릿 - 반드시 이 순서로 작성]
1. **오늘의 핵심 이슈**: 오늘 미국 시장에서 가장 중요했던 이슈는 무엇이었나요?
2. **오늘의 주인공(가장 많이 오른 종목)**: 어떤 종목이 가장 많이 올랐고, 그 이유는 무엇인가요?
3. **나스닥 100(Nasdaq 100) 현황**: 지수 상황과 기술주들의 중심 이슈를 설명해 주세요.
4. **S&P 500 현황**: 지수 상황과 해당 지수 내 기업 중 이슈가 된 곳을 설명해 주세요.
5. **정치적 이슈**: 주식과 관련된 정치적 사건이 있었나요?
6. **시장 종합**: 그래서 지금 시장 현황이 어떠한 상황인가요?
7. **주간 정치 이슈**: 이번 주 1주일간 있었던 중요한 정치적 이슈들을 정리해 주세요.
"""
    else:
        # Midnight Template
        session_prompt = f"""
[자정 브리핑 템플릿 - 반드시 이 순서로 작성]
*대상 기간: 전일 장 마감 후 ~ 오늘 장 시작 아침까지*
1. **중요 이슈**: 위 기간 동안 어떤 중요한 일이 있었나요?
2. **개장 30분 승자**: 장 시작 후 30분간 가장 많이 오른 종목과 그 이유는?
3. **나스닥 100(Nasdaq 100) 개장 현황**: 장 시작 동안의 지수와 기술주 이슈를 설명해 주세요.
4. **S&P 500 개장 현황**: 지수와 지수 내 기업들의 개장 초기 이슈를 설명해 주세요.
5. **밤사이 정치 이슈**: 전일 마감 후부터 지금까지 주식 관련 정치 이슈는?
6. **시장 종합**: 현재 시장의 개장 초기 분위기가 어떠한가요?
7. **주간 정치 이슈**: 이번 주 1주일간 있었던 중요한 정치적 이슈들을 정리해 주세요.
"""

    full_prompt = formatting_base + session_prompt + f"""
[데이터 자료]
- 시장 데이터: {market_data}
- 상승 종목: {top_gainers}
- 하락 종목: {top_losers}
- 뉴스: {news_items}

설명 없이 오직 <div>로 시작하는 HTML 코드만 출력하세요.
"""

    import time
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            content = response.text.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                if content.endswith("```"):
                    content = content.rsplit("\n", 1)[0]
            return content
        except Exception as e:
            if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and attempt < 2:
                time.sleep(65)
                continue
            else:
                return f"<div>에러 발생: {str(e)}</div>"
    return "<div>요청 초과. 다시 시도해 주세요.</div>"
