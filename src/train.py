import pandas as pd
import joblib
import mlflow
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from src.features import create_features

# 1. Ensure the models directory exists so we don't get a save error later
os.makedirs("models", exist_ok=True)

print("Loading and processing data...")
# 2. Load raw data and apply our feature engineering pipeline
df = pd.read_csv("data/raw/sales.csv")
df = create_features(df)

# 3. Define the exact features the model will use (X) and what it will predict (y)
features = ['Month', 'Quarter', 'Revenue_lag_1', 'Rolling_avg_3']
X = df[features]
y = df['Revenue']

# 4. Split into training and testing sets (shuffle=False is CRITICAL for time series!)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

print("Training model...")
# 5. Start MLflow tracking
with mlflow.start_run():
    # Initialize and train the XGBoost model
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions on our test set
    predictions = model.predict(X_test)
    
    # Calculate how far off we were on average (Mean Absolute Error)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model trained successfully! Mean Absolute Error (MAE): ${mae:,.2f}")
    
    # 6. Log metrics to MLflow and save the actual model file
    mlflow.log_metric("MAE", mae)
    joblib.dump(model, "models/model.pkl")
    print("Model saved to models/model.pkl")