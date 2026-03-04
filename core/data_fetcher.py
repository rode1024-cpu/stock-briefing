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
        # Get historical data for the last 2 sessions to calculate change
        hist = data.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            curr_close = hist['Close'].iloc[-1]
            pct_change = ((curr_close - prev_close) / prev_close) * 100
            results[name] = {
                'price': round(curr_close, 2),
                'change_pct': round(pct_change, 2)
            }
    return results

def get_top_movers():
    """
    Fetch top gainers and losers. 
    Note: yfinance doesn't provide a direct 'top gainers' list easily for a specific index.
    In a real scenario, we might scrape or use a more comprehensive API.
    For this POC, we'll fetch a few major tech stocks as a proxy or use yfinance's generic trending.
    """
    # Placeholder: In a full version, we'd list S&P 500 components or use a scraping approach.
    # For now, let's fetch a list of representative high-volume stocks.
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "BRK-B", "JNJ", "V"]
    movers = []
    for t in tickers:
        stock = yf.Ticker(t)
        hist = stock.history(period="2d")
        if len(hist) >= 2:
            prev = hist['Close'].iloc[-2]
            curr = hist['Close'].iloc[-1]
            change = ((curr - prev) / prev) * 100
            movers.append({
                'ticker': t,
                'name': stock.info.get('longName', t),
                'change_pct': round(change, 2),
                'summary': stock.info.get('longBusinessSummary', 'No description available.')[:200] + '...'
            })
    
    # Sort by change percentage
    movers.sort(key=lambda x: x['change_pct'], reverse=True)
    top_gainers = movers[:3]
    top_losers = movers[-3:]
    return top_gainers, top_losers

def get_market_news():
    """Fetch US political and financial news via RSS."""
    # Using Google News RSS for high-level summaries
    rss_url = "https://news.google.com/rss/search?q=US+stock+market+politics&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    news_items = []
    for entry in feed.entries[:5]: # Take top 5 news
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })
    return news_items

if __name__ == "__main__":
    # Test
    print("Market Indices:", get_market_indices())
    g, l = get_top_movers()
    print("Top Gainers:", g)
    print("News:", get_market_news())
