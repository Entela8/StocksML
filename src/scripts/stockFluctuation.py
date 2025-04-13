from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import yfinance as yf
import json
import sys
import warnings
import logging

# Supprimer tous les warnings, y compris ceux qui pourraient sortir dans stdout
warnings.filterwarnings("ignore")

# Supprimer tous les logs de yfinance
logging.getLogger().handlers.clear()
logging.basicConfig(level=logging.CRITICAL)

def get_stock_fluctuation(symbol):
    try:
        end_date = date.today()
        start_date = end_date - relativedelta(months=6)

        stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False, auto_adjust=True)

        if stock_data.empty:
            return {"error": f"No data found for {symbol} from {start_date} to {end_date}"}

        start_price = stock_data['Close'].iloc[0].item()
        end_price = stock_data['Close'].iloc[-1].item()

        fluctuation = end_price - start_price
        fluctuation_percentage = (fluctuation / start_price) * 100

        # After downloading the data and before resetting index:
        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = [col[0] for col in stock_data.columns]  # Drop second part (like 'AAPL')

        # Reset index to turn 'Date' into a column
        stock_data.reset_index(inplace=True)

        # Convert to dictionary

        for col in stock_data.columns:
            if pd.api.types.is_datetime64_any_dtype(stock_data[col]):
                stock_data[col] = stock_data[col].astype(str)

        stock_data_dict = stock_data.to_dict(orient='records')

        return {
            "symbol": symbol,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "start_price": float(start_price),
            "end_price": float(end_price),
            "fluctuation": float(fluctuation),
            "fluctuation_percentage": float(fluctuation_percentage),
            "stock_data": stock_data_dict
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Invalid arguments"}))
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        symbol = data.get("stockName")
        if not symbol:
            raise ValueError("Missing 'stockName' in input")

        result = get_stock_fluctuation(symbol)
        # ⚠️ NE PAS METTRE DE PRINT NON JSON
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

