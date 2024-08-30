import os
import sys
import pandas as pd
import pickle

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
parent_directory2 = os.path.dirname(parent_directory)
sys.path.insert(0, parent_directory2)

scripts_dir = os.path.join(parent_directory2, 'scripts')
from main import DataPreprocessing, FinancialAnalyzer

file_paths = {
    "AAPL_historical_data": "https://drive.google.com/uc?export=download&id=12QaqqPSHGQJAABo1hkYJqmE1fo0RTrfm",
    "AMZN_historical_data": "https://drive.google.com/uc?export=download&id=1gRA-R18ypsy2q2K0vc3BEW3RboX-LQbg",
    "GOOG_historical_data": "https://drive.google.com/uc?export=download&id=1rH0HiCmJCgJgqEP24FARUln8W1h6eErD",
    "META_historical_data": "https://drive.google.com/uc?export=download&id=16dCeNu5B5nG9uf6dPNKrverxHfeCUPOo",
    "MSFT_historical_data": "https://drive.google.com/uc?export=download&id=15O8RXW96qQ4mOVoYeMygGhPhjtzrCb7n",
    "NVDA_historical_data": "https://drive.google.com/uc?export=download&id=1OUXm-6FOavKaMe5MLTFupcO_PnyEeRu4",
    "TSLA_historical_data": "https://drive.google.com/uc?export=download&id=1z9BzWLQ5SQ_plmkF0YCA8zSBhIfhCLwQ"
}

preprocessor = DataPreprocessing(file_paths)
data_frames = preprocessor.process_file()
data_frames = {
    "AAPL": data_frames.get("AAPL_historical_data"),
    "AMZN": data_frames.get("AMZN_historical_data"),
    "GOOG": data_frames.get("GOOG_historical_data"),
    "META": data_frames.get("META_historical_data"),
    "MSFT": data_frames.get("MSFT_historical_data"),
    "NVDA": data_frames.get("NVDA_historical_data"),
    "TSLA": data_frames.get("TSLA_historical_data")
}

filtered_data_frames = {}
for label, df in data_frames.items():
    analyzer = FinancialAnalyzer(df, '2013-01-01', '2023-12-29')
    filtered_df = analyzer.filter_by_date()
    filtered_data_frames[label] = filtered_df

with open('filtered_data_frames.pkl', 'wb') as f:
    pickle.dump(filtered_data_frames, f)

