# Dynamic Topic Model (DTM)

Prueba de concepto usando DTM sobre la base de datos de **robos_prose.csv** para *K=2,...,10*. El directorio cuenta con los siguientes archivos relevantes.

1. **dtm_model.ipynb**: notebook que post procesa *robos_prose_clean_2.0.xlsx* eliminando palabras con frecuencia menor a 10, reduciendo el vocabulario a  5.430 y exporta el corpus en formato gensim `corpora.mm` y `dictionary.dict`. Además entrena DTM (Ejecutable: `dtm-win64.exe`) y exporta los modelos entrenados.
2. **dtm_evaluation.ipynb**: notebook que exporta data para evaluar la calidad de los modelos.
3. **dtm_vis/**: directorio con el archivo **demo.html**,archivo que muestra tres visualizaciones:
  - Dos métricas en función del número de tópicos.
  - Serie de tiempo de los tópicos en el tiempo.
  - LDAVis: muestra la relación entre los tópicos y la relevancia de las palabras en un tópico. Eeste gráfico es parámetrizable por:
    - `K`: número de tópicos, K debe estar entre 2 y 10, por ejemplo, `K=10`.
    - `slice`: partición temporal, debe ser un mes en inglés abreviado Jan-Dec y un año entre 2011-2016, por ejemplo, `slice=Jan 2011`.

Repositorio del modelo:
- https://github.com/magsilva/dtm
