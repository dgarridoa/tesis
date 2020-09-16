import numpy as np
import pandas as pd
from pyemd import emd
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import jensenshannon


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


def add_padding(token2id1, token2id2, topic1, topic2, q):
    """
     Input
        token2id1: dict[str->int], 
            mapping between tokens and ids from topic 1.
        token2id2: dict[str->int], 
            mapping between tokens and ids from topic 2.
        topic1: numpy.array, 
            distribution from topic 1.
        topic2: numpy.array, 
            distribution from topic 2.
        q: float, optional, 
            quantile rate between [0-1], used to filter words with less probability in a topic.
            represents the top N most likely words in a topic, such that its cumulative distribution 
            adds up to q.
    Output
        topic1: float
            distribution from topic 1 with zero padding in words out of its vocabulary
        topic2: float
            distribution from topic 2 with zero padding in words out of its vocabulary
        vocabulary: set
            vocabulary from the union of topic1 and topic2
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
    topic1 = np.array([topic1[token2id1[word]] if word in vocabulary1 else 0 for word in vocabulary])
    topic2 = np.array([topic2[token2id2[word]] if word in vocabulary2 else 0 for word in vocabulary])  

    # normalize topic to sum 1
    topic1 = topic1/topic1.sum()
    topic2 = topic2/topic2.sum()

    return topic1, topic2, vocabulary


def cosine_similarity(token2id1, token2id2, topic1, topic2, q=None):
    """
    Input
        token2id1: dict[str->int], 
            mapping between tokens and ids from topic 1.
        token2id2: dict[str->int], 
            mapping between tokens and ids from topic 2.
        topic1: numpy.array, 
            distribution from topic 1.
        topic2: numpy.array, 
            distribution from topic 2.
        q: float, optional, 
            quantile rate between [0-1], used to filter words with less probability in a topic.
            represents the top N most likely words in a topic, such that its cumulative distribution 
            adds up to q.
    Output
        similarity: float
            cosine similarity between two topics.
    """
     # get topic distributions with zero padding
    topic1, topic2, _ = add_padding(token2id1, token2id2, topic1, topic2, q)
    # cosine similarity
    similarity = np.dot(topic1, topic2)/(np.linalg.norm(topic1)*np.linalg.norm(topic2))
    
    return similarity


def js_similarity(token2id1, token2id2, topic1, topic2, q=None):
    """
    Input
        token2id1: dict[str->int], 
            mapping between tokens and ids from topic 1.
        token2id2: dict[str->int], 
            mapping between tokens and ids from topic 2.
        topic1: numpy.array, 
            distribution from topic 1.
        topic2: numpy.array, 
            distribution from topic 2.
        q: float, optional, 
            quantile rate between [0-1], used to filter words with less probability in a topic.
            represents the top N most likely words in a topic, such that its cumulative distribution 
            adds up to q.
    Output
        similarity: float
            jensen-shannon similarity between two topics.
    """
    # get topic distributions with zero padding
    topic1, topic2, _ = add_padding(token2id1, token2id2, topic1, topic2, q)
    # jensen-shannon divergence 
    distance = jensenshannon(topic1, topic2)
    # map distance to similarity
    similarity = 1/(1+distance) 

    return similarity


def wmd(embeddings, token2id1, token2id2, topic1, topic2, q=None):
    """
    Input
        embeddings: gensim.models.keyedvectors.FastTextKeyedVectors, 
            words embeddings.
        token2id1: dict[str->int], 
            mapping between tokens and ids from topic 1.
        token2id2: dict[str->int], 
            mapping between tokens and ids from topic 2.
        topic1: numpy.array, 
            distribution from topic 1.
        topic2: numpy.array, 
            distribution from topic 2.
        q: float, optional, 
            quantile rate between [0-1], used to filter words with less probability in a topic.
            represents the top N most likely words in a topic, such that its cumulative distribution 
            adds up to q.
    Output
        distance: float
            word movers similarity between two topics.
    """
    # get topic distributions with zero padding
    topic1, topic2, vocabulary = add_padding(token2id1, token2id2, topic1, topic2, q)
    
    # compute euclidean distance matrix between vocabulary words
    vocabulary_array = np.array([embeddings[word] for word in vocabulary])
    distance_matrix = pairwise_distances(X=vocabulary_array, metric="euclidean", n_jobs=-1)
    distance_matrix = distance_matrix.astype("float64")
    distance_matrix = distance_matrix.copy(order="C")
    # compute Earth Mover Distances
    distance = emd(topic1, topic2, distance_matrix)
    # map distance to similarity
    similarity = 1/(1+distance) 

    return similarity


def compute_similarity(similarity_type, embeddings, token2id1, token2id2, topic1, topic2, q=None):
    """
    Input
        similarity_type: str
            similarity measure to use, {"wmd": word mover similarity, 
            "js": jensen-shannon similarity, "cosine": cosine similarity}.
        embeddings: gensim.models.keyedvectors.FastTextKeyedVectors, 
            words embeddings.
        token2id1: dict[str->int], 
            mapping between tokens and ids from topic 1.
        token2id2: dict[str->int], 
            mapping between tokens and ids from topic 2.
        topic1: numpy.array, 
            distribution from topic 1.
        topic2: numpy.array, 
            distribution from topic 2.
        q: float, optional, 
            quantile rate between [0-1], used to filter words with less probability in a topic.
            represents the top N most likely words in a topic, such that its cumulative distribution 
            adds up to q.
    Output
        distance: float
            compute similarity between two topics according to the similarity_type options
    """
    if similarity_type == "wmd":
        similarity = wmd(embeddings, token2id1, token2id2, topic1, topic2, q)
    elif similarity_type == "cosine":
        similarity = cosine_similarity(token2id1, token2id2, topic1, topic2, q)
    elif similarity_type == "js":
        similarity = js_similarity(token2id1, token2id2, topic1, topic2, q)
    else:
        raise ValueError("similarity_type must be in {'wmd', 'cosine', 'js'}") 
    
    return similarity
    