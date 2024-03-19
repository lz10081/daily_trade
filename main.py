import yfinance as yf
import pandas_ta as ta
from datetime import datetime

# Function to get historical stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data


# Strategy 1: Moving Average Crossover
def moving_average_crossover(data):
    # Calculate short-term moving average (e.g., 50 days)
    data['Short_MA'] = data['Close'].rolling(window=50).mean()
    # Calculate long-term moving average (e.g., 200 days)
    data['Long_MA'] = data['Close'].rolling(window=200).mean()

    # Check for buy signal (short-term MA crosses above long-term MA)
    if data['Short_MA'].iloc[-1] > data['Long_MA'].iloc[-1] and \
            data['Short_MA'].iloc[-2] <= data['Long_MA'].iloc[-2]:
        return True
    else:
        return False


# Strategy 2: Relative Strength Index (RSI)
def relative_strength_index(data, period=14, oversold_threshold=30):
    # Calculate RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))

    # Check for oversold condition (RSI < oversold_threshold)
    if RSI.iloc[-1] < oversold_threshold:
        return True
    else:
        return False


# Strategy 3: Volume Surge
def volume_surge(data, volume_threshold=2):
    # Calculate average volume
    average_volume = data['Volume'].mean()

    # Check for volume surge (current volume > threshold * average volume)
    if data['Volume'].iloc[-1] > volume_threshold * average_volume:
        return True
    else:
        return False


# Strategy 4: Breakout
def breakout(data):
    # Check for breakout based on specific criteria (e.g., breaking out of a resistance level)
    # This can involve technical analysis of chart patterns or specific price levels
    # For simplicity, we'll just check if the current close price is higher than the previous close
    if data['Close'].iloc[-1] > data['Close'].iloc[-2]:
        return True
    else:
        return False


# Strategy 5: MACD (Moving Average Convergence Divergence)
def macd_signal(data):
    # Calculate MACD
    data.ta.macd(fast=12, slow=26, append=True)

    # Check for bullish crossover (MACD crosses above signal line)
    if data['MACD_12_26_9'].iloc[-1] > data['MACDs_12_26_9'].iloc[-1]:
        return True
    else:
        return False


# Strategy 6: Bollinger Bands
def bollinger_bands(data):
    # Calculate Bollinger Bands
    data.ta.bbands(length=20, append=True)

    # Check for breakout above upper band
    if data['Close'].iloc[-1] > data['BBU_20_2.0'].iloc[-1]:
        return True
    else:
        return False

# Main function
def main():
    tickers = [
    'AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB', 'TSLA', 'BRK.B', 'JPM', 'JNJ', 'V', 'PG', 'NVDA', 'MA', 'HD', 'DIS', 'UNH', 'PYPL', 'BAC', 'ADBE', 'CMCSA',
    'INTC', 'NFLX', 'XOM', 'VZ', 'CRM', 'ABT', 'T', 'PEP', 'KO', 'MRK', 'CVX', 'CSCO', 'NKE', 'ABBV', 'TMUS', 'PFE', 'MDT', 'ACN', 'WMT', 'TMO',
    'NEE', 'AVGO', 'IBM', 'TXN', 'QCOM', 'UNP', 'LIN', 'DHR', 'PM', 'LOW', 'ORCL', 'NOW', 'GE', 'LMT', 'UPS', 'HON', 'INTU', 'AMGN', 'SBUX',
    'AMD', 'BA', 'FIS', 'CAT', 'MMM', 'CVS', 'MS', 'AXP', 'BDX', 'D', 'FDX', 'ANTM', 'GILD', 'CCI', 'RTX', 'BKNG', 'ISRG', 'DE', 'BLK', 'CHTR',
    'ZTS', 'SPGI', 'SCHW', 'MO', 'PLD', 'TFC', 'APD', 'COST', 'TJX', 'CB', 'EW', 'BDX', 'CL', 'BDX', 'GD', 'WM', 'MMC', 'ETN', 'TROW', 'CMI',
    'ROP', 'VFC', 'ECL', 'AON', 'SYK', 'REGN', 'DUK', 'GM', 'KMB', 'IQV', 'LHX', 'SO', 'IDXX', 'NOC', 'ROST', 'SHW', 'CTSH', 'AEP', 'CTAS',
    'LRCX', 'COF', 'MET']  # Example stock ticker (Apple Inc.)
    start_date = '2023-01-01'

    end_date = datetime.today().strftime('%Y-%m-%d')

    # Get historical stock data
    for ticker in tickers:
        try:


                # Get historical stock data
                stock_data = get_stock_data(ticker, start_date, end_date)

                # Counter for the number of buy signals
                buy_signals = 0

                # Strategy 1: Moving Average Crossover
                if moving_average_crossover(stock_data):
                    buy_signals += 1

                # Strategy 2: Relative Strength Index (RSI)
                if relative_strength_index(stock_data):
                    buy_signals += 1

                # Strategy 3: Volume Surge
                if volume_surge(stock_data):
                    buy_signals += 1

                # Strategy 4: Breakout
                if breakout(stock_data):
                    buy_signals += 1
                if bollinger_bands(stock_data):
                    buy_signals += 1
                if macd_signal(stock_data):
                    buy_signals += 1


                # If more than one strategy indicates a buy, consider it a potential buy signal
                if buy_signals >= 2:
                    print(f'{ticker}: Potential BUY ({buy_signals} out of 6 strategies)')
        except:
            pass


if __name__ == "__main__":
    main()