import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def get_stock_data(symbol):
    data = yf.download(symbol, period="90d", interval="1d", progress=False)
    return data['Close']

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_end_of_day_price(symbol):
    stock_data = get_stock_data(symbol)

    if stock_data.isnull().values.any() or len(stock_data) < 61:
        return None, None, None, None

    current_price = stock_data.iloc[-1].item()
    last_date = stock_data.index[-1].strftime('%Y-%m-%d')

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data.values.reshape(-1, 1))

    time_step = 60
    X, Y = [], []

    for i in range(len(scaled_data) - time_step):
        X.append(scaled_data[i:i + time_step, 0])
        Y.append(scaled_data[i + time_step, 0])

    if not X:
        return None, None, None, None

    X = np.array(X).reshape(-1, time_step, 1)
    Y = np.array(Y)

    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, Y, epochs=5, batch_size=16, verbose=0)

    last_input = scaled_data[-time_step:].reshape(1, -1, 1)
    predicted_price_scaled = model.predict(last_input)
    predicted_price = scaler.inverse_transform(predicted_price_scaled)

    return current_price, predicted_price[0][0], last_date, stock_data
