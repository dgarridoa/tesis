import os
import json
import pickle as pkl
import numpy as np
import pandas as pd
import logging
from time import time
from sklearn.metrics import pairwise_distances
from pyemd import emd
from gensim.corpora import Dictionary
from gensim.corpora.bleicorpus import BleiCorpus
from gensim.models.fasttext import load_facebook_vectors


# get logger
logging.basicConfig(level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("similarity-graph")

def timeit(method):
    def timed(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.info('%r  %2.2f [s]' % (method.__name__, (te - ts)))
        return result
    return timed

def get_quantile(array, q=0.05):
    """
    Input
        array: numpy.array, 
            1D array.
        q: float, 
            quantile, defaut=0.05.
    Output
        quantile: int
            number of elements below 100q% of cumulative distribution of the array.
       
    """
    #cumulative distribution
    serie = pd.Series(array)
    serie_sorted = serie.sort_values(ascending=False)
    cum_dist = []

    cum = 0
    for value in serie_sorted:
        cum += value
        cum_dist.append(cum)

    cum_dist = pd.Series(cum_dist)
    
    #get quantile 
    cut = cum_dist.max()*q
    tail = np.array(cum_dist[cum_dist<=cut])
    if len(tail)>=1:
        quantile = np.argmax(tail)+1
    else:
        quantile = 1
    
    return quantile

@timeit
def wmd(embeddings, token2id1, token2id2, topic1, topic2, q=None):
    """
    Input
        embeddings: gensim.models.keyedvectors.FastTextKeyedVectors, 
            words embeddings.
        token2id1: dict[str->int], 
            mapping between tokens and ids from topic 1.
        token2id2: dict[str->int], 
            mapping between tokens and ids from topic 2.
        topic1: numpy.array[float64], 
            distribution from topic 1.
        topic2: numpy.array[float64], 
            distribution from topic 2.
        q: float64, optional, 
            quantile rate between [0-1], used to filter words with less probability in a topic.
            represents the top N most likely words in a topic, such that its cumulative distribution 
            adds up to q.
    Output
        distance: float64
            word movers distance between two topics.
    """
    
    if q:
        # get quantiles 
        q1 = get_quantile(topic1, q) 
        q2 = get_quantile(topic2, q)
        # get indexs of useful tokens
        index1 = pd.Series(topic1).sort_values(ascending=False).index[0:q1]
        index2 = pd.Series(topic2).sort_values(ascending=False).index[0:q2]
        # map id->token
        id2token1 = {v: k for k, v in token2id1.items()}
        id2token2 = {v: k for k, v in token2id2.items()}
        # get vocabulary from union of topic vocabularies
        vocabulary1 = set([id2token1[i] for i in index1])
        vocabulary2 = set([id2token2[i] for i in index2])
        vocabulary = vocabulary1.union(vocabulary2)
    else:
        # get vocabulary from union of topic vocabularies
        vocabulary1 = set(token2id1.keys())
        vocabulary2 = set(token2id2.keys())
        vocabulary = vocabulary1.union(vocabulary2)
    # topics distributions with padding
    first_histogram = np.array([topic1[token2id1[word]] if word in vocabulary1 else 0 for word in vocabulary])
    first_histogram = first_histogram/first_histogram.sum()
    second_histogram = np.array([topic2[token2id2[word]] if word in vocabulary2 else 0 for word in vocabulary])    
    second_histogram = second_histogram/second_histogram.sum()
    # compute euclidean distance matrix between vocabulary words
    vocabulary_array = np.array([embeddings[word] for word in vocabulary])
    distance_matrix = pairwise_distances(X=vocabulary_array, metric="euclidean", n_jobs=-1)
    distance_matrix = distance_matrix.astype("float64")
    distance_matrix = distance_matrix.copy(order="C")
    # compute Earth Mover Distances
    distance = emd(first_histogram, second_histogram, distance_matrix)
    return distance


logger.info("Loading Data")

# load args
with open("../args.json", "r") as f:
    args = json.load(f)

path_corpus = f'{args["corpus"]}{args["slice_type"]}'
dict_files = sorted([file for file in os.listdir(path_corpus) if ".dict" in file])
path_models = f'{args["results"]}hdp/{args["slice_type"]}'
models_dir = sorted(os.listdir(path_models))

slices = range(1, len(models_dir)+1)
data = {}
for slice in slices:
    # load dictionary {word->id}
    path_dict = f'{path_corpus}/{dict_files[slice-1]}'
    token2id = Dictionary.load(path_dict).token2id

    # load topics distributions
    path_topics = f'{path_models}/{models_dir[slice-1]}/mode-topics.dat'
    with open(path_topics, "r") as f:
        topics = np.array([[int(word) for word in line.strip().split()] for line in f])
    topics_dists = (topics.T/topics.sum(axis=1)).T

    # save data in a dict
    data[slice] = {"token2id": token2id, "topics_dists": topics_dists}

logger.info("Loading Embeddings")

embeddings = load_facebook_vectors(args["embeddings"])

logger.info("Computing Similarity Graph")
ti = time()
similarity_graph = []
for slice in slices[:-1]:
    logger.info(f"Steps Completed:{slice-1}/{slices[-1]-1}")
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
            distance = wmd(embeddings, token2id1, token2id2, topic_i, topic_j, q = args["topic_quantile_threshold"])
            similarity = 1/(1+distance)
            similarity_edges[i,j] = similarity
    similarity_graph.append(similarity_edges)
tf = time()
logger.info(f"Total Time [s]: {round(tf-ti)}")

logger.info(f"Saving Graph")
path_to_save_graph = f'{args["results"]}graph/graph_{args["slice_type"]}.pkl'
with open(path_to_save_graph, "wb") as f:
    pkl.dump(similarity_graph, f, pkl.HIGHEST_PROTOCOL)