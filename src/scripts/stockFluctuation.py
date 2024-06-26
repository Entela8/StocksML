from datetime import date
from dateutil.relativedelta import relativedelta
import yfinance as yf
import json
import sys

def get_stock_fluctuation(symbol):
    end_date = date.today()
    start_date = end_date - relativedelta(months=6)

    stock_data = yf.download(symbol, start=start_date, end=end_date)

    # Check if data is empty
    if stock_data.empty:
        return {"error": f"No data found for {symbol} from {start_date} to {end_date}"}

    # Calculate the price fluctuation
    start_price = stock_data['Close'].iloc[0]
    end_price = stock_data['Close'].iloc[-1]
    fluctuation = end_price - start_price
    fluctuation_percentage = (fluctuation / start_price) * 100

    return {
        "symbol": symbol,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "start_price": start_price,
        "end_price": end_price,
        "fluctuation": fluctuation,
        "fluctuation_percentage": fluctuation_percentage
    }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    data = json.loads(sys.argv[1])
    symbol = data["stockName"]
    result = get_stock_fluctuation(symbol)
    print(json.dumps(result))
