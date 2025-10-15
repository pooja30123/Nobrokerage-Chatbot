import pandas as pd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')

def load_master_data():
    file_path = os.path.join(DATA_PATH, 'master_properties.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Master data file not found at {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} properties from master data")
    return df

def get_unique_localities(df):
    localities = df['landmark'].dropna().unique().tolist()
    return localities

def get_price_range(df):
    min_price = df['price_crore'].min()
    max_price = df['price_crore'].max()
    return min_price, max_price
