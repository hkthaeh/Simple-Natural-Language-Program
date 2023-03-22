import nltk
import sys
import os
import re

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

from math import log

from questions import load_files, tokenize, compute_idfs, top_files

FILE_MATCHES = 2
SENTENCE_MATCHES = 2

files = load_files('corpus')
file_words = {
    filename: tokenize(files[filename])
    for filename in files
}
file_idfs = compute_idfs(file_words)

# query = set(tokenize('What are the types of supervised learning?'))
# query = set(tokenize('When was Python 3.0 released?'))
query = set(tokenize('How do neurons connect in a neural network?'))


# rank = {}

# # loop through each word in the user inputed query
# for word in query:
#     # goes through each key and value in the files dictionary
#     for key, value in file_words.items():
#         #check to see if the word in query is in the value of the dictionary
#         if word in value:
#             # I used try because when there is no rank[key], a KeyError is outputed
#             # so in order to capture this error, I used try/except
#             try:
#                 # checks to see if the specific key already exist in the rank dictionary
#                 if rank[key]:
#                     # if so, we add upon its value
#                     rank[key] += value.count(word) * file_idfs[word]
#                     # and then break out of the files dictionary
#                     break
#             # if we encounter a key that is not already in the rank dictionary
#             except KeyError:
#                 # initiate the entry of the key into the rank dictionary
#                 rank[key] = value.count(word) * file_idfs[word]

# # sort the dictionary
# rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
# # returns the list of the keys in the rank dictionary, sliced by n
# print(list(rank.keys())[:1])

filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

# print(filenames)

sentences = dict()
for filename in filenames:
    for lines in files[filename]:
        for passage in lines.split("\n"):
            # print(passage)
            # break
            for sentence in nltk.sent_tokenize(passage):
                # print(sentence)
                tokens = tokenize(sentence)
                # print(tokens)
                if tokens:
                    sentences[sentence] = tokens

# print(sentences)

idfs = compute_idfs(sentences)
# print(idfs['standard'])

# matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)

# print(matches)

# def top_sentences(query, sentences, idfs, n):


rank = {}
unique_v = {}

for key, value in sentences.items():
    for word in query:
        if word in value:
            try:
                if rank[key]:
                    rank[key] += idfs[word]
            except KeyError:
                rank[key] = idfs[word]
print(rank)

for k, v in rank.items():
    try:
        if unique_v[v]:
            unique_v[v] += 1
    except KeyError:
        unique_v[v] = 1