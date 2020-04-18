#Preprocesamiento
import re
import spacy
from spacy.lang.es.stop_words import STOP_WORDS #importar set de stopwords
from nltk.stem import SnowballStemmer #importar stemmer
nlp = spacy.load('es_core_news_sm') #python -m spacy download es

## Función para procesar texto
def tokenizer(doc, sep=None, vocabulary = None, homol_dict=None, lemmatization=False, stemming = False):
    '''
    Por defecto divide la sentencia por el carácter espacio.
    Ej: 'Data Mining is the best course'->['Data',  'Mining', 'is', 'the', 'best', 'course']

    Input:
    1. doc: str, documento.
    2. sep: str, carácter para dividir el documento en tokens, por defecto es el espacio.
    3. vocabuary: set, si un vocabulario es dado filtra las palabras que no estan presentes en el.
    4. homol_dict: dict, diccionario de homologaciones.
    5. lemmatization: bool, si es True lleva las palabras a su lema.
    6. stemming: bool, si es True lleva las palabas a su raíz.

    Output:
    list, lista de tokens.

    Nota: aplicar stemming y lemmatization al mismo tiempo no es correcto.
    '''
    doc = re.sub(r'\S+@\S+', '', doc) #elimina correos electrónicos
    doc = re.sub(r'[\xa0]', '', doc) #elimina el patrón \xa0
    doc = re.sub(r'[^\w\s]','', doc) #elimina los símbolos de puntuación excepto underscore
    doc = re.sub(r'[_]', '', doc) #elimina underscore
    doc = re.sub(r'[a-zA-Z]+[0-9]+', '', doc) #elimina los tokens que contienen letras y números
    doc = re.sub(r'([ø ÿ þ])', ' ', doc) #reemplazas los símbolos contenidos por un espacio
    doc = re.sub(r'[0-9]', '', doc) #elimina los tokens númericos
    tokens = doc.split(sep) #tokenización
    tokens = [word.lower() for word in tokens] #pasar todas las palabras a minúsculas


    if vocabulary is not None:
        #solo considera caracteres que tokens que estan en vocabulary
        tokens = [word for word in tokens if word in vocabulary]

    #if homol_dict is not None:

    if lemmatization==True:
        tokens = [nlp(word)[0].lemma_ for word in tokens]

    if stemming == True:
        stemmer = SnowballStemmer('spanish')
        tokens = [stemmer.stem(word) for word in tokens]

    return tokens
