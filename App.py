import streamlit as st
import pandas as pd
import plotly.express as px

from clusterer import cluster_data

st.set_page_config(page_title="Clustering Dashboard", layout="wide")

st.title("🔍 Data Clustering Dashboard")

with st.sidebar:
    st.header("⚙️ Configuración")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])  # Allow raw data upload

    if uploaded_file is not None:
        algorithm = st.selectbox("Algoritmo", ["kmeans", "dbscan"], index=0)
        if algorithm == "kmeans":
            n_clusters = st.slider("Número de clusters (k)", 2, 20, 3)
            run_button = st.button("Ejecutar clustering")
            params = {"n_clusters": n_clusters}
        else:  # dbscan parameters
            eps = st.slider("eps (radio de vecindad)", 0.1, 10.0, 0.5)
            min_samples = st.slider("min_samples", 1, 20, 5)
            run_button = st.button("Ejecutar clustering")
            params = {"eps": eps, "min_samples": min_samples}
    else:
        run_button = False

# -----------------------------------------------------------------------------
# Main content
# -----------------------------------------------------------------------------
if uploaded_file is None:
    st.info("📂 Carga un archivo CSV en la barra lateral para comenzar.")
    st.stop()

# Load data
try:
    df_raw = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
    st.stop()

st.subheader("Vista previa de los datos")
st.dataframe(df_raw.head())

# Run clustering when user clicks button
if run_button:
    with st.spinner("⏳ Ejecutando clustering..."):
        try:
            result_df, sil_score, inertia = cluster_data(df_raw, algorithm, **params)
        except Exception as e:
            st.error(f"Se produjo un error durante el clustering: {e}")
            st.stop()

    # KPIs
    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Total registros", len(result_df))
    if sil_score is not None:
        kpi_cols[1].metric("Silhouette", f"{sil_score:.3f}")
    if inertia is not None:
        kpi_cols[2].metric("Inertia", f"{inertia:.2f}")

    # Scatter plot
    fig = px.scatter(
        result_df,
        x="pca1",
        y="pca2",
        color="cluster",
        title="Proyección 2D de Clusters (PCA)",
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed data
    with st.expander("Detalles de los datos con etiquetas de cluster"):
        st.dataframe(result_df)
