import pandas as pd
from sklearn.cluster import KMeans
from ..io.clean import tidy

def kmeans_clusters(n_clusters: int = 8) -> pd.DataFrame:
    df = pd.DataFrame([sorted(r.balls) for r in tidy()],
                      columns=[f"b{i+1}" for i in range(5)])
    km = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
    df["label"] = km.fit_predict(df)
    return df
