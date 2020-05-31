# Procesamiento de relatos
## Actualizar
El presente directorio contiene todo lo relacionado al procesamiento de los relatos. Descripción del contenido:

1. **resume.ipynb**: notebook con algunas estadísticas descriptivas sobre `robos_prose.csv`. Del notebook se justifica que la elección de la muestra son los relatos de los años 2011-2016.
2. **processing.ipynb**: notebook que procesa los relatos, no se encuentra en estado finalizado, aún se puede afinar el procesamiento de los relatos y en el mismo documento se describen direcciones de mejora.
3. **processing.py**: contiene el mismo código del notebook anterior pero en un estado productivo, este archivo tras procesar los datos los exporta en un formato adecuado para el entrenamiento de modelos de tópicos, exportando los siguientes archivos en `data/`:
  - `robos_prose_v1.pkl`: subconjunto de `robos_prose.csv`, solo considera relatos no nulos de los años 2011-2016, su header es `id_pose|sin_fecha_siniestro|sin_relato`.
  - `vocabulary.pickle`: objeto tipo lista con el vocabulario.
  - `dictionary.dict`: diccionario que encapsula el mapeo entre palabras y sus ids.
  - `corpus.mm`: serialización del corpus usando usando una *sparse coordinate Matrix market format*, , es decir, el corpus se guarda como una lista de listas, donde cada documento es representado por una lista de tuplas, donde cada tupla contiene dos elementos, el primer elemento es una id de una palabra y el segundo la frecuencia dentro del documento (siempre mayor a cero).
4. **tokenizer.py**: función de tokenización, es usada en `data_processing.py`.
