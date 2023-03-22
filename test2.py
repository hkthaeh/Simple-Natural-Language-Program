from questions import tokenize, compute_idfs, load_files

q = 'What are the types of supervised learning?'

test1 = 'This is a test sentence. Oh what should i do if this test fails?'

test2 = ['python', 'apress', 'isbn', 'summerfield', 'mark', 'programming', 'python', 'professional', 'isbn', 'external', 'links', 'official', 'website', 'python', 'programming', 'language', 'curlie']

test3 = ' '.join(test2)
            # load file works
# print(load_files('corpus'))

files = load_files('corpus')



            # tokenize works... I think?....

# for filename in files:
#     print(tokenize(files[filename]))
    # print(files[filename])

            # no output for q .. . .
            # why is there no output?/..?..

                # what am i doing with load files..

                    # I am grabing all the words in each text file

                # so then tokenize will match each work in the user entered question

                    #



            # q:        failed
            # test1:    failed
            # test2:    failed
            # test3:    failed

# print(tokenize(q))

print(tokenize(test3))












            # compuete_idfs works!?!?!

                # why does the next step of the code works and not tokenize ?!?!?!



# file_words = {
#         filename: tokenize(files[filename])
#         for filename in files
#     }
# file_idfs = compute_idfs(file_words)

# print(file_idfs)