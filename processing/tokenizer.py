import re
import spacy
#python -m spacy download es
from nltk.stem import SnowballStemmer 

lemmatizer = spacy.load('es_core_news_sm') 
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
    # homologate word with similar meaning
    if homol_dict is not None:
        for i, word in enumerate(tokens):
            for key in homol_dict.keys():
                if word in homol_dict[key]:
                    tokens[i] = key
                    break        
    # take the words to their lemma
    if lemmatization is True:
        tokens = [lemmatizer(word)[0].lemma_ for word in tokens]
    # take the words to their stem
    if stemming is True:
        tokens = [stemmer.stem(word) for word in tokens]
     # filter by vocabulary
    if vocabulary is not None:
        tokens = [word for word in tokens if word in vocabulary]

    return tokens