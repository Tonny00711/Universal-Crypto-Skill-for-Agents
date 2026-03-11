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

    try:
        params = {"symbol": symbol}
        response = requests.get(base_url, params=params, timeout=5)
        
        # 处理币对不存在的情况
        if response.status_code == 400:
            return {"error": f"交易对 {symbol} 无效，请检查名称。"}
            
        response.raise_for_status()
        data = response.json()
        
        return {
            "symbol": data["symbol"],
            "price": float(data["price"]),
            "timestamp": int(time.time() * 1000),
            "source": "Binance"
        }
        
    except Exception as e:
        return {"error": f"API 调用失败: {str(e)}"}

# 开发者自测
if __name__ == "__main__":
    print(get_crypto_price("BTC"))
