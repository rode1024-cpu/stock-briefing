import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def generate_briefing(market_data, top_gainers, top_losers, news_items):
    """Generate a briefing using Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "GEMINI_API_KEY not found. Please set it in .env file."

    client = genai.Client(api_key=api_key)
    
    # Construct a highly detailed prompt for premium HTML design
    prompt = f"""
당신은 대한민국 최고의 경제 뉴스레터 '머니스타드'의 메인 에디터입니다. 
제공된 데이터를 활용하여 개인 투자자들을 위한 **프리미엄 아침 브리핑**을 작성해 주세요. 

[디자인 요구사항 - 반드시 준수]
1. **전체 구조**: 깔끔한 흰색 배경의 HTML 이메일 형식으로 작성하세요.
2. **헤더**: 가장 상단에 오늘의 핵심을 찌르는 제목을 <h1> 태그로 가운데 정렬해 배치하세요.
3. **인트로**: 어제 시장의 흐름을 관통하는 한 문장 요약을 인용구 스타일(옅은 회색 배경, 기울임꼴)로 배치하세요.
4. **섹션 구분**: 
   - '1️⃣ 지수 브리핑', '2️⃣ 특징주 분석' 등 숫자 이모지와 함께 왼쪽 수직 바(|) 디자인을 적용한 헤더를 사용하세요.
   - 각 섹션 사이에는 <hr> 태그나 충분한 공백을 주어 가독성을 높이세요.
5. **텍스트 스타일**: 
   - 중요 키워드와 수치는 <b> 태그를 사용하세요.
   - 상승률은 빨간색(#ff4d4d), 하락률은 파란색(#4d94ff)으로 강조하세요 (인라인 CSS color 속성 사용).
   - '📌', '→', '📍' 이모지를 적재적소에 배치하세요.
6. **내용 구성**: 
   - [지수] S&P 500과 나스닥 지수의 변화량을 설명하세요.
   - [종목] 상승/하락 TOP 3 종목에 대해, 그 회사가 **무슨 일을 하는 회사인지**를 아주 쉽고 친근하게 설명하세요.
   - [뉴스/이슈] 현재 시장을 흔드는 정치/경제적 이슈를 전문가의 시선에서 풀어서 설명하세요.
   - [포인트] 오늘 하루 주목해야 할 변수를 '관전 포인트'로 정리해 주세요.

[제약 사항]
- 본문은 반드시 <div> 태그로 감싸진 완벽한 HTML이어야 합니다.
- 마크다운 기호(###, **, - 등)는 절대 사용하지 말고 오직 HTML 태그만 사용하세요.
- 답변에 설명이나 인사말 없이 오직 HTML 코드만 출력하세요.

[데이터 자료]
- 시장 지수: {market_data}
- 상승 종목: {top_gainers}
- 하락 종목: {top_losers}
- 주요 뉴스: {news_items}
"""

    import time
    
    for attempt in range(3): # 최대 3번 시도
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            content = response.text.strip()
            # AI가 마크다운 코드 블록(```html)을 포함할 경우 제거
            if content.startswith("```"):
                content = content.split("\n", 1)[-1]
                if content.endswith("```"):
                    content = content.rsplit("\n", 1)[0]
            return content
        except Exception as e:
            if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and attempt < 2:
                print(f"AI 사용량 초과로 잠시 대기 중... (시도 {attempt + 1}/3)")
                time.sleep(65)
                continue
            else:
                return f"<div>에러가 발생했습니다: {str(e)}</div>"
    
    return "<div>재시도 횟수를 초과했습니다. 잠시 후 다시 시도해 주세요.</div>"
