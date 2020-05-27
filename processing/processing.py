import os
import shutil
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
with open("../args.json", "r") as f:
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

def split_docs(df, slice_type):
    """
    Input
        df: pandas.DataFrame, 
            corpus dataframe.
        slice_type: str, 
            type of temporal division of the corpus ('year', 'quarter' or 'month').
    Output
        df_slices: pandas.DataFrame, 
            dataframe with slice assignment for each pair of (year, month).
    """
    df_slices = df[["year", "month"]].drop_duplicates()
    df_slices.reset_index(inplace=True, drop=True)
    df_slices["slice"] = 0
    N = len(df_slices)
    if slice_type == "year":
        steps = 12
        M = int(N/steps)
        slices = range(1, M+1)
    elif slice_type == "quarter":
        steps = 3
        M = int(N/steps)
        slices = range(1, M+1)
    else:
        # slice_type == "month"
        steps = 1
        slices = range(1, N+1)

    for slice in slices:
        df_slices.loc[steps*(slice-1):steps*slice, "slice"] = slice

    return df_slices

# group corpus into slices
df.loc[:, "year"] = df.apply(lambda x: x["sin_fecha_siniestro"].year, axis=1)
df.loc[:, "month"] = df.apply(lambda x: x["sin_fecha_siniestro"].month, axis=1)
df.loc[:, "slice"] = 0
df_slices = split_docs(df, args["slice_type"])
slices = df_slices["slice"].unique()

for row in df_slices.values: 
    year, month, slice = row[0], row[1], row[2]
    df.loc[(df["year"]==year) & (df["month"]==month), "slice"] = slice

# make folder to export results
path_to_save = f'{args["corpus"]}{args["slice_type"]}/'
if os.path.exists(path_to_save):
    # remove pre executions
    shutil.rmtree(path_to_save)
os.makedirs(path_to_save)

for slice in slices:
    logger.info(f"***Slices Completed:{slice-1}/{slices[-1]}***")
    
    docs = df[df["slice"] == slice]["sin_relato"]
    logger.info(f"Corpus size: {len(docs)}")

    logger.info("Extracting Vocabulary")

    tokenizer_args = {"stopwords": stopwords, "homol_dict": homol_dict, 
                      "stemming": args["stemming"], "lemmatization": args["lemmatization"]}
    tf_vectorizer = CountVectorizer(analyzer='word', tokenizer=lambda text: tokenizer(text, **tokenizer_args))
    tf_vectorizer.fit(docs)
    vocabulary = tf_vectorizer.get_feature_names()
    frequency = tf_vectorizer.transform(docs).toarray().sum(axis=0)
    word_freq = {'vocabulary':pd.Series(vocabulary), 'frequency': pd.Series(frequency)}
    df_word_freq = pd.DataFrame(word_freq)

    logger.info(f"Vocabulary size: {len(vocabulary)}")

    # remove words with less frequency and with little chars
    vocabulary = df_word_freq[(df_word_freq['frequency']>=2) & (df_word_freq['vocabulary'].str.len()>3)]['vocabulary'].to_list()
    logger.info(f"Vocabulary size after elimination: {len(vocabulary)}")

    logger.info("Getting corpus in Blei’s LDA-C format")

    # tokenized corpus using vocabulary
    tokenizer_args = {"stopwords": stopwords, "homol_dict": homol_dict, "vocabulary": vocabulary, 
                      "lemmatization": args["lemmatization"], "stemming": args["stemming"]}
    corpus = [tokenizer(doc, **tokenizer_args) for doc in docs]
    # remove empty documents
    corpus = [doc for doc in corpus if len(doc)>0]

    logger.info(f"Corpus size after elimination of empty docs: {len(corpus)}")

    # map each word to an id {id->word}
    dictionary = Dictionary(corpus)
    # a document is a list of tuples, each tuples has two element, the first is the id of the word and the second is its frequency
    corpus = [dictionary.doc2bow(text) for text in corpus]

    logger.info("Saving Corpus")
    # save dictionary and corpus 
    zeros = "0"*(len(str(slices[-1]))-len(str(slice)))
    slice_string = f"{zeros}{slice}"
    dictionary.save(f"{path_to_save}dictionary_{slice_string}.dict")
    BleiCorpus.serialize(f"{path_to_save}corpus_{slice_string}.mm", corpus)

logger.info("***Data Processing Completed***")