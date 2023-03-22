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

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


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
        for passage in files[filename].split("\n"):
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
                lines = file.read()
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

    # check if the input is a string or not
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

    # if the input is a list instead of a string ( like what I had before )
    # the program will exit and gives a error
    sys.exit("tokenize was not given a string")


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
    for doc in documents.values():
        for word in doc:
            if word in result:
                result[word] += 1
            else:
                result[word] = 1

    # tracks the idfs score
    score = {}

    # loops through the result dictionary and transform the value into IDF a IDF value
    # using the formula ( total documents / number of documents containing (word) )
    for key, value in result.items():
        idf = log(nums / value)
        score[key] = idf

    return score



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
                # initiate the entry of the key into the rank dictionary
                try:
                    if rank[key]:
                        rank[key] += value.count(word) * idfs[word]
                except KeyError:
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


    # sort the rank dictionary in descending order
    rank = {k: v for k, v in sorted(rank.items(), key=lambda item: item[1], reverse=True)}

    # initiate a variable to capture the highest idfs value
    max_idfs = list(rank.values())[0]

    # check to see if there is only one sentence with the highest idfs value
    if list(rank.values()).count(max_idfs) == 1:
        # if so, we return that sentence, which will be the closest answer to our query question
        return list(rank.keys())[:n]

    # otherwise, if there are more than one highest idfs value,
    # we'll calculate the density of the sentences with the highest idfs value
    density_sentences = {}
    max_idfs_count = list(rank.values()).count(max_idfs)
    traverse = 0

    # loop through the whole rank dictionary until we hit when 'traverse' is equal to 'max_idfs_count'
    # because the 'rank' dictionary is sorted in descending order and we only care about the sentences
    # with the highest idfs value
    for phrase, _ in rank.items():
        # tokenize the sentence to capture the important words
        p_t = tokenize(phrase)
        times = 0
        # loop through each word in the inputed 'query' question and find if each word
        # is in the tokenized phrase
        for i in query:
            if i in p_t:
                times += p_t.count(i)
        # calculate the sentence density
        density = times / len(phrase)
        density_sentences[phrase] = density
        traverse += 1
        # since we only care about the sentences with the hihgest idfs value, we'll stop this loop
        # when we go through all of the aforementioned sentences to save time
        if traverse == max_idfs_count:
            break

    # sort the density sentences in descending order
    density_sentences = {k: v for k, v in sorted(density_sentences.items(), key=lambda item: item[1], reverse=True)}

    # return the best answer to the inputed 'query' question
    return list(density_sentences.keys())[:n]


if __name__ == "__main__":
    main()