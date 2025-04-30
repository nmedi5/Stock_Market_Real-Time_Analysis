# Fetch real historical data
@st.cache_data
def fetch_stock_data(ticker):
    stock_data = yf.download(ticker, period='1mo', interval='1d')
    return stock_data

stock_data = fetch_stock_data(selected_ticker)

st.subheader("Enter Today's Stock Information")

# Safe fallback defaults
default_values = {
    'Close': 100.0,
    'Open': 100.0,
    'High': 100.0,
    'Low': 100.0,
    'Volume': 1000000
}

if not stock_data.empty and all(col in stock_data.columns for col in ['Close', 'Open', 'High', 'Low', 'Volume']):
    latest_close = stock_data['Close'].iloc[-1]
    latest_open = stock_data['Open'].iloc[-1]
    latest_high = stock_data['High'].iloc[-1]
    latest_low = stock_data['Low'].iloc[-1]
    latest_volume = stock_data['Volume'].iloc[-1]
else:
    latest_close = default_values['Close']
    latest_open = default_values['Open']
    latest_high = default_values['High']
    latest_low = default_values['Low']
    latest_volume = default_values['Volume']

# Pre-fill with today's stock prices
close = st.number_input('Close Price', min_value=0.0, value=float(latest_close), step=1.0)
open_price = st.number_input('Open Price', min_value=0.0, value=float(latest_open), step=1.0)
high = st.number_input('High Price', min_value=0.0, value=float(latest_high), step=1.0)
low = st.number_input('Low Price', min_value=0.0, value=float(latest_low), step=1.0)
volume = st.number_input('Volume', min_value=0, value=int(latest_volume), step=1000)
