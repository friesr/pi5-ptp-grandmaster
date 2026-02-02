import numpy as np
from sklearn.cluster import KMeans

def cluster_anomalies(feature_vectors, k=5):
    """
    feature_vectors: list of 6-element vectors
    k: number of clusters
    """

    if len(feature_vectors) < k:
        return [0] * len(feature_vectors)

    X = np.array(feature_vectors)
    model = KMeans(n_clusters=k, n_init=10)
    labels = model.fit_predict(X)

    return labels.tolist(), model.cluster_centers_.tolist()
