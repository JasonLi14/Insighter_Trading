import yfinance as yf
import pandas as pd

from accounts.models import stocks

def getHistory(ticker: str, period: int = 3) -> pd.DataFrame:
    # Convert int to a period
    interval = "1d"
    match period:
        case 1:
            time = "1d"
            interval = "5m"
        case 2:
            time = "5d"
            interval = "1h"
        case 3:
            time = "1mo"
        case 4:
            time = "3mo"
        case 5:
            time = "6mo"
        case _:
            time = "1y"

    ticker_obj = yf.Ticker(ticker)
    company_name = stocks.objects.filter(ticker=ticker).values()[0]["name"]
    fast_info = ticker_obj.get_fast_info()
    history = ticker_obj.history(period=time, interval=interval)["Close"]
    history = history.tz_convert(None)
    return history, company_name, fast_info


def getStats(ticker: str) -> pd.DataFrame:
    ticker_obj = yf.Ticker(ticker)
    fast_info = ticker_obj.fast_info
    stats = {
        "Last Price": fast_info['lastPrice'],
        "High": fast_info['dayHigh'],
        "Low": fast_info['dayLow'],
        "Open": fast_info['open'],
        "Previous Close": fast_info['previousClose'],
        "Volume": fast_info['lastVolume'],
        "Market Cap": fast_info['marketCap'],
    }
    return stats


if __name__ == "__main__":
    print(getHistory("AAPL", 1))
