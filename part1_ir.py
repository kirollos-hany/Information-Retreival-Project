# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 08:40:10 2021

@author: Malak-pc
"""

#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words      = stopwords.words('english')
word_lemmitizer = WordNetLemmatizer()

#function to read file and return its data
def read_file(path):
    f = open(path, "r")
    data=f.read()
    f.close()
    return data

#read documents

documents={
          "doc1"  : read_file("doc1.txt"),
          "doc2"  : read_file("doc2.txt"),
          "doc3"  : read_file("doc3.txt"),
          "doc4"  : read_file("doc4.txt"),
          "doc5"  : read_file("doc5.txt"),
          "doc6"  : read_file("doc6.txt"),
          "doc7"  : read_file("doc7.txt"),
          "doc8"  : read_file("doc8.txt"),
          "doc9"  : read_file("doc9.txt"),
          "doc10" : read_file("doc10.txt")
}
punctuations="?:!.,;"

tokenized_documents={}

def tokenize ():
    for key, value in documents.items():
        tokenized_documents[key]= word_tokenize(value) #tokenize documents
        tokenized_documents[key]= [t.casefold() for t in tokenized_documents[key]] #case folding
        tokenized_documents[key]= [t for t in tokenized_documents[key] if not t in stop_words] #remove stop words
        tokenized_documents[key]= [word_lemmitizer.lemmatize(t) for t in tokenized_documents[key]] #apply lemmitizer
        tokenized_documents[key]= [t for t in tokenized_documents[key] if not t in punctuations] #remove punctuations
    return tokenized_documents
