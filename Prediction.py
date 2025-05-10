import yfinance as yf
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import warnings
warnings.filterwarnings("ignore")

def get_stock_data(symbol):
    data = yf.download(symbol, period="1d", interval="1m", progress=False)
    return data['Close']

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_next_price(symbol):
    stock_data = get_stock_data(symbol)

    if stock_data.isnull().values.any() or len(stock_data) < 61:
        return None, None, None

    current_price = stock_data.iloc[-1].item()  # Ensure it's a scalar value
    last_time_utc = stock_data.index[-1]
    
    # Convert to IST
    last_time_utc = pd.to_datetime(last_time_utc).tz_localize('UTC') if last_time_utc.tzinfo is None else last_time_utc
    predicted_time_ist = (last_time_utc + pd.Timedelta(minutes=1)).tz_convert('Asia/Kolkata')

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data.values.reshape(-1, 1))
    time_step = 60

    if len(scaled_data) <= time_step:
        return None, None, None

    X, Y = [], []
    for i in range(len(scaled_data) - time_step):
        X.append(scaled_data[i:i + time_step, 0])
        Y.append(scaled_data[i + time_step, 0])

    if len(X) == 0:
        return None, None, None

    X = np.array(X).reshape(-1, time_step, 1)
    Y = np.array(Y)

    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, Y, epochs=3, batch_size=32, verbose=0)

    last_input = scaled_data[-time_step:].reshape(1, -1, 1)
    predicted_price = model.predict(last_input)
    predicted_price = scaler.inverse_transform(predicted_price)

    return current_price, predicted_price[0][0], predicted_time_ist

def run_ticker(symbol):
    print(f"\n📈 Real-Time Stock Ticker for {symbol}\nPress Ctrl+C to stop.\n")
    try:
        while True:
            current_price, predicted_price, time_ist = predict_next_price(symbol)
            if predicted_price is not None:
                print(f"[{time_ist.strftime('%Y-%m-%d %H:%M:%S %p IST')}] "
                      f"Current: ₹{current_price:.2f} | Predicted: ₹{predicted_price:.2f}")
            else:
                print("⚠️  Not enough data or market might be closed.")
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n⏹️  Ticker stopped by user.")

if __name__ == "__main__":
    run_ticker("TCS.NS")  # Change this to any NSE stock symbol.
