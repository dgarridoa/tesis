import os
import pandas as pd
import json
import logging
from sklearn.feature_extraction.text import CountVectorizer
from tokenizer import tokenizer
from gensim.corpora import Dictionary
from gensim.corpora.bleicorpus import BleiCorpus

# get logger
logging.basicConfig(level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("processing-data")

logger.info("***Loading Data***")

# load args
with open("args.json", "r") as f:
    args = json.load(f)

# load documents
if args["target_data"]!="":
    # load data
    df = pd.read_csv(args["raw_data"], index_col = 'id_prose',
    usecols = ['id_prose', 'sin_fecha_siniestro', 'sin_relato'], sep=',')
    # change data type
    df['sin_fecha_siniestro'] = pd.to_datetime(df['sin_fecha_siniestro'])
    # sort by date
    df.sort_values('sin_fecha_siniestro', inplace=True)
    # select data between 2011-2016 and skip nulls
    df = df[(df['sin_fecha_siniestro']>=pd.Timestamp(2011,1,1)) 
        & (df['sin_fecha_siniestro']<pd.Timestamp(2017,1,1)) 
        & (df['sin_relato'].isnull()==False)]
    # export data
    path_to_export = args["raw_data"].split(".csv")[0]+".pkl"
    df.to_pickle(path_to_export) 
else:
    # load data
    df = pd.read_pickle(args["target_data"])

logger.info(f"Corpus size: {len(df)}")

# load stopwords
if args["stopwords"]!="":
    with open(args["stopwords"], "r") as f:
        stopwords = [line.strip() for line in f]
else:
    stopwords = None

# load dicionary with homologations
if args["homol_dict"]!="":
    with open(args["homol_dict"], "r") as f:
        homol_dict = json.load(f)
else:
    homol_dict = None

logger.info("***Data Processing***")
logger.info("Extracting Vocabulary")

tokenizer_args = {"stopwords": stopwords, "homol_dict": homol_dict, 
                "stemming": args["stemming"], "lemmatization": args["lemmatization"]}
tf_vectorizer = CountVectorizer(analyzer='word', tokenizer=lambda text: tokenizer(text, **tokenizer_args))
tf_vectorizer.fit(df['sin_relato'])
vocabulary = tf_vectorizer.get_feature_names()
frequency = tf_vectorizer.transform(df['sin_relato']).toarray().sum(axis=0)
word_freq = {'vocabulary':pd.Series(vocabulary), 'frequency': pd.Series(frequency)}
df_word_freq = pd.DataFrame(word_freq)

logger.info(f"Vocabulary size: {len(vocabulary)}")

# remove words with less of 10 ocurrence in corpus and with 3 char or less 
vocabulary = df_word_freq[(df_word_freq['frequency']>=10) & (df_word_freq['vocabulary'].str.len()>3)]['vocabulary'].to_list()

logger.info(f"Vocabulary size after elimination: {len(vocabulary)}")

# save vocabulary
if args["vocabulary"]!="":
    with open(args["vocabulary"], "w") as f:
        for word in vocabulary:
            f.write("%s\n" % word)

logger.info("*** Getting corpus in Blei’s LDA-C format ***")

# tokenized corpus using vocabulary
tokenizer_args = {"stopwords": stopwords, "homol_dict": homol_dict, "vocabulary": vocabulary, 
                "lemmatization": args["lemmatization"], "stemming": args["stemming"]}
corpus = [tokenizer(doc, **tokenizer_args) for doc in df['sin_relato']]
# remove empty documents
corpus = [doc for doc in corpus if len(doc)>0]

logger.info(f"Corpus size after elimination: {len(corpus)}")

# map each word to an id {id->word}
dictionary = Dictionary(corpus)
# a document is a list of tuples, each tuples has two element, the first is the id of the word and the second is its frequency
corpus = [dictionary.doc2bow(text) for text in corpus]

# save dictionary and corpus 
dictionary.save(args["dictionary"])
BleiCorpus.serialize(args["corpus"], corpus)

logger.info("***Data Processing Completed***")