# Procesamiento de relatos

El presente directorio contiene todo lo relacionado al procesamiento de los relatos. Descripción del contenido:

1. **tokenizer.py**: codigo para procesar los relatos,  es utilizados en `processing.py`.
2. **processing.py**: main de ejecución para procesar los relatos. Exporta los siguientes archivos en `data/`:
  - `robos_prose.pkl`: subconjunto de `robos_prose.csv`, solo considera relatos no nulos de los años 2011-2016, su header es *id_pose|sin_fecha_siniestro|sin_relato*.
  - `dictionary.dict`: diccionario que encapsula el mapeo entre palabras y sus ids de una época particular.
  - `corpus.mm`: serialización del corpus de una época particular bajo el formato *sparse coordinate matrix*, es decir, el corpus se guarda como una lista de listas, donde cada documento es representado por una lista de tuplas, donde cada tupla contiene dos elementos, el primer elemento es una id de una palabra y el segundo la frecuencia dentro del documento (siempre mayor a cero).
3. **resume.ipynb**: notebook con algunas estadísticas descriptivas sobre `robos_prose.csv`. Del notebook se justifica que la elección de la muestra son los relatos de los años 2011-2016.
4. **processing.ipynb**: notebook que describe todas las etapas de procesamiento aplicadas a los datos.
