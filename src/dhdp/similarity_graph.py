import os
import json
import numpy as np
import pandas as pd
import logging
from time import time
from gensim.corpora import Dictionary
from gensim.models import KeyedVectors
from similarity_measures import compute_similarity, get_topic_topn
from dotenv import load_dotenv

# get logger
logging.basicConfig(format='%(asctime)s : %(message)s', level = os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger("similarity-graph")

# load environment variables
load_dotenv()
corpus = os.getenv("CORPUS")
model_path = os.getenv("MODEL_PATH")
similarity = os.getenv("SIMILARITY")
embeddings_path = os.getenv("EMBEDDINGS")
q = float(os.getenv("TOPIC_QUANTILE_THRESHOLD"))
topn = int(os.getenv("TOPN"))
graph_dir = os.getenv("GRAPH_PATH")

logger.info("Loading Data")

dict_files = sorted([file for file in os.listdir(corpus) if ".dict" in file])
models_dir = sorted(os.listdir(model_path))

epochs = range(0, len(models_dir))
data = {}
for epoch in epochs:
    # load dictionary {word->id}
    dict_path = f'{corpus}{dict_files[epoch]}'
    token2id = Dictionary.load(dict_path).token2id

    # load topics distributions
    topics_path = f'{model_path}{models_dir[epoch]}/mode-topics.dat'
    with open(topics_path, "r") as f:
        topics = np.array([[int(word) for word in line.strip().split()] for line in f])
    topics_dists = (topics.T/topics.sum(axis=1)).T

    # load word assignments and get mixture weigths
    word_assignments_path = f'{model_path}{models_dir[epoch]}/mode-word-assignments.dat'
    word_assignments = []
    with open(word_assignments_path, "r") as f:
        lines = f.readlines()[1:]

        # (doc_id, word_id, topic_id, x)
        for line in lines:
            line = line.strip().split()
            word_assignments.append(int(line[2]))

    tokens = len(word_assignments)
    mixture_weights = np.unique(word_assignments, return_counts=True)[1]/tokens

    # save data in a dict
    data[epoch] = {"token2id": token2id, "topics_dists": topics_dists, "mixture_weights":mixture_weights}

if similarity == "wmd":
    logger.info("Loading Embeddings")
    embeddings = KeyedVectors.load_word2vec_format(embeddings_path)
else:
    embeddings = None

logger.info("Computing Similarity Graph")
ti = time()
similarity_graph = {"nodes":[], "edges":[], "matrix":[]}
for epoch in epochs[:-1]:
    logger.info(f"Steps :{epoch}/{epochs[-1]}")
    t1 = time()

    # get vocabularies and topics distributions by epoch
    token2id1 = data[epoch]["token2id"]
    token2id2 = data[epoch+1]["token2id"]
    topics_dists1 = data[epoch]["topics_dists"]
    topics_dists2 = data[epoch+1]["topics_dists"]
    K1 = len(topics_dists1)
    K2 = len(topics_dists2)

    # save similarities in a matrix
    similarity_matrix = np.zeros((K1, K2))
    for i in range(K1):
        topic_i = topics_dists1[i]
        for j in range(K2):
            topic_j = topics_dists2[j]

            # get similarity
            similarity_matrix[i,j] = compute_similarity(
                    similarity,
                    embeddings,
                    token2id1,
                    token2id2,
                    topic_i,
                    topic_j,
                    q = q
            )

            # update similarity graph with edge data
            similarity_graph["edges"].append({
                "s": f"{epoch+1}-{i+1}",
                "t": f"{epoch+2}-{j+1}",
                "w": similarity_matrix[i,j]
            })

        # update similarity graph with node data
        topn_words = get_topic_topn(token2id1, topic_i, topn)
        similarity_graph["nodes"].append({
            "epoch":epoch+1,
            "id": i+1,
            "size": data[epoch]["mixture_weights"][i],
            "topn": topn_words
        })

    # update similarity graph with matrix data
    similarity_graph["matrix"].append(similarity_matrix.tolist())
    t2 = time()
    logger.info(f"Steps Completed: {epoch}/{epochs[-1]-1}, Time: {round(t2-t1)}")

# update similarity graph with last node
for j in range(K2):
    topic_j = topics_dists2[j]
    topn_words = get_topic_topn(token2id2, topic_j, topn)
    similarity_graph["nodes"].append({
        "epoch": epoch+2,
        "id": j+1,
        "size": data[epoch+1]["mixture_weights"][j],
        "topn": topn_words
    })
tf = time()
logger.info(f"Total Time [s]: {round(tf-ti)}")

logger.info(f"Saving Graph")
graph_path = f'{graph_dir}graph_{similarity}_q{int(100*q)}.json'
with open(graph_path, "w") as f:
    json.dump(similarity_graph, f)
