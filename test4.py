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

from questions import load_files, tokenize, compute_idfs, top_files

question = 'What are the types of supervised learning?'

files = load_files('corpus')
file_words = {
    filename: tokenize(files[filename])
    for filename in files
}

file_idfs = compute_idfs(file_words)

filenames = top_files(question, file_words, file_idfs, n=FILE_MATCHES)

print(filenames)