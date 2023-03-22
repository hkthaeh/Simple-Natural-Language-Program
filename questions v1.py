import nltk
import sys
import os
import re

# import the word tokenizer from the library nltk
# https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.punkt.PunktLanguageVars.word_tokenize
from nltk.tokenize import word_tokenize
# in order to use 'stopwords' from nltk, we need to download it
# input the following commands into python console
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# if there is a CERTIFICATE_VERIFY_FAILED error, like I did
# I used the following code from:
# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
# and used the top answer's code to download 'stopword' and 'punkt'
from nltk.corpus import stopwords
# import log from the math library
# https://docs.python.org/3/library/math.html
from math import log
# import the punctuations from the string library
# https://docs.python.org/3/library/string.html
from string import punctuation

FILE_MATCHES = 2
SENTENCE_MATCHES = 2


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for lines in files[filename]:
            for passage in lines.split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # dictionary containing all the file's name and their corresponding content
    result = {}

    # loop through each file in the folder
    for i in os.listdir(directory):
        # checks if the file is a .txt file or not
        if i.endswith('.txt'):
            # platform independent pathway for each files in the folder
            path = os.path.join(directory, str(i))
            # Opening each file using "with" so that it'll close itself afterwards
            with open(path, "r") as file:
                # read everything inside the file
                lines = file.readlines()
                # add it to the result dictionary with the file name as key and content of the file as value
                result[i] = lines
    # returns the dictionary with all the files' content in its value
    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.
    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    # List for all the words inside each document
    result = []

    # check if the input is a string or not, since the load_files function returns a list
    # so then if we want to just use the tokenize function by itself to prompt user for a "query"
    # the tokenize funcion will work properly
    if isinstance(document, str):
        # makes everything lower case
        words_tok = word_tokenize(document.lower())
        # iterates through each word in string
        for word_tok in words_tok:
            # Check if the word is a stopword
            if word_tok not in stopwords.words("english"):
                # check if its a punctuation
                if word_tok not in punctuation:
                    # add it to the result list
                    result.append(word_tok)
        return result


    # Iterates through the document line by line
    for i in document:

        # tokenize the lines
        tok = word_tokenize(i)

        # Iterates through the tokenize list
        for token in tok:
            # Check if the word is a stopword
            if token.lower() not in stopwords.words("english"):
                # check if its a punctuation
                if token not in punctuation:
                    # add it to the result list
                    result.append(token.lower())

    # Removes all 'https' from the result list since its from the beginning of a website
    for i in range(result.count('https')):
        result.remove('https')

    # returns a list of all of the words in the document
    return result


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Dictionary for all return values
    result = {}
    # number of total documents
    nums = len(documents)

    # loops through each document's dictionary values from the tokenize function
    for doc in documents:
        for word in documents[doc]:
            if word in result:
                result[word] += 1
            else:
                result[word] = 1

    # loops through the result dictionary and transform the value into IDF a IDF value
    # using the formula ( total documents / number of documents containing (word) )
    for key, value in result.items():
        idf = log(nums / value)
        result[key] = idf

    return result



def top_files(query, files, idfs, n):
    """
    Given a
        `query` (a set of words),
        `files` (a dictionary mapping names of files to a list of their words),
    and `idfs` (a dictionary mapping words to their IDF values),
    return a list of the filenames of the `n` top
    files that match the query,
     ranked according to tf-idf.
    """


    # dictionary to capture all the files that contain words in query
    rank = {}

    # loop through each word in the user inputed query
    for word in query:
        # goes through each key and value in the files dictionary
        for key, value in files.items():
            #check to see if the word in query is in the value of the dictionary
            if word in value:
                # I used try because when there is no rank[key], a KeyError is outputed
                # so in order to capture this error, I used try/except
                try:
                    # checks to see if the specific key already exist in the rank dictionary
                    if rank[key]:
                        # if so, we add upon its value
                        rank[key] += value.count(word) * idfs[word]
                        # and then break out of the files dictionary
                        break
                # if we encounter a key that is not already in the rank dictionary
                except KeyError:
                    # initiate the entry of the key into the rank dictionary
                    rank[key] = value.count(word) * idfs[word]

    # sort the dictionary
    rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
    # returns the list of the keys in the rank dictionary, sliced by n
    return list(rank.keys())[:n]



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words),
    `sentences` (a dictionary mapping sentences to a list of their words),
    and `idfs` (a dictionary mapping words to their IDF values),
    return a list of the `n` top sentences that match the query,
    ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # set up a dictionary for determining the highest IDF value for any
    # particular sentence
    rank = {}
    # initiate a dictionary for collecting the unique values ( or IDF values ) from
    # the 'sentences' dictionary and counting how many times each of those IDF values
    # appear
    unique_v = {}

    # loops through the 'sentences' dictionary and find out if it contains any word
    # from the inputed question 'query'
    for key, value in sentences.items():
        for word in query:
            if word in value:
                # if we find a word that matches, we'll associate that particular
                # key ( or sentence ) to a IDF value
                try:
                    if rank[key]:
                        rank[key] += idfs[word]
                except KeyError:
                    rank[key] = idfs[word]

    # now we loop through the dictionary with all the sentences that contains at least
    # one of the query's words and IDF values to find and count the unique IDF value(s)
    for k, v in rank.items():
        try:
            if unique_v[v]:
                unique_v[v] += 1
        except KeyError:
            unique_v[v] = 1

    # next we check if there is only one unique max IDF value in the unique IDF values dictionary
    # this means that there is only one sentence that best match the inputed question ( query )
    if unique_v[max(unique_v)] == 1:
        # we'll sorted the 'rank' dictionary, in reverse order, with all the keys and values as
        # sentences and its IDF values
        rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1], reverse=True)}
        # and return the first sentence from the list of sentences in the 'rank' dictionary
        # because there is only one
        return list(rank.keys())[:1]

    # otherwise, if the max unique IDF value appears more than 1 time

    # set up a dictionary to collect the max unqiue IDF value's sentences
    # in relation with their density value
    density_sentences = {}

    # we go thorugh every single sentence and their IDF values in the 'rank' dictioanry
    for k, v in rank.items():
        # and see if a particular IDF value matches with the max IDF value in 'unique_v' dictionary
        if v == max(unique_v):
            # initiate a variable to count how many times a word in 'query' appears in
            # this particular sentence
            times = 0
            for i in query:
                times += k.count(i)
            # then calclate its word density and add it to the 'density_sentences' dictionary
            density = times / len(k)
            density_sentences[k] = density
    # we'll sort through this dictionary with its biggest value coming first
    density_sentences = {k: v for k, v in sorted(density_sentences.items(), key=lambda item: item[1], reverse=True)}
    # and return the 'SENTENCE_MATCHES' amount of the best sentences that can answer the inputed 'query' question
    return list(density_sentences.keys())[:n]



if __name__ == "__main__":
    main()