# Dynamic Hierarchical Dirichlet Process (DHDP)
## Actualizar
El presente directorio contiene la implementación del algoritmo de clustering dinámico propuesto para el trabajo de tesis. Para esto el algoritmo supone que el corpus está divido en épocas y entrena de forma independiente HDP en cada una de ellas, luego cálcula el grafo de similitud entre tópicos de épocas adyacentes para luego fijar un umbral que definirá las relaciones entre tópicos adyacentes, como nacimiento, muerte, evolución, división y fusión.

- `poc_hdp_py/`: prueba de concepto de HDP en python, efectivamente ocurre que el número de tópicos inferidos es igual a la cota superior inpuesta en el número de tópicos a encontrar, por tanto, se descarta usar la implementación de python.
- `hdp/`: carpeta con HDP c++.
- `run_hdp.sh`
- `similarity_graph.py`
- `graph_analysis.ipynb`:
- `wmd_analysis.ipynb`:
- `hdp_vs_lda.ipynb`:
- `results/`:
- `fasttext-sbwc.bin`

## To do
- [x] poc hdp c++
- [ ] similarity graph
- [ ] visualizations
