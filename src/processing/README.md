# Procesamiento de relatos

El presente directorio contiene todo lo relacionado al procesamiento de los documentos. 

Descripción del contenido:

1. **tokenizer.py**: codigo con la función tokenize para procesar un documento,  es utilizados en `processing.py`.
2. **processing.py**: main de ejecución para procesar los documentos por época. Exporta los siguientes archivos en subcarpetas por época en la ruta `DATA`:
  - `dictionary.dict`: diccionario que encapsula el mapeo entre tokens y sus ids de una época particular.
  - `corpus.mm`: serialización del corpus de una época particular bajo el formato *sparse coordinate matrix*, es decir, el corpus se guarda como una lista de listas, donde cada documento es representado por una lista de tuplas, donde cada tupla contiene dos elementos, el primer elemento es una id de un token y el segundo la frecuencia dentro del documento (siempre mayor a cero).
3. **resume.ipynb**: notebook con algunas estadísticas descriptivas sobre de la base de datos utilizada.
4. **processing.ipynb**: notebook que describe todas las etapas de procesamiento aplicadas a los datos.
