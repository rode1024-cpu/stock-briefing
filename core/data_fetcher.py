import yfinance as yf
import feedparser
from datetime import datetime, timedelta

def get_market_indices():
    """Fetch S&P 500 and Nasdaq 100 data."""
    indices = {
        'S&P 500': '^GSPC',
        'Nasdaq 100': '^IXIC'
    }
    results = {}
    for name, ticker in indices.items():
        data = yf.Ticker(ticker)
        # Period 2d to get prev close and current
        hist = data.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            curr_close = hist['Close'].iloc[-1]
            # Also get today's Open for Midnight session
            today_open = hist['Open'].iloc[-1]
            pct_change = ((curr_close - prev_close) / prev_close) * 100
            open_change = ((curr_close - today_open) / today_open) * 100
            
            results[name] = {
                'price': round(curr_close, 2),
                'change_pct': round(pct_change, 2),
                'open_change_pct': round(open_change, 2) # Change since market open
            }
    return results

def get_top_movers(session_type="Morning"):
    """
    Fetch top gainers and losers. 
    If Midnight, we check change from Open price.
    """
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JNJ", "V", "AMD", "NFLX", "AVGO"]
    movers = []
    for t in tickers:
        stock = yf.Ticker(t)
        hist = stock.history(period="1d") # Just today's data for opening check
        hist_prev = stock.history(period="2d")
        
        if not hist.empty and len(hist_prev) >= 2:
            prev_close = hist_prev['Close'].iloc[-2]
            curr_price = hist['Close'].iloc[-1]
            open_price = hist['Open'].iloc[-1]
            
            # Morning uses Prev Close, Midnight uses Today's Open (for opening 30 min check)
            if session_type == "Midnight":
                change = ((curr_price - open_price) / open_price) * 100
            else:
                change = ((curr_price - prev_close) / prev_close) * 100
                
            movers.append({
                'ticker': t,
                'name': stock.info.get('longName', t),
                'change_pct': round(change, 2),
                'summary': stock.info.get('longBusinessSummary', 'Description not available.')[:150] + '...'
            })
    
    movers.sort(key=lambda x: x['change_pct'], reverse=True)
    return movers[:5], movers[-5:] # Return top 5 gainers/losers

def get_market_news():
    """Fetch daily and weekly political/financial news."""
    # Daily news (today)
    daily_url = "https://news.google.com/rss/search?q=US+stock+market+politics+today&hl=en-US&gl=US&ceid=US:en"
    # Weekly news (last 7 days)
    weekly_url = "https://news.google.com/rss/search?q=US+stock+market+politics+weekly+summary&hl=en-US&gl=US&ceid=US:en"
    
    daily_feed = feedparser.parse(daily_url)
    weekly_feed = feedparser.parse(weekly_url)
    
    news = {
        'today': [],
        'weekly': []
    }
    
    for entry in daily_feed.entries[:8]:
        news['today'].append(entry.title)
    
    for entry in weekly_feed.entries[:5]:
        news['weekly'].append(entry.title)
        
    return news

if __name__ == "__main__":
    print(get_market_indices())
    print(get_top_movers("Midnight")[0])
    print(get_market_news())
