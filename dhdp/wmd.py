import numpy as np
import pandas as pd
from pyemd import emd
from sklearn.metrics import pairwise_distances


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
