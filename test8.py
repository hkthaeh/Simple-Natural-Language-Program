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

for i in file_words.values():
    print(i)
    break
