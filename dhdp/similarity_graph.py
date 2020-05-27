import os
import json
import numpy as np
import logging
from pyemd import emd
from gensim.corpora import Dictionary
from gensim.corpora.bleicorpus import BleiCorpus
from gensim.models.fasttext import load_facebook_vectors

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
        q1 = get_quantile(topic_1, q) 
        q2 = get_quantile(topic_2, q)
        # get indexs of useful tokens
        index1 = pd.Series(topic_1).sort_values(ascending=False).index[0:q1]
        index2 = pd.Series(topic_2).sort_values(ascending=False).index[0:q2]
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
    second_histogram = np.array([topic2[token2id2[word]] if word in vocabulary2 else 0 for word in vocabulary])    
    # compute euclidean distance matrix between vocabulary words
    vocabulary_array = np.array([embeddings[word] for word in vocabulary])
    distance_matrix = np.sqrt(np.sum((vocabulary_array[:, np.newaxis, :] - vocabulary_array[np.newaxis, :, :])**2, axis = -1))
    distance_matrix = distance_matrix.astype("float64")
    # compute Earth Mover Distances
    distance = emd(first_histogram, second_histogram, distance_matrix)
    return distance


# get logger
logging.basicConfig(level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("similarity-graph")

logger.info("***Loading Data***")

# load args
with open("../args.json", "r") as f:
    args = json.load(f)

path_corpus = f'{args["corpus"]}{args["slice_type"]}'
dict_files = sorted([file for file in os.listdir(path_corpus) if ".dict" in file])
path_models = f'{args["hdp_results"]}{args["slice_type"]}'
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

    #save data in a dict
    data[slice] = {"token2id": token2id, "topics_dists": topics_dists}

logger.info("***Loading Embeddings***")

embeddings = load_facebook_vectors(args["embeddings"])

logger.info("***Computing Similarity Graph***")

grap_similarity = {}
for slice in slices[:-1]:
    logger.info(f"***Steps Completed:{slice-1}/{slices[-1]-1}***")
    token2id1 = data[slice]["token2id"]
    token2id2 = data[slice+1]["token2id"]
    topics_dists1 = data[slice]["topics_dists"] 
    topics_dists2 = data[slice+1]["topics_dists"]
    for i, topic_i in enumerate(topics_dists1):
        for j, topic_j in enumerate(topics_dists2):
            distance = wmd(embeddings, token2id1, token2id2, topic_i, topic_j)
            grap_similarity[(slice, i, j)] = 1/(1+distance)

#args["prunning_threshold"]