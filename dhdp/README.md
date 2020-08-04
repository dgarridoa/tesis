# Dynamic Hierarchical Dirichlet Process (DHDP)
## Actualizar
El presente directorio contiene la implementación del algoritmo de clustering dinámico propuesto para el trabajo de tesis. Para esto el algoritmo supone que el corpus está divido en épocas y entrena de forma independiente HDP en cada una de ellas, luego cálcula el grafo de similitud entre tópicos de épocas adyacentes para luego fijar un umbral que definirá las relaciones entre tópicos adyacentes, como nacimiento, muerte, evolución, división y fusión.


- **hdp/**: carpeta con <a href="https://github.com/blei-lab/hdp">HDP C++</a>. El código original está intacto, solo se actualizó el README, agregando ejemplos de uso.
- **run_hdp.sh**: main de ejecución de HDP, ejecuta HDP sobre cada una de las épocas y guarda los resultados en `results/hdp`.
- **wmd.py**: código para computar Word Mover's Distance (WMD).
- **similarity_graph.py**: main de ejecución de wmd. Carga los vocabularios, los resultados de HDP y los embeddings para computar WMD y construir el grafo de similitud que guarda en `results/graph`.
- **results/**: carpeta donde se guardan los resultados del modelo.
    - **graph/**: contiene el grafo de similitud en .pkl y visualizaciones del grafo en .html.
    - **hdp/**: guarda el output de HDP en subcarpetas. Para más detalles sobre los archivos que genera HDP en su entrenamiento leer `hdp/README.md`.
    - **topics/**: visualización interactiva de los resultados del modelo. Contiene el grafo de similitud y una visualización para interpretar los tópicos generada con <a href="https://github.com/cpsievert/LDAvis">LDAvis</a> (<a href="https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf">paper</a>). Contiene un formulario para actualizar la visualización de LDAvis en función de la época que se quiere inspeccionar. Para poder ver la visualización ejecutar `python -m http.server`.
- **fasttext-sbwc.bin**: binario con los embeddings obtenidos al aplicar FasText sobre el corpus Spanish Billion Word Corpus (<a href="https://crscardellino.github.io/SBWCE/">SBWC</a>). Los embeddings están disponible en este <a href="https://github.com/dccuchile/spanish-word-embeddings#fasttext-embeddings-from-sbwc">link</a>.
- **graph_analysis.ipynb**: notebook que genera una visualizacipon del grafo de similitud y permite experimentar con distintos threshold para el pruning de los arcos.
- **wmd_analysis.ipynb**: notebook con análisis de la distribución acumulada de los tópicos y tiempo de ejecución de WMD en función del tamaño de vocabulario que explica un x% de la distribución acumulada del tópico.