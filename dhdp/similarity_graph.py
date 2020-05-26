import os
import json
import numpy as np
import logging
from pyemd import emd
from gensim.corpora import Dictionary
from gensim.corpora.bleicorpus import BleiCorpus
from gensim.models.fasttext import load_facebook_vectors

def wmd(embeddings, token2id1, token2id2, topics_dists_1, topics_dists_2):
    vocabulary1 = set(token2id1.keys())
    vocabulary2 = set(token2id2.keys())
    vocabulary = vocabulary1.union(vocabulary2)
    distance_matrix = [((embeddings[word1]-embeddings[word2])**2).sum()**(1/2) for word1 in vocabulary for word2 in vocabulary]

    first_histogram = np.array([topics_dists_1[token2id1[word]] if word in vocabulary1 else 0 for word in vocabulary])
    second_histogram = np.array([topics_dists_2[token2id2[word]] if word in vocabulary2 else 0 for word in vocabulary])
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
    print(path_dict)
    token2id = Dictionary.load(path_dict).token2id

    # load topics distributions
    path_topics = f'{path_models}/{models_dir[slice-1]}/mode-topics.dat'
    print(path_topics)
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
    token2id_1 = data[slice]["token2id"]
    token2id_2 = data[slice+1]["token2id"]
    topics_dists_1 = data[slice]["topics_dists"] 
    topics_dists_2 = data[slice+1]["topics_dists"]
    for i, topic_i in enumerate(topics_dists_1):
        for j, topic_j in enumerate(topics_dists_2):
            distance = wmd(embeddings, token2id_1, token2id_2, topic_i, topic_j)
            grap_similarity[(slice, i, j)] = 1/(1+distance)


#args["prunning_threshold"]