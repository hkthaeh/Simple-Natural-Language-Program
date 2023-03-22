from questions import tokenize, compute_idfs, load_files
from nltk.tokenize import word_tokenize



files = load_files('corpus')


for filename in files:
    # print(files[filename])
    a = files[filename]
    break

# file_words = {
#     filename: tokenize(files[filename])
#     for filename in files
# }

# print(len(a))
for i in range(4):
    print(a[i])

# print(word_tokenize(a))

# for i in a:
#     print(i)

        # BECAUSE load_files returns a list and query inputs a string!!