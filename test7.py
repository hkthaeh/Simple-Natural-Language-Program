import nltk
import sys
import os
import re


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from math import log
from string import punctuation

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

from questions import load_files, tokenize, compute_idfs, top_files, top_sentences

# Calculate IDF values across files
files = load_files('corpus')
file_words = {
    filename: tokenize(files[filename])
    for filename in files
}
file_idfs = compute_idfs(file_words)

# Prompt user for query
query = set(tokenize('What are the types of supervised learning?'))
# query = set(tokenize('When was Python 3.0 released?'))
# query = set(tokenize('How do neurons connect in a neural network?'))

rank = {}

for word in query:
    # goes through each key and value in the files dictionary
    for key, value in file_words.items():
        #check to see if the word in query is in the value of the dictionary
        if word in value:
            # initiate the entry of the key into the rank dictionary
            try:
                if rank[key]:
                    rank[key] += value.count(word) * file_idfs[word]
            except KeyError:
                rank[key] = value.count(word) * file_idfs[word]
rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
print(rank)