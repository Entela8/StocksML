import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta

def get_stock_price_timeline(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    if stock_data.empty:
        return f"No data found for {symbol} from {start_date} to {end_date}"
    
    return stock_data

if __name__ == "__main__":
    symbol = input("Enter stock symbol: ")
    end_date = date.today()
    # Subtract 6 months from the start date
    start_date = end_date - relativedelta(months=6)


    print(end_date)   
    print(get_stock_price_timeline(symbol, start_date, end_date))