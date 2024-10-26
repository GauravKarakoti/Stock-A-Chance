import torch
import torch.nn as nn
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from stock_data import get_stock_data

input_size = 1
hidden_layer_size = 50
output_size = 1

def lstm_model():
    lstm = nn.LSTM(input_size, hidden_layer_size, batch_first=True)
    linear = nn.Linear(hidden_layer_size, output_size)
    return lstm, linear

def initialize_hidden(batch_size):
    return (torch.zeros(1, batch_size, hidden_layer_size),
            torch.zeros(1, batch_size, hidden_layer_size))

def forward_pass(lstm, linear, input_seq, hidden_cell):
    lstm_out, hidden_cell = lstm(input_seq.view(len(input_seq), 1, -1), hidden_cell)
    predictions = linear(lstm_out.view(len(input_seq), -1))
    return predictions[-1], hidden_cell

def preprocess_stock_data(ticker, seq_length=60):
    stock_data = get_stock_data(ticker)
    stock_prices = stock_data['Close'].values
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaled_data = scaler.fit_transform(stock_prices.reshape(-1, 1))

    sequences = []
    for i in range(len(scaled_data) - seq_length):
        sequences.append(scaled_data[i:i+seq_length])

    sequences = np.array(sequences)
    train_size = int(len(sequences) * 0.8)
    train_data = sequences[:train_size]
    test_data = sequences[train_size:]

    return train_data, test_data, scaler

def train_model(lstm, linear, train_data, num_epochs=10, lr=0.001):
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(list(lstm.parameters()) + list(linear.parameters()), lr=lr)

    for epoch in range(num_epochs):
        for seq in train_data:
            optimizer.zero_grad()
            batch_size = len(seq[:-1])
            hidden_cell = initialize_hidden(batch_size)
            y_pred, hidden_cell = forward_pass(lstm, linear, torch.tensor(seq[:-1], dtype=torch.float32), hidden_cell)
            single_loss = loss_function(y_pred, torch.tensor(seq[-1], dtype=torch.float32))
            single_loss.backward()
            optimizer.step()
        print("Please Wait a Moment.....")
        # print(f'Epoch {epoch+1} loss: {single_loss.item()}')

def predict_stock(lstm, linear, test_data, scaler):
    predictions = []
    actuals = []
    lstm.eval()
    for seq in test_data:
        with torch.no_grad():
            batch_size = len(seq[:-1])
            hidden_cell = initialize_hidden(batch_size)
            predicted_price, hidden_cell = forward_pass(lstm, linear, torch.tensor(seq[:-1], dtype=torch.float32), hidden_cell)
            predicted_price = scaler.inverse_transform(predicted_price.detach().numpy().reshape(-1, 1))
            actual_price = scaler.inverse_transform(seq[-1].reshape(-1, 1))
            
            predictions.append(predicted_price)
            actuals.append(actual_price)

    return np.array(predictions), np.array(actuals)

'''def evaluate_model(predictions, actuals):
    predictions = predictions.reshape(-1, 1)
    actuals = actuals.reshape(-1, 1)
    
    mse = mean_squared_error(actuals, predictions,squared=False)
    
    print(f'MSE: {mse}')'''


def predict_stock_price(ticker):
    train_data, test_data, scaler = preprocess_stock_data(ticker)
    lstm, linear = lstm_model()
    train_model(lstm, linear, train_data)
    predictions, actuals = predict_stock(lstm, linear, test_data, scaler)
    #evaluate_model(predictions, actuals)
    return predictions