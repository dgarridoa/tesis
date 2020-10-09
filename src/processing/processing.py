import pandas as pd
import os
import shutil
import logging
from dotenv import load_dotenv
from tokenizer import tokenizer
from gensim.corpora import Dictionary
from gensim.corpora.bleicorpus import BleiCorpus
from time import time

# get logger
logging.basicConfig(format='%(asctime)s : %(message)s', level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("processing-data")

logger.info("Loading Data")

# load environment variables
load_dotenv()

# load documents, columns = ["text", "epoch"]
df = pd.read_pickle(os.getenv("DATA"))

# load stopwords
if os.getenv("STOPWORDS")!="":
    with open(os.getenv("STOPWORDS"), "r") as f:
        stopwords = [line.strip() for line in f]
else:
    stopwords = None

# load vocabulary
if os.getenv("VOCABULARY")!="":
    with open(os.getenv("VOCABULARY"), "r") as f:
        vocabulary = [line.strip() for line in f]
else:
    vocabulary = None

# load dictionary with homologations between words.
if os.getenv("HOMOL_DICT")!="":
    with open(os.getenv("HOMOL_DICT"), "r") as f:
        homol_dict = [line.strip() for line in f]
else:
    homol_dict = None

# stemming and lemmatization
if os.getenv("STEMMING") == "true":
    stemming = True
else:
    stemming = None
if os.getenv("LEMMATIZATION") == "true":
    lemmatization = True
else:
    lemmatization = None

# make folder to export results
path_to_save = f'{os.getenv("CORPUS")}'
if os.path.exists(path_to_save):
    # remove pre executions
    shutil.rmtree(path_to_save)
os.makedirs(path_to_save)

logger.info("Data Processing")
ti = time()
epochs = df["epoch"].unique()
for epoch in epochs:
    logger.info(f"Epochs Completed: {epoch}/{epochs[-1]}")
    logger.info(f"Processing docs in epoch: {epoch}")
    
    # docs from actual epoch
    docs = df[df["epoch"] == epoch]["text"]
    logger.info(f"Corpus size: {len(docs)}")

    # processing docs from actual epoch
    tokenizer_args = {"stopwords": stopwords, "vocabulary": vocabulary, 
    "homol_dict": homol_dict, "stemming": stemming, "lemmatization":lemmatization}
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
    
    # new vocabulary and corpus
    vocab = list(dictionary.token2id.keys())
    corpus = [[word for word in doc if word in vocab] for doc in corpus]
    # remove documents with less than DOC_LEN words
    corpus = [doc for doc in corpus if len(doc)>=float(os.getenv("DOC_LEN"))]
    logger.info(f"Corpus size after elimination of docs with less than {os.getenv('DOC_LEN')} words: {len(corpus)}")

    logger.info("Getting corpus in Blei’s LDA-C format")
    # a document is a list of tuples, each tuples has two element, the first is the id of the word and the second is its frequency
    dictionary = Dictionary(corpus)
    corpus = [dictionary.doc2bow(doc) for doc in corpus]
    
    # save dictionary and corpus in LDA-C format
    logger.info("Saving Corpus")
    zeros = "0"*(len(str(epochs[-1]))-len(str(epoch)))
    epoch_string = f"{zeros}{epoch}"
    dictionary.save(f"{path_to_save}dictionary_{epoch_string}.dict")
    BleiCorpus.serialize(f"{path_to_save}corpus_{epoch_string}.mm", corpus)
tf = time()
logger.info("Data Processing Completed")
total_time = round(tf-ti)
logger.info(f"Processing time: {total_time} [s]")