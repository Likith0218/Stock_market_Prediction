import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import warnings
warnings.filterwarnings("ignore")

# Fetch stock data (1-minute interval)
def get_stock_data(symbol):
    return yf.download(symbol, period="1d", interval="1m")['Close']

# Build LSTM Model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train and Predict
def predict_stock_price(symbol):
    stock_data = get_stock_data(symbol)

    if stock_data.isnull().values.any() or len(stock_data) < 61:
        print("Not enough data or missing data points.")
        return

    # Get last timestamp (already in UTC), convert to IST
    last_time_utc = stock_data.index[-1]
    predicted_time_ist = last_time_utc + pd.Timedelta(minutes=1)
    predicted_time_ist = predicted_time_ist.tz_convert('Asia/Kolkata')

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data.values.reshape(-1, 1))

    # Create sequences
    time_step = 60
    X, Y = [], []
    for i in range(len(scaled_data) - time_step):
        X.append(scaled_data[i:i + time_step, 0])
        Y.append(scaled_data[i + time_step, 0])

    X = np.array(X).reshape(-1, time_step, 1)
    Y = np.array(Y)

    # Train LSTM model
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, Y, epochs=3, batch_size=32, verbose=0)

    # Predict next price
    last_input = scaled_data[-time_step:].reshape(1, -1, 1)
    predicted_price = model.predict(last_input)
    predicted_price = scaler.inverse_transform(predicted_price)

    return predicted_price[0][0], predicted_time_ist

# Run the prediction
if __name__ == "__main__":
    symbol = "ITC.NS"  # NSE stock ticker
    result = predict_stock_price(symbol)
    if result:
        price, timestamp = result
        print(f"Predicted price for {symbol} at {timestamp.strftime('%Y-%m-%d %H:%M %p IST')} is ₹{price:.2f}")
