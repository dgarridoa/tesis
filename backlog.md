

# Procesamiento
1. 2011-2016 sin nulos.
2. lista de stopwords.
3. diccionario de homologaciones.
4. lista de frases.
5. lemmatización

- Estudiar en que orden aplicar estas operaciones.

## 1. Stopwords
- Omitir palabras de interés que están en la lista de stopwords de nltk de spacy (**done**).

  Tras revisar la lista no se encontraron palabras de interés que deban quitar.

- Crear lista de stopwords contextuales (**done**).

  - Revisar con tiempo si existe alguna palabra que rescatar.
  - Hay palabras en la lista que son la fusión del stopwords con otra palabra (faltas ortográficas).

## 2. Homologaciones
  - Aplicar lemmatización
  - Estudiar palabras cuya semántica fue alterada al lemmatizar y se desee preservar su formato de origen.
  - Normalizar palabras relevantes no homologadas por lematización

## 3. Frases
 - Usar generador de frases para identificar frases claves.
 - Analizar el corpus por búsqueda de frases que puedieron quedar fuera.
 
# Implementar HDP
  - Sobre un año completo, probar con diferentes hiperparámetros hasta encontrar tópicos razonables.
  - Probar con dos años, con splits de un año.

# Implementar DHDP



# Comprensión del negocio
- Leer estudios sobre robo de vehículo en chile: estadísticas, tendencias, métodos de robo.
- Correlacionar estudio.
