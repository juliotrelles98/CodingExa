# Clustering Dashboard con Pandas y Streamlit

Este proyecto ofrece una aplicación **Streamlit** para cargar un dataset (CSV), ejecutar algoritmos de clustering (K-means o DBSCAN) y visualizar los resultados en un dashboard interactivo.

## Instalación rápida

1. Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución de la app

```bash
streamlit run App.py
```

Se abrirá tu navegador predeterminado en `http://localhost:8501` con el dashboard.

## Funcionamiento

1. Carga un archivo CSV usando la barra lateral.
2. Elige el algoritmo y ajusta sus parámetros.
3. Pulsa **Ejecutar clustering**.
4. Se muestra:
   * Gráfico de dispersión (PCA 2D) coloreado por cluster.
   * Métricas (Silhouette, Inertia).
   * Tabla interactiva con las etiquetas de cluster.

## Escalabilidad

Para datasets más grandes se puede migrar el módulo de clustering a **Dask DataFrame** o **PySpark** sin cambiar la interfaz de la app. También es posible desplegar la aplicación con **Docker** y escalar horizontalmente detrás de un balanceador de carga.

## Próximos pasos sugeridos

* Añadir autenticación (p.ej. OAuth2) si se expone públicamente.
* Programar ejecuciones automáticas (cron, Airflow) y almacenar resultados en una base de datos.
* Implementar nuevos algoritmos de clustering y validación automática de hiperparámetros.