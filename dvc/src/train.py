from sklearn.linear_model import LinearRegression
import joblib
import yaml
import pandas as pd

with open("params.yaml") as f:
    params = yaml.safe_load(f)

X_train = pd.read_csv('data/processed/X_train.csv')
y_train = pd.read_csv('data/processed/y_train.csv')

model = LinearRegression(n_jobs=params["train"]["model"]["n_jobs"])
model.fit(X_train, y_train)
joblib.dump(model, 'models/model.pkl')