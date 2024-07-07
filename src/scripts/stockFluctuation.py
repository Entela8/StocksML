from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import yfinance as yf
import json
import sys

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def get_stock_fluctuation(symbol):
    try:
        end_date = date.today()
        start_date = end_date - relativedelta(months=6)

        stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)

        # Check if data is empty
        if stock_data.empty:
            return {"error": f"No data found for {symbol} from {start_date} to {end_date}"}

        # Calculate the price fluctuation
        start_price = stock_data['Close'].iloc[0]
        end_price = stock_data['Close'].iloc[-1]
        fluctuation = end_price - start_price
        fluctuation_percentage = (fluctuation / start_price) * 100

        stock_data.reset_index(inplace=True)
        stock_data['Date'] = stock_data['Date'].astype(str)
        stock_data_dict = stock_data.to_dict(orient='records')

        return {
            "symbol": symbol,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "start_price": start_price,
            "end_price": end_price,
            "fluctuation": fluctuation,
            "fluctuation_percentage": fluctuation_percentage,
            "stock_data": stock_data_dict
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    data = json.loads(sys.argv[1])
    symbol = data.get("stockName")
    if not symbol:
        print(json.dumps({"error": "Missing 'stockName' in input"}))
        sys.exit(1)

    result = get_stock_fluctuation(symbol)
    print(json.dumps(result))
