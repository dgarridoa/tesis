# Modelamiento y seguimiento de tópicos para la deteción de modus operandi en robo de vehículos

El objetivo del trabajo de tesis es caracterizar los modus operandi de los delincuentes a partir de los relatos de víctimas de robo de vehículo entregados por la Asociación de Aseguradores de Chile (AACH).

Para este problema se cuenta con las fuentes de datos de la AACH, lo que corresponde a relatos de las víctimas del robo de sus vehículos desde el 2011 hasta el 2016, lo cual corresponde a 49.015 relatos. Cabe destacar que se estima que un tercio del parque automotriz se encuentra asegurado, por lo que se trabaja con una muestra del parque automotriz.

El resultado esperado es descubrir los modus operandi ocultos en los relatos de las víctimas y caracterizarlos a partir de las palabras, como también ver su evolución a través del tiempo, siendo capaz de detectar cuando nacen y mueren, y cómo cambian en el tiempo.

Para esto se propone utilizar un modelo de clustering dinámico como el propuesto en (Beykikhoshk et al., 2018), el algoritmo supone que el corpus está divido en épocas y entrena de forma independiente en cada una de ellas un modelo de tópicos no parámetrico llamado Hierarchical Dirichlet Process (HDP), luego cálcula un grafo de similitud entre tópicos de épocas adyacentes para luego fijar un umbral que definirá la relación entre tópicos adyacentes, como nacimiento, muerte, evolución, división y fusión.

La estructura del proyecto es la siguiente:

1. **<a href="https://drive.google.com/drive/folders/1UZjx2cZEWf6iaTmUbwOquR-8lIoKIrBh?usp=sharing">bib/</a>**: bibliografía.
2. **reports/**: reportes sobre el proyecto de tesis y del proyecto fondef. El LaTex de la tesis se encuentra en `tesis/`.
3. **<a href="https://drive.google.com/drive/folders/1UZjx2cZEWf6iaTmUbwOquR-8lIoKIrBh?usp=sharing">data/</a>**: almacena la base de datos de estudio `robos_prose.csv` y subproductos de este.
4. **processing/**: archivos de código para el procesamiento de relatos.
5. **dtm/**: prueba de concepto usando Dynamic Topic Model (DTM).
6. **dhdp/**: código con el modelo de clustering dinámico propuesto para el trabajo de tesis.

# Referencia

Beykikhoshk, A., Arandjelović, O., Phung, D., & Venkatesh, S. (2018). Discovering topic structures of a temporally evolving document corpus. Knowledge and Information Systems, 55(3), 599-632. <a href="https://link.springer.com/content/pdf/10.1007/s10115-017-1095-4.pdf">PDF</a>


# Variables de entorno

- `STOPWORDS`: ruta con archivo **.txt** con la lista de stopwords.
- `VOCABULARY`: ruta con archivo **.txt** con vocabulario base.
- `RAW_DATA`: ruta con **.csv** con los relatos.
- `TARGET_DATA`:  ruta con **.pkl** con los relatos, a diferencia de RAW_DATA solo contiene relatos no nulos entre 2011-2016.
- `LEMMATIZATION`: **true** si se desea aplicar lematización en el procesamiento, **false** sino.
- `STEMMING`: **true** si se desea aplicar stemming en el procesamiento, **false** sino.
- `NO_BELOW`: float ([0,1]), cada palabra debe estar presente en al menos un x% de los documentos de una época. 
- `NO_ABOVE`: float ([0,1]), cada palabra puede estar presente en a lo más un x% de los documentos de una época.
- `CORPUS`: carpeta donde se guardan los relatos procesados en el formato que requiere HDP.
- `EPOCH_TYPE`: nivel de división del corpus en épocas. Admite los siguientes tres valores: "month", "quarter" y "year".
- `EMBEDDINGS`: nombre del archivo binario con los embeddings. Debe estar dentro de la carpeta **dhdp/**.
- `RESULTS`: carpeta donde se guardan los resultados del modelo.
- `SIMILARITY`: medida de similitud a utilizar, `wmd`: word mover similarity, 
        `js`: jensen-shannon similarity, `cosine`: cosine similarity.
- `TOPIC_QUANTILE_THRESHOLD`: float ([0,1]), cuantil de la distribución acumulada de un tópico. Se utiliza para reducir el tamaño del vocabulario asociado a un tópico, considerando solo las top N palabras más probables que explican un x% de la distribución acumulada.
- `PRUNING_THRESHOLD`: float ([0,1]), cuantil de la distribución acumulada de la similitud. Se utiliza para podar el grafo, eliminando aquellos arcos con valor por debajo del quantil.

# Ejecución

Procesamiento de los relatos:

```bash
cd processing/
python processing.py
```

Correr HDP sobre cada una de las épocas:

```bash
cd dhdp/
./run.sh
```

Construir el grafo de similitud:

```bash
cd dhdp/
python similarity_graph.py
```

Visualización de los resultados:

```bash
cd dhdp/results/topics/
python -m http.server
```