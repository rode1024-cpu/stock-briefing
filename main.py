import os
from core.data_fetcher import get_market_indices, get_top_movers, get_market_news
from core.ai_generator import generate_briefing
from core.mailer import send_email
from datetime import datetime

def main():
    print("--- Starting US Stock Market Briefing Process ---")
    
    # 1. Fetch Data
    print("Fetching market indices...")
    indices = get_market_indices()
    
    # 2. Determine Session Type (Morning: 6 AM, Midnight: 0 AM)
    current_hour = datetime.now().hour
    session_type = "Morning" if 4 <= current_hour <= 10 else "Midnight"
    print(f"Session Type: {session_type}")

    print(f"Fetching {session_type} movers...")
    gainers, losers = get_top_movers(session_type)
    
    print("Fetching latest news...")
    news = get_market_news()
    
    # 2. Determine Session Type (Morning: 6 AM, Midnight: 0 AM)
    current_hour = datetime.now().hour
    # Mornings are 5-8 AM, Midnights are 23-1 AM (roughly)
    # Since GitHub Actions runs at 21:00 UTC (6 AM KST) and 15:00 UTC (12 AM KST)
    if offset_hour := os.getenv("GITHUB_ACTIONS"): # If running on GitHub, we can be more precise
         # Environment variables are better, but let's use a simple hour check for now
         pass
         
    session_type = "Morning" if 4 <= current_hour <= 8 else "Midnight"
    print(f"Session Type: {session_type}")

    # 3. Generate Content
    print(f"Generating AI {session_type} briefing content...")
    briefing_content = generate_briefing(indices, gainers, losers, news, session_type)
    
    # 3. Send Email
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"[Stock Briefing] {today} 미국 증시 브리핑"
    
    print("Sending email...")
    success = send_email(subject, briefing_content)
    
    if success:
        print("Process completed successfully.")
    else:
        print("Process failed at email step.")

if __name__ == "__main__":
    main()
