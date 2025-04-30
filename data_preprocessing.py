import yfinance as yf
import pandas as pd
import os
import logging
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("download_log.txt")
    ]
)

def download_stock_data(tickers, start_date, end_date, save_path):
    logging.info(f"Downloading stock data for {tickers} from {start_date} to {end_date}...")

    # If multiple tickers, split into a list
    if isinstance(tickers, str):
        tickers = [ticker.strip() for ticker in tickers.split(',')]

    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', auto_adjust=True)

    if data.empty:
        logging.error(f"❌ No data downloaded. Check internet or ticker symbols.")
        return

    logging.info(f"Downloaded data head:\n{data.head()}")
    logging.info(f"Data columns: {data.columns.tolist()}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # If multiple stocks, we need to process each stock separately
    all_stocks_data = []

    for ticker in tickers:
        if isinstance(data.columns, pd.MultiIndex):
            if ticker not in data.columns.get_level_values(0):
                logging.warning(f"⚠️ Ticker {ticker} not found in downloaded data. Skipping.")
                continue

            stock_data = data[ticker].copy()

            if 'Close' not in stock_data.columns:
                logging.warning(f"⚠️ 'Close' not found for {ticker}. Skipping.")
                continue

            stock_data['Ticker'] = ticker
            stock_data['Daily_Return'] = stock_data['Close'].pct_change()
            all_stocks_data.append(stock_data)

        else:
            # Single stock
            stock_data = data.copy()
            stock_data['Ticker'] = ticker
            stock_data['Daily_Return'] = stock_data['Close'].pct_change()
            all_stocks_data.append(stock_data)

    if not all_stocks_data:
        logging.error("❌ No valid stock data found to save.")
        return

    final_data = pd.concat(all_stocks_data)
    final_data.to_csv(save_path)
    logging.info(f"✅ Combined data saved to {save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download stock data for multiple tickers and process it.")
    parser.add_argument('--tickers', type=str, required=True, help="Comma-separated stock ticker symbols (e.g., AMZN,TSLA,MSFT)")
    parser.add_argument('--start', type=str, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument('--end', type=str, required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument('--save', type=str, required=True, help="Path to save the processed CSV")

    args = parser.parse_args()

    download_stock_data(args.tickers, args.start, args.end, args.save)
