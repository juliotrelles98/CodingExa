import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score


def cluster_data(
    df: pd.DataFrame,
    method: str = "kmeans",
    n_clusters: int | None = 3,
    **kwargs,
):
    """Perform clustering on a numeric pandas DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The raw data containing *only* numeric columns (non-numeric columns will
        be ignored automatically).
    method : {"kmeans", "dbscan"}
        Algorithm to use.
    n_clusters : int | None
        Number of clusters (only for k-means).
    **kwargs :
        Extra keyword arguments passed directly to the underlying estimator.

    Returns
    -------
    result_df : pd.DataFrame
        DataFrame enriched with principal component coordinates and cluster
        label.
    sil_score : float | None
        Silhouette score when definable, else *None*.
    inertia : float | None
        k-means inertia when definable, else *None*.
    """

    # 1. Select numeric data
    X = df.select_dtypes(include=[np.number]).dropna()
    if X.empty:
        raise ValueError("Input data must contain at least one numeric column with non-NA values.")

    # 2. Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. Fit chosen model
    if method.lower() == "kmeans":
        if n_clusters is None:
            raise ValueError("n_clusters must be provided for k-means clustering.")
        model = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
        labels = model.fit_predict(X_scaled)
        inertia = float(model.inertia_)
        sil = float(silhouette_score(X_scaled, labels)) if n_clusters > 1 else None
    elif method.lower() == "dbscan":
        model = DBSCAN(**kwargs)
        labels = model.fit_predict(X_scaled)
        inertia = None
        unique_labels = set(labels)
        sil = float(silhouette_score(X_scaled, labels)) if len(unique_labels) > 1 else None
    else:
        raise ValueError(f"Unsupported clustering method: {method}")

    # 4. Dimensionality reduction for visualisation
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)

    # 5. Compose result DataFrame
    result_df = X.copy()
    result_df["pca1"] = components[:, 0]
    result_df["pca2"] = components[:, 1]
    result_df["cluster"] = labels

    return result_df, sil, inertia 