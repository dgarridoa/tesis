import pandas as pd
import re
import unidecode
import spacy
# https://github.com/pablodms/spacy-spanish-lemmatizer/
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
# python -m spacy_spanish_lemmatizer download wiki
from nltk.stem import SnowballStemmer 

lemmatizer = spacy.load("es")
lemmatizer.add_pipe(SpacyCustomLemmatizer(), name="lemmatizer", after="tagger")

stemmer = SnowballStemmer('spanish')

def tokenizer(doc, sep=None, stopwords=None, vocabulary=None, homol_dict=None, lemmatization=None, stemming=None):
    '''
    Extracts a list of processed words from a document.

    Parameters
    ----------
    doc: str
        document.
    sep: str, default=None 
        split char, by defect space is used.
    stopwords: list, default=None
        list of word to remove.
    vocabulary: list, default=None
        list of human readable words
    homol_dict: dict, default=None
        dictionary with homologations between words.
    lemmatization: bool,  default=None
        if is True takes the words to their lemma.
    stemming: bool,  default=None
        if is True takes the words to their stem.

    Returns
    -------
    tokens: list
        list of processed words.
    '''
    # transliterate an unicode object into an ASCII string
    # this remove accents
    doc = unidecode.unidecode(doc)
    doc = re.sub(r'\S+@\S+', '', doc) # remove e-mails
    doc = re.sub(r'[\xa0]', '', doc) # remove pattern \xa0
    doc = re.sub(r'[^\w\s]','', doc) # remove punctuation symbols except underscore
    doc = re.sub(r'[_]', '', doc) # remove underscore
    doc = re.sub(r'[a-zA-Z]+[0-9]+', '', doc) # remove tokens with letters and numbers 
    doc = re.sub(r'([ø ÿ þ])', ' ', doc) # replace ø ÿ þ by space
    doc = re.sub(r'[0-9]', '', doc) # remove numbers
    tokens = doc.split(sep) # tokenization
    # to lowercase and delete word with less than 4 chars
    tokens = [word.lower() for word in tokens if len(word)>3] 
    
    # map word to another of similar meaning
    if homol_dict:
        tokens = [homol_dict[word] if word in homol_dict else word for word in tokens]

    # remove stopwords
    if stopwords:
        tokens = [word for word in tokens if word not in stopwords]

    # filter by vocabulary
    if vocabulary:
        tokens = [word for word in tokens if word in vocabulary]

    # take the words to their lemma
    if lemmatization:
        doc = " ".join(tokens)
        if vocabulary:
             tokens = [unidecode.unidecode(word.lemma_) if unidecode.unidecode(word.lemma_) in vocabulary else word.text for word in lemmatizer(doc)]
        else:
            tokens = [unidecode.unidecode(word.lemma_) for word in lemmatizer(doc)]
    # take the words to their stem
    if stemming:
        if vocabulary:
            tokens = [stemmer.stem(word) if stemmer.stem(word) in vocabulary else word for word in tokens ]
        else:
            tokens = [stemmer.stem(word) for word in tokens]
    return tokens