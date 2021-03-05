import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter


def filter_text(text):
    """Returns a filtered version of a str ready for analysis

    Args:
        text (str): string of a speech

    Returns:
        str: filtered string of a speech
    """
    # remove all puntuation and uppercases
    text = re.sub("[^a-zA-Z]+", " ", text).lower()
    
    # lemmatize text
    lemmatizer = WordNetLemmatizer()
    text = lemmatizer.lemmatize(text)
    
    # remove common english stop words
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
    
    # return str of filtered text
    return " ".join(filtered_tokens)