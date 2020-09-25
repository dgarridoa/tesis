import os
import pickle as pkl
import numpy as np
import pandas as pd
import logging
from time import time
from gensim.corpora import Dictionary
from gensim.models import KeyedVectors
from similarity_measures import compute_similarity
from dotenv import load_dotenv

# get logger
logging.basicConfig(format='%(asctime)s : %(message)s', level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("similarity-graph")

# load environment variables
load_dotenv()

logger.info("Loading Data")

dict_files = sorted([file for file in os.listdir(os.getenv("CORPUS")) if ".dict" in file])
models_dir = sorted(os.listdir(os.getenv("MODEL_PATH")))

epochs = range(0, len(models_dir))
data = {}
for epoch in epochs:
    # load dictionary {word->id}
    dict_path = f'{os.getenv("CORPUS")}{dict_files[epoch]}'
    token2id = Dictionary.load(dict_path).token2id

    # load topics distributions
    topics_path = f'{os.getenv("MODEL_PATH")}{models_dir[epoch]}/mode-topics.dat'
    with open(topics_path, "r") as f:
        topics = np.array([[int(word) for word in line.strip().split()] for line in f])
    topics_dists = (topics.T/topics.sum(axis=1)).T

    # save data in a dict
    data[epoch] = {"token2id": token2id, "topics_dists": topics_dists}

if os.getenv("SIMILARITY") == "wmd":
    logger.info("Loading Embeddings")
    embeddings = KeyedVectors.load_word2vec_format(os.getenv("EMBEDDINGS"))
else:
    embeddings = None

logger.info("Computing Similarity Graph")
ti = time()
similarity_graph = []
for epoch in epochs[:-1]:
    t1 = time()
    logger.info(f"Steps :{epoch}/{epochs[-1]}")
    token2id1 = data[epoch]["token2id"]
    token2id2 = data[epoch+1]["token2id"]
    topics_dists1 = data[epoch]["topics_dists"] 
    topics_dists2 = data[epoch+1]["topics_dists"]
    K1 = len(topics_dists1)
    K2 = len(topics_dists2)
    similarity_matrix = np.zeros((K1, K2))
    for i in range(K1):
        topic_i = topics_dists1[i]
        for j in range(K2):
            topic_j = topics_dists2[j]
            similarity_matrix[i,j] = compute_similarity(os.getenv("SIMILARITY"), embeddings, 
            token2id1, token2id2, topic_i, topic_j, 
            q = float(os.getenv("TOPIC_QUANTILE_THRESHOLD")))
    similarity_graph.append(similarity_matrix)
    t2 = time()
    logger.info(f"Steps Completed: {epoch}/{epochs[-1]-1}, Time: {round(t2-t1)}")
tf = time()
logger.info(f"Total Time [s]: {round(tf-ti)}")

logger.info(f"Saving Graph")
graph_path = f'{os.getenv("GRAPH_PATH")}/graph_{os.getenv("SIMILARITY")}_q{os.getenv("TOPIC_QUANTILE_THRESHOLD")}.pkl'
with open(graph_path, "wb") as f:
    pkl.dump(similarity_graph, f, pkl.HIGHEST_PROTOCOL)