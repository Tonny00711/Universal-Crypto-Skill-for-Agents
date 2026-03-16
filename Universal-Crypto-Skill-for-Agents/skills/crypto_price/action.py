import requests
import time

def get_crypto_price(symbol: str):
    """
    通过币安公开 API 执行实时查价。
    """
    base_url = "https://api.binance.com/api/v3/ticker/price"
    
    # 格式清理：确保是大写并处理常见的缩写
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT") and symbol in ["BTC", "ETH", "BNB", "SOL"]:
        symbol += "USDT"

    # 尝试多个数据源以应对地区限制
    sources = [
        ("Binance", "https://api.binance.com/api/v3/ticker/price", {"symbol": symbol}),
        ("Binance-US", "https://api.binance.us/api/v3/ticker/price", {"symbol": symbol}),
        ("CoinGecko", f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower().replace('usdt','')}&vs_currencies=usd", {})
    ]

    for name, url, params in sources:
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if name.startswith("Binance"):
                    price = float(data["price"])
                else:
                    # CoinGecko format
                    coin_id = symbol.lower().replace('usdt','')
                    price = float(data[coin_id]["usd"])
                
                return {
                    "symbol": symbol,
                    "price": price,
                    "timestamp": int(time.time() * 1000),
                    "source": name
                }
        except:
            continue

    return {"error": f"所有数据源调用失败，请检查网络连接。"}

# 开发者自测
if __name__ == "__main__":
    print(get_crypto_price("BTC"))
