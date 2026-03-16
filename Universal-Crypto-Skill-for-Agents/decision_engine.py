import time
from skills.crypto_price.action import get_crypto_price
from skills.sentiment_analysis.action import get_market_sentiment

def run_decision_engine(symbol="BTC"):
    """
    MVP: 综合决策引擎
    逻辑：波动 > 2% (相对于起始价) 且 情绪为 Bearish 相关时触发警报
    """
    print(f"[*] Starting Nova Decision Engine MVP for {symbol}...")
    
    # 记录初始价格
    initial_data = get_crypto_price(symbol)
    if "error" in initial_data:
        print(f"[!] Error: {initial_data['error']}")
        return
    
    # 记录初始价格
    initial_data = get_crypto_price(symbol)
    if "error" in initial_data:
        # 如果 API 失败，使用当前市场大概值作为 fallback
        base_price = 65000.0
        print(f"[!] API Notice: {initial_data['error']}. Using fallback base: ${base_price}")
    else:
        base_price = initial_data["price"]
        print(f"[*] Base price locked: ${base_price}")

    while True:
        # 1. 获取实时价格
        current_data = get_crypto_price(symbol)
        if "error" in current_data:
            time.sleep(10)
            continue
        
        current_price = current_data["price"]
        price_change = ((current_price - base_price) / base_price) * 100
        
        # 2. 获取实时情绪
        sentiment_data = get_market_sentiment(symbol)
        sentiment_label = sentiment_data["label"]

        print(f"[*] Check: ${current_price:.2f} ({price_change:+.2f}%) | Sentiment: {sentiment_label}")

        # 3. 综合判定逻辑
        if abs(price_change) > 2.0 and "Bearish" in sentiment_label:
            alert_msg = (
                f"[NOVA ALERT] {symbol} RISK DETECTED\n"
                f"Price: ${current_price:.2f} ({price_change:+.2f}%)\n"
                f"Sentiment: {sentiment_label} (High Risk!)\n"
                f"Action: Consider immediate hedging or exit."
            )
            print("\n" + alert_msg + "\n")
            return alert_msg

        time.sleep(60) # 生产环境轮询间隔建议 1 分钟


if __name__ == "__main__":
    run_decision_engine("BTC")
