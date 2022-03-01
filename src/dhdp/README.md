
# Dynamic Hierarchical Dirichlet Process (DHDP)
La metodología propuesta está basada en (i) discretización del corpus en épocas, (ii) descubrimiento de tópicos en cada época mediante Hierarchical Dirichlet Process (HDP), (iii) la construcción de un grafo de similitud entre tópicos de épocas adyacentes, el cual permite modelar cambios entre los tópicos como: nacimiento, muerte, evolución, división y fusión.

- **hdp/**: carpeta con <a href="https://github.com/blei-lab/hdp">HDP C++</a>. El código original está intacto, solo se actualizó el README, agregando ejemplos de uso.
- **run_hdp.sh**: main de ejecución de HDP, ejecuta HDP sobre cada una de las épocas y guarda los resultados en `results/hdp`. Con la variable de entorno `CORES` se puede ejecutar de forma paralela.
- **similarity_measures.py**: código para computar distintas medidas de similitud, entre ellas word mover similarity, jensen-shannon similarity y cosine similarity.
- **similarity_graph.py**: main de ejecución del grafo temporal. Carga los vocabularios, los resultados de HDP y los embeddings para computar WMD y construir el grafo de similitud temporal que guarda en la ruta especificada `GRAPH_PATH`.
- **evolution.ipynb**: notebook con análisis de sensibilidad de los dinámismos bajos diferentes úmbrales de pruning.
- **sampler.ipynb**: notebook con análisis de la distribución Dirichlet, Dirichlet Process y Gamma.
- **similarity_graph.ipynb**: notebook que genera una visualización de la cdf de similitud del grafo fully-connected y permite experimentar con distintos threshold para el pruning de los arcos.
- **speedup.ipynb**: notebook con análisis de la distribución acumulada de los tópicos y tiempo de ejecución de WMD en función del tamaño de vocabulario que explica un x% de la distribución acumulada del tópico.
- **topics_ldavis.ipynb**: notebook que genera una visualización interactiva de los resultados de HDP. La visualización es generada con <a href="https://github.com/cpsievert/LDAvis">LDAvis</a> [<a href="https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf">pdf</a>].
- `GRAPH_PATH`: carpeta donde guarda el grafo de similitud podado deacuerdo al úmbral en `PRUNING_THRESHOLD` formato **.json**.
- `MODEL_PATH`: carpeta donde se guarda el output de HDP en subcarpetas. Para más detalles sobre los archivos que genera HDP en su entrenamiento leer `hdp/README.md`.
