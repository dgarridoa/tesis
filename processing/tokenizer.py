import re
import spacy
# https://github.com/pablodms/spacy-spanish-lemmatizer/
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
# python -m spacy_spanish_lemmatizer download wik
from nltk.stem import SnowballStemmer 

lemmatizer = spacy.load("es")
lemmatizer.add_pipe(SpacyCustomLemmatizer(), name="lemmatizer", after="tagger")

stemmer = SnowballStemmer('spanish')

def tokenizer(doc, sep=None, stopwords = None, homol_dict=None, vocabulary = None, lemmatization=False, stemming = False):
    '''
    Extracts a list of processed words from a document.

    Input
        doc: str, 
            document.
        sep: str, 
            split char, by defect space is used.
        stopwords: list[str], optional
            list of word to remove.
        homol_dict: dict, optional
            dictionary with homologations between words.
        vocabuary: list[str], optional
            list of word allowed.
        lemmatization: bool, default False
            if is True takes the words to their lemma.
        stemming: bool, default False
            if is True takes the words to their stem.

    Output
        tokens: list[str], 
            list of processed words.
    '''
    doc = re.sub(r'\S+@\S+', '', doc) # remove e-mails
    doc = re.sub(r'[\xa0]', '', doc) # remove pattern \xa0
    doc = re.sub(r'[^\w\s]','', doc) # remove punctuation symbols except underscore
    doc = re.sub(r'[_]', '', doc) # remove underscore
    doc = re.sub(r'[a-zA-Z]+[0-9]+', '', doc) # remove tokens with letters and numbers 
    doc = re.sub(r'([ø ÿ þ])', ' ', doc) # replace ø ÿ þ by space
    doc = re.sub(r'[0-9]', '', doc) # remove numbers
    tokens = doc.split(sep) # tokenization
    tokens = [word.lower() for word in tokens] # to lowercase

    # remove stopwords
    if stopwords is not None:
        tokens = [word for word in tokens if word not in stopwords]
    # filter by vocabulary
    if vocabulary is not None:
        tokens = [word for word in tokens if word in vocabulary]
    # homologate word with similar meaning
    if homol_dict is not None:
        for i, word in enumerate(tokens):
            for key in homol_dict.keys():
                if word in homol_dict[key]:
                    tokens[i] = key
                    break        
    # take the words to their lemma
    if lemmatization is True:
        doc = " ".join(tokens)
        tokens = [token.lemma_ for token in lemmatizer(doc)]
    # take the words to their stem
    if stemming is True:
        tokens = [stemmer.stem(word) for word in tokens]
    return tokens