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

# Calculate IDF values across files
files = load_files('corpus')
file_words = {
    filename: tokenize(files[filename])
    for filename in files
}
file_idfs = compute_idfs(file_words)

# Prompt user for query
query = set(tokenize('When was Python 3.0 released?'))

# Determine top file matches according to TF-IDF
filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

# Extract sentences from top files
sentences = dict()
for filename in filenames:
    ### I had to change this part of the code because I did not read the load_files instructinos ###
    ### correctly, my apologies. ###
    for lines in files[filename]:
        for passage in lines.split("\n"):
    ### Above code is changed, my load_files function returns a list instead of a string ###
    ### so the split("\n") method didn't work on files[filename] ###
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

# Compute IDF values across sentences
idfs = compute_idfs(sentences)

# Determine top sentence matches
# matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)

# print(matches)




                    ###  What are the types of supervised learning? ###
                    ###     Works

                    ###  When was Python 3.0 released?
                    ###     Kindof works!!
                    ### output: Python 3.0, released in 2008, was a major revision of the language that is not completely backward-compatible, and much Python 2 code does not run unmodified on Python 3. ###

                    ###  How do neurons connect in a neural network?
                    ###     Does not work!!!
                    ### output: A fourth approach is harder to intuitively understand, but is inspired by how the brain's machinery works: the artificial neural network approach uses artificial "neurons" that can learn by comparing itself to the desired output and altering the strengths of the connections between its internal neurons to "reinforce" connections that seemed to be useful. ###


rank = {}
unique_v = {}

for key, value in sentences.items():

    times = 0


    for word in query:

        if word in value:

            # print(key,'\n', f'!!COUNT: {value.count(word)}', '\n', value,'\n', word)
            try:

                if rank[key]:

                    rank[key] += idfs[word]

            except KeyError:

                rank[key] = idfs[word]

for k, v in rank.items():

    try:
        if unique_v[v]:
            unique_v[v] += 1
    except KeyError:
        unique_v[v] = 1

print("MAX!!", max(unique_v))

for k, v in rank.items():
    if v == max(unique_v):
        print("THIS IS K!!", k)
        times = 0
        for i in query:
            # print(i)
            times += k.count(i)
        rank[k] = times / len(k)


print(len(rank), unique_v)
#             times += 1
#     rank[key] = idfs[word] * (times / len(value))
# print(rank)

rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}

print(list(rank.keys())[:1])