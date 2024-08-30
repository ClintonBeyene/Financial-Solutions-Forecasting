import pandas as pd
import gdown
import os
import talib as ta
import numpy as np
import plotly.express as px
from pypfopt.efficient_frontier import EfficientFrontier
<<<<<<< HEAD
from pypfopt import risk_models, expected_returns
import yfinance as yf
=======
from pypfopt import risk_models
from pypfopt import expected_returns
>>>>>>> e7092f880e0ccd3f974d1758fc933f2dbf6d8a80

class DataPreprocessing:
    def __init__(self, file_paths=None):
        self.file_paths = file_paths if file_paths else {
            "Row-Analysis-Ratings": "https://drive.google.com/uc?export=download&id=1MC0ePKh2oc3VqGtOMNTboyICpyuiSr2l",
            "AAPL_historical_data": "https://drive.google.com/uc?export=download&id=12QaqqPSHGQJAABo1hkYJqmE1fo0RTrfm",
            "AMZN_historical_data": "https://drive.google.com/uc?export=download&id=1gRA-R18ypsy2q2K0vc3BEW3RboX-LQbg",
            "GOOG_historical_data": "https://drive.google.com/uc?export=download&id=1rH0HiCmJCgJgqEP24FARUln8W1h6eErD",
            "META_historical_data": "https://drive.google.com/uc?export=download&id=16dCeNu5B5nG9uf6dPNKrverxHfeCUPOo",
            "MSFT_historical_data": "https://drive.google.com/uc?export=download&id=15O8RXW96qQ4mOVoYeMygGhPhjtzrCb7n",
            "NVDA_historical_data": "https://drive.google.com/uc?export=download&id=1OUXm-6FOavKaMe5MLTFupcO_PnyEeRu4",
            "TSLA_historical_data": "https://drive.google.com/uc?export=download&id=1z9BzWLQ5SQ_plmkF0YCA8zSBhIfhCLwQ"
        }
        self.data_frames = {}

    def process_file(self, file_name=None):
        if file_name:
            file_path = self.file_paths.get(file_name=6)
            if file_path:
                try:
                    output = f"{file_name}.csv"
                    if not os.path.exists(output):
                        gdown.download(file_path, output, quiet=False)
                    data = pd.read_csv(output)
                    self.data_frames[file_name] = data
                    print(f'Data for {file_name} loaded successfully.')
                except Exception as e:
                    print(f"An error occurred while processing {file_name}: {e}")
            else:
                print(f"No file path found for {file_name}")
        else:
            for name, file_path in self.file_paths.items():
                try:
                    output = f"{name}.csv"
                    if not os.path.exists(output):
                        gdown.download(file_path, output, quiet=False)
                    data = pd.read_csv(output)
                    self.data_frames[name] = data
                    print(f'Data for {name} loaded successfully.')
                except Exception as e:
                    print(f"An error occurred while processing {name}: {e}")
        return self.data_frames

    def check_missing_values(self):
        missing_values = {}
        for name, df in self.data_frames.items():
            missing_values[name] = df.isnull().sum()
        return missing_values

    def check_data_type(self, name):
        data_type_counts = {}
        for name, df in self.data_frames.items():
            data_type_counts[name] = df.dtypes.value_counts()
        return data_type_counts

    def uniform_date_format(self, filename, date_column, new_filename):
        try:
            df = pd.read_csv(filename)
            df[date_column] = pd.to_datetime(df[date_column], format="%Y-%m-%d %H:%M:%S%z")
            df[date_column] = df[date_column].dt.strftime('%m/%d/%Y %I:%M:%S %p %z')
            df.to_csv(new_filename, index=False)
            print(f"Date format in column '{date_column}' has been standardized and saved to '{new_filename}'.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

class FinancialAnalyzer:
    def __init__(self, data_frame, start_date, end_date):
        self.data_frame = data_frame
        self.start_date = start_date
        self.end_date = end_date
    
    def filter_by_date(self):
        # Ensure the 'Date' column is in datetime format
        self.data_frame['Date'] = pd.to_datetime(self.data_frame['Date'])
        # Filter the DataFrame by the specified date range
        filtered_df = self.data_frame[(self.data_frame['Date'] >= self.start_date) & (self.data_frame['Date'] <= self.end_date)]
        return filtered_df
    
    def check_missing_values(self, filtered_df):
        return filtered_df.isnull().sum()

    def check_data_type(self, filtered_df):
        return filtered_df.dtypes

    def calculate_moving_average(self, data, window_size):
        return ta.SMA(data, timeperiod=window_size) 

<<<<<<< HEAD
    def calculate_technical_indicators(self, data_dict):
        for label, data in data_dict.items():
            # Check if 'Close' column exists
            if 'Close' not in data.columns:
                raise KeyError(f"'Close' column is missing from the DataFrame for {label}")
        
            # Calculate various technical indicators using .loc to avoid SettingWithCopyWarning
            data.loc[:, 'SMA_50'] = self.calculate_moving_average(data.loc[:, 'Close'], 50)
            data.loc[:, 'SMA_200'] = self.calculate_moving_average(data.loc[:,'Close'], 200)
            data.loc[:, 'RSI'] = ta.RSI(data.loc[:, 'Close'], timeperiod=14)
            data.loc[:, 'EMA_12'] = ta.EMA(data.loc[:, 'Close'], timeperiod=12)
            data.loc[:, 'EMA_26'] = ta.EMA(data.loc[:, 'Close'], timeperiod = 26)
            macd, macd_signal, _ = ta.MACD(data.loc[:, 'Close'], fastperiod=12, slowperiod=26, signalperiod=9)
            data.loc[:, 'MACD'] = macd
            data.loc[:, 'MACD_Signal'] = macd_signal
        
        return data_dict
    
    def plot_stock_data1(self, data_dict):
        fig = px.line(title='Stock Prices with Moving Averages')
        
        for label, data in data_dict.items():
            data.set_index('Date', inplace=True)
            fig.add_scatter(x=data.index, y=data['Close'], mode='lines', name=f'{label} Close')
            fig.add_scatter(x=data.index, y=data['SMA_50'], mode='lines', name=f'{label} 50-Day SMA')
            fig.add_scatter(x=data.index, y=data['SMA_200'], mode='lines', name=f'{label} 200-Day SMA')
        
        fig.show()

    def plot_stock_data(self, data_dict):        
        for label, data in data_dict.items():
            fig = px.line(title=f'Stock Prices with moving average for {label}')
            data.set_index('Date', inplace=True)
            fig.add_scatter(x=data.index, y=data['Close'], mode='lines', name=f'{label} Close')
            fig.add_scatter(x=data.index, y=data['SMA_50'], mode='lines', name=f'{label} 50-Day SMA')
            fig.add_scatter(x=data.index, y=data['SMA_200'], mode='lines', name=f'{label} 200-Day SMA')
        
            fig.show()

    def plot_rsi(self, data_dict):
        for label, data in data_dict.items():
            fig = px.line(data, x=data.index, y='RSI', title=f'{label} RSI')
            fig.show()

    def plot_ema(self, data_dict):
        for label, data in data_dict.items():
            fig = px.line(data, x=data.index, y=['Close', 'EMA_12', 'EMA_26'], title=f'{label}: Stock Price with Exponential Moving Average')
            fig.show()

    def plot_macd(self, data_dict):
        for label, data in data_dict.items():
            fig = px.line(data, x=data.index, y=['MACD', 'MACD_Signal'], title=f'{label}: Moving Average Convergence Divergence (MACD)')
            fig.show()

=======
    def calculate_technical_indicators(self, data):
        # Calculate various technical indicators
        data['SMA'] = self.calculate_moving_average(data['Close'], 20)
        data['RSI'] = ta.RSI(data['Close'], timeperiod=14)
        data['EMA'] = ta.EMA(data['Close'], timeperiod=20)
        macd, macd_signal, _ = ta.MACD(data['Close'])
        data['MACD'] = macd
        data['MACD_Signal'] = macd_signal
        # Add more indicators as needed
        return data

    def plot_stock_data(self, data):
        data.set_index('Date', inplace=True)
        fig = px.line(data, x=data.index, y=['Close', 'SMA'], title='Stock Price with Moving Average')
        fig.show()

    def plot_rsi(self, data):
        fig = px.line(data, x=data.index, y='RSI', title='Relative Strength Index (RSI)')
        fig.show()

    def plot_ema(self, data):
        fig = px.line(data, x=data.index, y=['Close', 'EMA'], title='Stock Price with Exponential Moving Average')
        fig.show()

    def plot_macd(self, data):
        fig = px.line(data, x=data.index, y=['MACD', 'MACD_Signal'], title='Moving Average Convergence Divergence (MACD)')
        fig.show()
    
>>>>>>> e7092f880e0ccd3f974d1758fc933f2dbf6d8a80
    def calculate_portfolio_weights(self, tickers, start_date, end_date):
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        mu = expected_returns.mean_historical_return(data)
        cov = risk_models.sample_cov(data)
        ef = EfficientFrontier(mu, cov)
        weights = ef.max_sharpe()
        weights = dict(zip(tickers, weights.values()))
        return weights
<<<<<<< HEAD
    
=======

>>>>>>> e7092f880e0ccd3f974d1758fc933f2dbf6d8a80
    def calculate_portfolio_performance(self, tickers, start_date, end_date):
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        mu = expected_returns.mean_historical_return(data)
        cov = risk_models.sample_cov(data)
        ef = EfficientFrontier(mu, cov)
        weights = ef.max_sharpe()
        portfolio_return, portfolio_volatility, sharpe_ratio = ef.portfolio_performance()
        return portfolio_return, portfolio_volatility, sharpe_ratio

"""
# Example usage
file_path = { 
    "Row-Analysis-Ratings": "https://drive.google.com/uc?export=download&id=1MC0ePKh2oc3VqGtOMNTboyICpyuiSr2l"
}
preprocessor = DataPreprocessing(file_path)
data_frames = preprocessor.process_file()  # This will download and process the specific file

# If i want to download and process all files, i can initialize without file_path
preprocessor_all = DataPreprocessing()
data_frames_all = preprocessor_all.process_file()  # This will download and process all files
"""