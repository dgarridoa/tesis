# Modelamiento y seguimiento de tópicos para la deteción de modus operandi en robo de vehículos

El objetivo del trabajo de tesis es caracterizar los modus operandi de los delincuentes a partir de los relatos de víctimas de robo de vehículo entregados por la Asociación de Aseguradores de Chile (AACH).

Para este problema se cuenta con las fuentes de datos de la AACH, lo que corresponde a relatos de las víctimas del robo de sus vehículos desde el 2011 hasta el 2016, lo cual corresponde a 49.015 relatos. Cabe destacar que se estima que un tercio del parque automotriz se encuentra asegurado, por lo que se trabaja con una muestra del parque automotriz.

El resultado esperado es descubrir los modus operandi ocultos en los relatos de las víctimas y caracterizarlos a partir de las palabras, como también ver su evolución a través del tiempo, siendo capaz de detectar cuando nacen y mueren, y cómo cambian en el tiempo.

Para esto se propone utilizar un modelo de clustering dinámico como el propuesto en (Beykikhoshk et al., 2018), el algoritmo supone que el corpus está divido en épocas y entrena de forma independiente en cada una de ellas un modelo de tópicos no parámetrico llamado Hierarchical Dirichlet Process (HDP), luego cálcula un grafo de similitud entre tópicos de épocas adyacentes para luego fijar un umbral que definirá la relación entre tópicos adyacentes, como nacimiento, muerte, evolución, división y fusión.

La estructura del proyecto es la siguiente:

1. **bib**: bibliografía.
2. **reports**: reportes sobre el proyecto de tesis y del proyecto fondef. El LaTex de la tesis se encuentra en `tesis/`.
3. **data**: almacena la base de datos de estudio `robos_prose.csv` y subproductos de este.
4. **processing**: archivos de código para el procesamiento de relatos.
5. **dtm**: prueba de concepto usando Dynamic Topic Model (DTM).
6. **dhdp**: código con el modelo de clustering dinámico propuesto para el trabajo de tesis.

# Referencia

Beykikhoshk, A., Arandjelović, O., Phung, D., & Venkatesh, S. (2018). Discovering topic structures of a temporally evolving document corpus. Knowledge and Information Systems, 55(3), 599-632. <a href="https://link.springer.com/content/pdf/10.1007/s10115-017-1095-4.pdf">PDF</a>

# <a href="https://drive.google.com/drive/folders/1UZjx2cZEWf6iaTmUbwOquR-8lIoKIrBh?usp=sharing">Drive</a>
