# Modelamiento y seguimiento de tópicos para la deteción de modus operandi en robo de vehículos

En este trabajo se describe una metodología para el descubrimiento de tópicos en el tiempo. La metodología propuesta está basada en (i) discretización del corpus en épocas, (ii) descubrimiento de tópicos en cada época mediante Hierarchical Dirichlet Process (HDP), (iii) la construcción de un grafo de similitud entre tópicos de épocas adyacentes, el cual permite modelar cambios entre los tópicos como: nacimiento, muerte, evolución, división y fusión.

La estructura del proyecto es la siguiente:

- **processing/**: código para procesar los documentos.
- **dhdp/**: código con la implementación del modelo de clustering dinámico.
- **data/**: path donde se guardan los documentos, stopwords, vocabulario y output del modelo. 

# Variables de entorno

- `DATA`: path del corpus almacenado como objeto dataframe en formato **.pkl**, columns ["text", "epoch"].
- `STOPWORDS`: path con lista de stopwords en formato **.txt**.
- `VOCABULARY`: path con vocabulario base en formato **.txt**.
- `LEMMATIZATION`: **true** si se desea aplicar lematización en el procesamiento, **false** sino.
- `STEMMING`: **true** si se desea aplicar stemming en el procesamiento, **false** sino.
- `NO_BELOW`: float ([0,1]), cada token debe estar presente en al menos un x% de los documentos de una época. 
- `NO_ABOVE`: float ([0,1]), cada token puede estar presente en a lo más un x% de los documentos de una época.
- `DOC_LEN`: número mínimo de tokens que debe tener un documento, los documentos bajo este número son eliminados.
- `CORPUS`: carpeta donde se guardan los documentos procesados por época en el formato que requiere HDP.
- `MODEL_PATH`: path donde se guarda la salida de HDP por época.
- `MAX_ITER`: número máximo de iteraciones del algoritmo de Gibbs Sampling en HDP.
- `GRAPH_PATH`: path donde se guarda el grafo temporal podado.
- `EMBEDDINGS`: path de los embeddings en formato **.vec**.
- `SIMILARITY`: medida de similitud a utilizar, `wmd`: word mover similarity, 
        `js`: jensen-shannon similarity, `cosine`: cosine similarity.
- `TOPIC_QUANTILE_THRESHOLD`: float ([0,1]), cuantil de la distribución acumulada de un tópico. Se utiliza para reducir el tamaño del vocabulario asociado a un tópico, considerando solo las top N palabras más probables que explican un x% de la distribución acumulada.
- `PRUNING_THRESHOLD`: float ([0,1]), cuantil de la distribución acumulada de la similitud. Se utiliza para podar el grafo, eliminando aquellos arcos con valor por debajo del quantil.
- `CORES`: número de núcleos a utilizar para paralelizar el entrenamiento de los HDP por época.
- `TOPN`: top n palabras que se mostraran en cada tópico en el grafo temporal, su utilidad aplica solamente a la visualización. 

# Ejecución

Procesamiento de los documentos:

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
mv data/graph/graph.json vis/data/graph.json
cd vis
python -m http.server
```
