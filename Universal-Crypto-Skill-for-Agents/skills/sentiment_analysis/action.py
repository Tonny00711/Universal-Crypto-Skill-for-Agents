import random
import time

def get_market_sentiment(symbol: str):
    """
    模拟多维情绪分析接口。
    实际版本将接入 CryptoPanic 或 Alternative.me (Fear & Greed Index) API。
    """
    symbol = symbol.upper().strip()
    
    # 模拟 API 逻辑
    sources = ["News", "Social Media", "On-chain Data"]
    sentiment_score = random.uniform(20, 90)  # 0-100 评分
    
    if sentiment_score > 70:
        label = "Strongly Bullish"
    elif sentiment_score > 55:
        label = "Bullish"
    elif sentiment_score > 45:
        label = "Neutral"
    elif sentiment_score > 30:
        label = "Bearish"
    else:
        label = "Strongly Bearish"

    return {
        "symbol": symbol,
        "score": round(sentiment_score, 2),
        "label": label,
        "weighted_sources": sources,
        "timestamp": int(time.time()),
        "notice": "Commercial Version: Nova Architecture Studio Private Access required for real-time live scoring."
    }

if __name__ == "__main__":
    print(get_market_sentiment("BTC"))
