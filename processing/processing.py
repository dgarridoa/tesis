import os
import shutil
import pandas as pd
import logging
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from tokenizer import tokenizer
from gensim.corpora import Dictionary
from gensim.corpora.bleicorpus import BleiCorpus

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

# get logger
logging.basicConfig(level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("processing-data")

logger.info("Loading Data")

# load environment variables
load_dotenv()

# load documents
if os.getenv("TARGET_DATA")!="":
    # load data
    df = pd.read_csv(os.getenv("RAW_DATA"), index_col = 'id_prose',
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
    path_to_export = os.getenv("RAW_DATA").split(".csv")[0]+".pkl"
    df.to_pickle(path_to_export) 
else:
    # load data
    df = pd.read_pickle(os.getenv("TARGET_DATA"))

# load stopwords
if os.getenv("STOPWORDS")!="":
    with open(os.getenv("STOPWORDS"), "r") as f:
        stopwords = [line.strip() for line in f]
else:
    stopwords = None
# stemming and lemmatization
if os.getenv("STEMMING") == "true":
    stemming = True
else:
    stemming = False
if os.getenv("LEMMATIZATION") == "true":
    lemmatization = True
else:
    lemmatization = False

logger.info("Data Processing")

# group corpus into slices
df.loc[:, "year"] = df.apply(lambda x: x["sin_fecha_siniestro"].year, axis=1)
df.loc[:, "month"] = df.apply(lambda x: x["sin_fecha_siniestro"].month, axis=1)
df.loc[:, "slice"] = 0
df_slices = split_docs(df, os.getenv("SLICE_TYPE"))
slices = df_slices["slice"].unique()

for row in df_slices.values: 
    year, month, slice = row[0], row[1], row[2]
    df.loc[(df["year"]==year) & (df["month"]==month), "slice"] = slice

# make folder to export results
path_to_save = f'{os.getenv("CORPUS")}{os.getenv("SLICE_TYPE")}/'
# if os.path.exists(path_to_save):
#     # remove pre executions
#     shutil.rmtree(path_to_save)
# os.makedirs(path_to_save)

for slice in slices:
    logger.info(f"Slices Completed: {slice-1}/{slices[-1]}")
    
    docs = df[df["slice"] == slice]["sin_relato"]
    logger.info(f"Corpus size: {len(docs)}")

    logger.info(f"Processing docs in slice: {slice}")
    tokenizer_args = {"stopwords": stopwords, "stemming": stemming, "lemmatization":lemmatization }
    corpus = [tokenizer(doc, **tokenizer_args) for doc in docs]
    
    logger.info("Extracting Vocabulary")
    # map each word to an id {id->word}
    dictionary = Dictionary(corpus)
    logger.info(f"Vocabulary size: {len(dictionary)}")

    # remove words with higher and lower frequency into the corpus
    lb = int(float(os.getenv("NO_BELOW"))*len(corpus))
    ub = int(float(os.getenv("NO_ABOVE"))*len(corpus))
    dictionary.filter_extremes(no_below=lb, no_above=ub)
    logger.info(f"Vocabulary size after elimination: {len(dictionary)}")
    
    logger.info("Getting corpus in Blei’s LDA-C format")
    # a document is a list of tuples, each tuples has two element, the first is the id of the word and the second is its frequency
    corpus = [dictionary.doc2bow(doc) for doc in corpus]
    # remove empty documents
    corpus = [doc for doc in corpus if len(doc)>0]
    # tokenized corpus using vocabulary
    logger.info(f"Corpus size after elimination of empty docs: {len(corpus)}")
    logger.info("Saving Corpus")
    # save dictionary and corpus 
    zeros = "0"*(len(str(slices[-1]))-len(str(slice)))
    slice_string = f"{zeros}{slice}"
    # dictionary.save(f"{path_to_save}dictionary_{slice_string}.dict")
    # BleiCorpus.serialize(f"{path_to_save}corpus_{slice_string}.mm", corpus)

logger.info("Data Processing Completed")