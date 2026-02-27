import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Convert Date string to actual datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Calculate our Target Variable (what we want to predict)
    df['Revenue'] = df['Quantity_Sold'] * df['Price_per_kg']
    
    # 3. Extract time-based features
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    
    # 4. Create Time-Series specific features
    # 'Revenue_lag_1' is the revenue from the previous month
    df['Revenue_lag_1'] = df['Revenue'].shift(1)
    
    # 'Rolling_avg_3' is the average revenue of the past 3 months
    df['Rolling_avg_3'] = df['Revenue'].rolling(3).mean()
    
    # 5. Drop empty rows (NaNs) caused by the shift and rolling calculations
    df = df.dropna().reset_index(drop=True)
    
    return df