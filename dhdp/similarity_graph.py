import os
import pickle as pkl
import numpy as np
import pandas as pd
import logging
from time import time
from gensim.corpora import Dictionary
from gensim.models.fasttext import load_facebook_vectors
from wmd import wmd
from dotenv import load_dotenv

# get logger
logging.basicConfig(level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("similarity-graph")

# load environment variables
load_dotenv()

logger.info("Loading Data")

corpus_dir = f'{os.getenv("CORPUS")}{os.getenv("SLICE_TYPE")}'
dict_files = sorted([file for file in os.listdir(corpus_dir) if ".dict" in file])
models_path = f'{os.getenv("RESULTS")}hdp/{os.getenv("SLICE_TYPE")}'
models_dir = sorted(os.listdir(models_path))

slices = range(1, len(models_dir)+1)
data = {}
for slice in slices:
    # load dictionary {word->id}
    dict_path = f'{corpus_dir}/{dict_files[slice-1]}'
    token2id = Dictionary.load(dict_path).token2id

    # load topics distributions
    topics_path = f'{models_path}/{models_dir[slice-1]}/mode-topics.dat'
    with open(topics_path, "r") as f:
        topics = np.array([[int(word) for word in line.strip().split()] for line in f])
    topics_dists = (topics.T/topics.sum(axis=1)).T

    # save data in a dict
    data[slice] = {"token2id": token2id, "topics_dists": topics_dists}

logger.info("Loading Embeddings")

embeddings = load_facebook_vectors(os.getenv("EMBEDDINGS"))

logger.info("Computing Similarity Graph")
ti = time()
similarity_graph = []
for slice in slices[:-1]:
    t1 = time()
    logger.info(f"Steps :{slice-1}/{slices[-1]-1}")
    token2id1 = data[slice]["token2id"]
    token2id2 = data[slice+1]["token2id"]
    topics_dists1 = data[slice]["topics_dists"] 
    topics_dists2 = data[slice+1]["topics_dists"]
    K1 = len(topics_dists1)
    K2 = len(topics_dists2)
    similarity_edges = np.zeros((K1, K2))
    for i in range(K1):
        topic_i = topics_dists1[i]
        for j in range(K2):
            topic_j = topics_dists2[j]
            distance = wmd(embeddings, token2id1, token2id2, topic_i, topic_j, q = float(os.getenv("TOPIC_QUANTILE_THRESHOLD")))
            similarity = 1/(1+distance)
            similarity_edges[i,j] = similarity
    similarity_graph.append(similarity_edges)
    t2 = time()
    logger.info(f"Steps Completed: {slice}/{slices[-1]-1}, Time: {round(t2-t1)}")
tf = time()
logger.info(f"Total Time [s]: {round(tf-ti)}")

logger.info(f"Saving Graph")
graph_path = f'{os.getenv("RESULTS")}graph/graph_{os.getenv("SLICE_TYPE")}.pkl'
with open(graph_path, "wb") as f:
    pkl.dump(similarity_graph, f, pkl.HIGHEST_PROTOCOL)