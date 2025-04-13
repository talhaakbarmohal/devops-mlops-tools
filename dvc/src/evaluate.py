import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import json

X_test = pd.read_csv('data/processed/X_test.csv')
y_test = pd.read_csv('data/processed/y_test.csv')
model = joblib.load('models/model.pkl')

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Optionally save to metrics.json
with open("metrics.json", "w") as f:
    json.dump({"mse": mse, "mae": mae, "r2": r2}, f, indent=4)