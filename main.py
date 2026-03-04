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
    
    print("Fetching top movers...")
    gainers, losers = get_top_movers()
    
    print("Fetching latest news...")
    news = get_market_news()
    
    # 2. Generate Content
    print("Generating AI briefing content...")
    briefing_content = generate_briefing(indices, gainers, losers, news)
    
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
