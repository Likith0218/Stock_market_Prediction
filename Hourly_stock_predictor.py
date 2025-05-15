import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Function to fetch stock data
def get_stock_data(symbol):
    return yf.download(symbol, period="7d", interval="1h")['Close']

# Building the LSTM Model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Training LSTM and Predicting Next Prices
def predict_hourly(symbol):
    stock_data = get_stock_data(symbol)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data.values.reshape(-1, 1))

    # Creating dataset
    X, Y = [], []
    time_step = 24  # Using 24 hours of data for prediction
    for i in range(len(scaled_data) - time_step):
        X.append(scaled_data[i:i + time_step, 0])
        Y.append(scaled_data[i + time_step, 0])

    X = np.array(X)
    Y = np.array(Y)

    X = X.reshape(X.shape[0], X.shape[1], 1)

    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, Y, epochs=3, batch_size=32, verbose=0)

    last_input = scaled_data[-time_step:]
    last_input = last_input.reshape(1, -1, 1)

    predicted_price = model.predict(last_input)
    predicted_price = scaler.inverse_transform(predicted_price)

    return predicted_price[0][0]

# Example of usage:
if __name__ == "__main__":
    symbol = "TCS.NS"  # You can dynamically change this based on user input
    predicted_price = predict_hourly(symbol)
    print(f"Predicted next hour price for {symbol}: ₹{predicted_price}")
