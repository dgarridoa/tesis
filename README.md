# Modelamiento y seguimiento de tópicos para la deteción de modus operandi en robo de vehículos

En este trabajo se describe una metodología para el descubrimiento de tópicos en el tiempo. La metodología propuesta está basada en (i) discretización del corpus en épocas, (ii) descubrimiento de tópicos en cada época mediante Hierarchical Dirichlet Process (HDP), (iii) la construcción de un grafo de similitud entre tópicos de épocas adyacentes, el cual permite modelar cambios entre los tópicos como: nacimiento, muerte, evolución, división y fusión.

En contraste a trabajos anteriores, la metodología propuesta utiliza Word Mover’s Distance (WMD) como medida de similitud entre tópicos, medida que destaca por ser robusta a tópicos que no poseen un vocabulario común, debido a que trabaja con sus word embeddings.

Se reportan resultados experimentales tanto cuantitativos como cualitativos en el fenómeno de robo de vehículos en Chile, usando como corpus los relatos de víctimas de robo de vehículo entre los años 2011-2016 provistos por la Asociación de Aseguradores de Chile (AACH). El algoritmo propuesto logra capturar los tópicos latentes del corpus, descubriendo delitos tales como robo sin presencia del conductor, robo con violencia y “portonazo”.

La estructura del proyecto es la siguiente:

1. **tesis/**: Documento de la tesis. [[pdf](tesis/main.pdf)]
2. **slides/**: Presentación de la tesis. [[pdf](slides/main.pdf)]
3. **src/**: Código fuente con la implementación de la metodología.
4. **vis/**: Visualización interactiva de la salida del modelo. Para ver la visualización ejecutar:
```bash
cd vis
python -m http.server
```
5. **data/**: Directorio con la lista de stopwors y el vocabulario utilizado. Además contiene el json con la estructura del grafo temporal bajo distons úmbrales de poda.

# Principales referencias

- Teh, Y. W., Jordan, M. I., Beal, M. J., & Blei, D. M. (2006). Hierarchical dirichlet processes. Journal of the american statistical association, 101(476), 1566-1581. [[pdf](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.67.6544&rep=rep1&type=pdf)]
- Beykikhoshk, A., Arandjelović, O., Phung, D., & Venkatesh, S. (2018). Discovering topic structures of a temporally evolving document corpus. Knowledge and Information Systems, 55(3), 599-632. [[pdf](https://link.springer.com/content/pdf/10.1007/s10115-017-1095-4.pdf)]
- Kusner, M., Sun, Y., Kolkin, N., & Weinberger, K. (2015, June). From word embeddings to document distances. In International conference on machine learning (pp. 957-966). PMLR. [[pdf](http://proceedings.mlr.press/v37/kusnerb15.pdf)]
