import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

def train_rf_model(input_csv, model_path):
    df = pd.read_csv(input_csv)
    
    print(f"✅ Loaded data shape: {df.shape}")
    print(f"✅ Columns: {df.columns.tolist()}")

    # Feature Engineering
    features = ['Close', 'Open', 'High', 'Low', 'Volume']
    target = 'Daily_Return'

    if not all(col in df.columns for col in features + [target]):
        print("❌ Missing required columns in data!")
        return

    # Drop any rows with missing values
    df = df.dropna()

    X = df[features]
    y = df[target]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    print(f"✅ Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_rf_model('datasets/multi_stock_data.csv', 'datasets/stock_model.pkl')
