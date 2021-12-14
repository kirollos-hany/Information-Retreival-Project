# importing libraries
import numpy as np
import os
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from natsort import natsorted
import string


def read_file(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    return data


def remove_header_footer(final_string):
    new_final_string = ""
    tokens = final_string.split('\n\n')

    # Remove tokens[0] and tokens[-1]
    for token in tokens[1:-1]:
        new_final_string += token + " "
    return new_final_string


tokenized_documents = {}  # From Malak Task

# Replace by your path
projectPath = "C:\\Users\\FFaye\\OneDrive\\Desktop\\DS\IR\\Information-Retreival-Project"
# In this example, we create the positional index for only 1 folder.
folder_names = ["Docs"]  # you can add more to the array if you want

# Initialize the stemmer.
stemmer = PorterStemmer()

# Initialize the file no.
fileno = 0

# Initialize the dictionary.
pos_index = {}

# Initialize the file mapping (fileno -> file name).
file_map = {}

for folder_name in folder_names:

    # Open files.
    file_names = natsorted(os.listdir(projectPath + "/" + folder_name))

    # For every file.
    for file_name in file_names:

        # Read file contents.
        stuff = read_file(projectPath + "/" + folder_name + "/" + file_name)

        # This is the list of words in order of the text.
        # We need to preserve the order because we require positions.
        # 'preprocessing' function does some basic punctuation removal,
        # stop-word removal etc.
        final_token_list = tokenized_documents

        # For position and term in the tokens.
        for pos, term in enumerate(final_token_list):

            # First stem the term.
            term = stemmer.stem(term)

            # If term already exists in the positional index dictionary.
            if term in pos_index:

                # Increment total freq by 1.
                pos_index[term][0] = pos_index[term][0] + 1

                # Check if the term has existed in that DocID before.
                if fileno in pos_index[term][1]:
                    pos_index[term][1][fileno].append(pos)

                else:
                    pos_index[term][1][fileno] = [pos]

            # If term does not exist in the positional index dictionary
            # (first encounter).
            else:

                # Initialize the list.
                pos_index[term] = []
                # The total frequency is 1.
                pos_index[term].append(1)
                # The postings list is initially empty.
                pos_index[term].append({})
                # Add doc ID to postings list.
                pos_index[term][1][fileno] = [pos]

        # Map the file no. to the file name.
        file_map[fileno] = projectPath + "/" + folder_name + "/" + file_name

        # Increment the file no. counter for document ID mapping
        fileno += 1

# Sample positional index to test the code.
print("Positional Index")
print(pos_index)
