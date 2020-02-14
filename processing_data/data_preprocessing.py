import pandas as pd

#Preprocesamiento
import re
import spacy
from spacy.lang.es.stop_words import STOP_WORDS #importar set de stopwords
from nltk.stem import SnowballStemmer #importar stemmer
nlp = spacy.load('es_core_news_sm') #python -m spacy download es
from sklearn.feature_extraction.text import CountVectorizer
from tokenizer import tokenizer

## Importar la base de datos
df = pd.read_csv('../data/robos_prose.csv', index_col = 'id_prose', usecols = ['id_prose', 'sin_fecha_siniestro', 'sin_relato'], sep=',')
# cambiar el tipo de dato a timestamp
df['sin_fecha_siniestro'] = pd.to_datetime(df['sin_fecha_siniestro'])
# ordenar relatos por fecha
df.sort_values('sin_fecha_siniestro', inplace=True)
# seleccionar relatos entre 2011-2016 y omitir registros con relatos nulos
df = df[(df['sin_fecha_siniestro']>=pd.Timestamp(2011,1,1)) & (df['sin_fecha_siniestro']<pd.Timestamp(2017,1,1)) & (df['sin_relato'].isnull()==False)]

# exportar dataframe
df.to_pickle('../data/robos_prose_v1.pkl')

#Importar la base de datos
df = pd.read_pickle('../data/robos_prose_v1.pkl')

## Reducción de vocabulario: Eliminación de stopwords y palabras poco frecuentes

# Creamos objetos para llevar el corpus a bag-of-words
tf_vectorizer = CountVectorizer(analyzer='word', tokenizer= tokenizer)

# Extraer vocabulario
tf_vectorizer.fit(df['sin_relato'])
vocabulary = tf_vectorizer.get_feature_names()
frequency = tf_vectorizer.transform(df['sin_relato']).toarray().sum(axis=0)
data = {'vocabulary':pd.Series(vocabulary), 'frequency': pd.Series(frequency)}
df_freq = pd.DataFrame(data)


# Extraer stopwords contextuales: palabras muy frecuentes que aportan poca información
stopwords_filter = ['veh', 'vh', 'culo', 'aut', 'camion', 'camión','rob', 'denun', 'dej',
                    'daño', 'dano', 'daos', 'perc' ,'sinies' ,'llev' ,'volver' ,'sali' ,
                    'hrs' ,'dedu' ,'hecho' , 'habia', 'busc' ,'regre' ,'aseg' ,
                    'frent' ,'comuna' ,'direcc' ,'aprox' ,'circun' ,'lleg' , 'afuera' ,
                    'hora' ,'indica' ,'ubica' ,'minut' ,'conta', 'presen', 'senal',
                    'señal', 'web', 'descrip', 'carabi', 'fech', 'avis', 'docu', 'ppu',
                    'dya', 'mario', 'medina', 'alcoholemiano'
                   ]
#ppu:patente, web: página web para denunciar

contextual_stopwords = set()

for word in stopwords_filter:
    words_to_filter = set(df_freq[df_freq['vocabulary'].str.contains(word)]['vocabulary'])
    contextual_stopwords = contextual_stopwords.union(words_to_filter)

not_stopwords = set(['autopista', 'autopistas', 'autoservicio', 'automático', 'algarrobo', 'petrobras'])
contextual_stopwords = contextual_stopwords-not_stopwords
contextual_stopwords = contextual_stopwords.union(set(['via', 'vía', 'uf', 'numero', 'número']))

# Nuevo conjunto de stopwords
stopwords_set = STOP_WORDS.union(contextual_stopwords)

# Extraer palabras que aparecen almenos 10 veces en el corpus y tienen más de tres caracteres
most_freq_words = set(df_freq[(df_freq['frequency']>=10) & (df_freq['vocabulary'].str.len()>3)]['vocabulary'])

# Vocabulario final corresponde most_freq_words menos los elementos en stopwords_set
vocabulary = most_freq_words-stopwords_set
# Guardar vocabulario en ../data/ con como un objeto tipo set
with open('../data/vocabulary.pickle', 'wb') as f:
    pickle.dump(vocabulary, f, protocol=pickle.HIGHEST_PROTOCOL)




#Importar vocabulario
with open('../data/vocabulary.pickle', 'rb') as f:
    vocabulary = pickle.load(f)

#Corpus tokenizado utilizando el vocabulario
data_tokenized = [tokenizer(doc, vocabulary=vocabulary) for doc in df['sin_relato']]

#Creamos el diccionario a partir de los textos procesados en el formato que necesita LDA en gensim
dictionary = Dictionary(data_tokenized)

#Transformamos el corpus al formato que requiere la librería
#El corpus contiene una representacion numerica de los textos, un texto es representado por una lista de tuplas
#donde el primer elemento de la tupla es la id de la palabra y el segundo es su frecuencia de aparición en el texto.
corpus = [dictionary.doc2bow(text) for text in data_tokenized]

#Guardamos el diccionario y el corpus
dictionary.save('../data/dictionary.dict')
MmCorpus.serialize('../data/corpus.mm', corpus)
