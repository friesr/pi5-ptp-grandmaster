import numpy as np
from sklearn.linear_model import LinearRegression

def train_stability_model(X, y):
    if len(X) < 3:
        return None

    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_stability(model, today_features):
    if model is None:
        return None

    pred = model.predict([today_features])[0]
    return float(pred)
