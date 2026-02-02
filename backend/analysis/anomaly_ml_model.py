import numpy as np
from sklearn.ensemble import RandomForestClassifier

def train_anomaly_model(rows):
    """
    rows: list of anomaly rows with 'cluster' labels
    """

    X = []
    y = []

    for r in rows:
        X.append([
            r["snr"],
            r["multipath"],
            r["geometry_score"],
            r["prn_health"],
            r["interference_level"],
            r["state"]
        ])
        y.append(r["cluster"])

    if len(X) < 10:
        return None

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    model.fit(X, y)
    return model


def predict_anomaly(model, row):
    if model is None:
        return None

    X = np.array([[
        row["snr"],
        row["multipath"],
        row["geometry_score"],
        row["prn_health"],
        row["interference_level"],
        row["state"]
    ]])

    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0].tolist()

    return {
        "predicted_cluster": int(pred),
        "probabilities": prob
    }
