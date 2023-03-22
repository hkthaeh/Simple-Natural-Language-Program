import nltk
import sys
import os

from questions import load_files
import string
import re
from questions import tokenize
from questions import top_files

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')


from questions import compute_idfs

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from math import log


# file = open("corpus/", "r")
# print(file)

f = os.listdir("corpus")
result = {}

for i in f:
    dir = os.path.join("corpus", str(i))
    with open(dir, "r") as file:
        lines = file.readlines()
        # print(lines)
        result[i] = lines
    # break

# print(result)


# file_words = {
#         filename: nltk.tokenize(f[filename])
#         for filename in f
#     }

# print(file_words)

# print(nltk.tokenize(f))

# print(load_files("corpus"))

# print(result.values())

# a = result.values()


# a.replace(string.punctuation, '')
for k, v in result.items():
    # print(v)
    b = v
# b = b.remove(string.punctuation)
# print(b)

times = 0
wordlist = []
for i in b:
    if times < 10:
        # print("~~THIS IS i:~~",i)
        i = i.lower()
        words = re.findall('[a-z]+', i)
        # print("WORDS!!", words)
        for word in words:
            # print("THE LOOP:", word)
            if word not in stopwords.words("english"):
                wordlist.append(word)
        times += 1

    else:
        break
# print("RESULTS!", wordlist)

# dic = {}
# for i in wordlist:
#     if i in dic:
#         dic[i] += 1
#     else:
#         dic[i] = 1
# # print(dic)

file_words = {
        filename: wordlist
        for filename in result
    }
# print(file_words)

temp = []
temp2 = []
for test in result:
    # temp = []
    for j in result[test]:
        # print(j)

        # NO NLTK
        words = re.findall('[a-z]+', j)

        # YES NLTK
        test1 = word_tokenize(j)


        # print(words)
        # asd = words.lower()

        # NO NLTK
        for i in words:
            if i.lower() not in stopwords.words("english"):
                temp.append(i.lower())

        # YES NLTK
        for j in test1:
            if j.lower() not in stopwords.words("english"):
                if j not in string.punctuation:
                    j = re.sub('[0-9]+', '', j)
                    j = re.sub('^[a-zA-Z]$', '', j)
                    j = re.sub('^[a-z][a-z]$', '', j)
                    # if len(j) != 2 or len(k) !=1:
                    if j.isalpha():
                        temp2.append(j)
    # print("NO NLTK", "\n", temp)
    # print("YES NLTK","\n", temp2)
    # for k in temp2:
    #     if len(k) == 2 or len(k) == 1:
    #         print(k)
        # elif len(k) == 1:
        #     temp2.remove(k)
    # for l in temp2:
    #     if len(l) == 1:
    #         print(l)
    # print("YES NLTK, NO single/doubles", "\n", temp2)

    # break

# print(temp2)
# dic = {}
# for i in temp2:
#     if i in dic:
#         dic[i] += 1
#     else:
#         dic[i] = 1
# print(dic)

# th, th, de, de, la, ϕ ,De, De, Pr, Pr, th, pp, nd, ed, pp, pp, de

for i in range(temp2.count('https')):
    temp2.remove('https')
# print('https' in temp2)

result_idfs = {}

for i in temp2:
    if i in result_idfs:
        result_idfs[i] += 1
    result_idfs[i] = 1

# print(result_idfs)

# for key, value in result_idfs.items():
#     idf = log(num)

result_idf = {}

for key, value in result_idfs.items():
    idf = log(len(temp2) / value)
    result_idf[key] = idf

# print(result_idf)

question = 'What are the types of supervised learning?'
query = set(tokenize('What are the types of supervised learning?'))

# print(tokenize(question))

# print(result_idf['Curlie'])

# for k in tokenize(question):
    # print(result_idf[k])

# print(file_words['probability.txt'].count('python'))



# result = []

# rank = {}

# for word in set(tokenize(question)):
#     # print(word)

#     for key, value in file_words.items():

#         if word in value:
#             print("yes")

            # if rank[key]:

            #     rank[key] += files[key].count(word) * result_idfs(word)

            # else:

            #     rank[key] = files[key].count(word) * result_idfs[word]



file_idfs = compute_idfs(file_words)

filenames = top_files(question, file_words, file_idfs, n=FILE_MATCHES)

# print(filename)





sentences = dict()
for filename in filenames:
    # print(filename)
    for i in result[filename]:

        for passage in i.split("\n"):

            # this gives me a error saying that a list cannot be split..
            # where did the list come from?..?..?

            # ok, i had to loop through each value in the files dictionary
            # because i returned it as a list in load_files function

            # print(passage)
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

# print(sentences)

idfs = compute_idfs(sentences)


rank = {}

for word in query:

    for key, value in sentences.items():

        if word in value:

            print(key,'\n', f'!!COUNT: {value.count(word)}', '\n', value,'\n', word)