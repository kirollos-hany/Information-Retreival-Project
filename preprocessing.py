from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

def tokenize(document):
    return word_tokenize(document)

def casefolding(tokens):
    return [t.casefold() for t in tokens]

def remove_stopwords(tokens):
    stop_words = stopwords.words('english')
    stop_words.remove('to')
    stop_words.remove('where')
    stop_words.remove('in')
    return [t for t in tokens if not t in stop_words]

def lemmatize(tokens):
    word_lemmatizer = WordNetLemmatizer()
    return [word_lemmatizer.lemmatize(t) for t in tokens]

def remove_punctuation(tokens):
    translator = str.maketrans('', '', string.punctuation)
    return [t.translate(translator) for t in tokens ]

def preprocess(document):
    tokens = tokenize(document)
    tokens = casefolding(tokens)
    tokens = remove_stopwords(tokens)
    tokens = remove_punctuation(tokens)
    tokens = lemmatize(tokens)
    return tokens