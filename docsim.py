__author__ = 'anthonylim'

# Anthony Lim
# alim4@ucsc.edu
#
# CMPS 5P, Spring 2014
# Assignment 7
#

from collections import defaultdict
from collections import Counter
import re
import math
import sys

def main():
    parameters = sys.argv[1:]

    while True:
        input_loop(parameters)

def input_loop(params):
    config_list = load_config(params[0])
    dict_list = []
    user_dict_list = []

    user_input = raw_input("What is your search?: ").split(" ")

    if len(user_input) <= 1:
        print "EXITING..."
        sys.exit(0)
    else:
        user_dict_list.append(process_document(user_input))

    for fname in config_list:
        dict_list.append(process_document(fname))

    IDF_vectors = compute_IDF(dict_list)
    user_IDF = compute_IDF(user_dict_list)

    # print user_dict_list[0]
    # print IDF_vectors
    # print user_IDF

    sim_list = []

    print "Your document results are..."
    for idx, d in enumerate(dict_list):
        sim_list.append((config_list[idx], similarity(d, user_dict_list[0], IDF_vectors[idx], user_IDF[0])))

    # Sort the tuple list
    sorted_sim_list = sorted(sim_list, key=lambda tup: tup[1], reverse=True)

    for i in range(20):
        if len(sorted_sim_list) != i:
            print "{0:4}: {1:20} {2}".format(i+1, sorted_sim_list[i][0], sorted_sim_list[i][1])
        else:
            break


def load_config(config):
    """
    loads a config file used to read in books
    :return: list of config strings
    """
    #config = raw_input("Choose config file to load (filetype: .txt): ")
    #with open("{0}".format(config), 'r') as f:
    with open(config, 'r') as f:
        read_data = f.readlines()

    # Remove \n from string element
    for idx, item in enumerate(read_data):
        read_data[idx] = item.rstrip()

    return read_data

def process_document(user_input):
    word_dict = defaultdict(int)

    # Differentiate between file and user input
    if type(user_input) == str:
        with open("test_files/{0}".format(user_input), 'r') as f:
            read_data = f.read()
    else:
        read_data = ' '.join(user_input)

    # Split the book into individual words
    book_str = read_data.split()

    # Strip elements of non-alpha characters
    # Uses regular expressions
    for idx, item in enumerate(book_str):
        book_str[idx] = re.sub(r'\W+', '', item).lower()

    # Increment the word counts
    for i in range(len(book_str)):
        word_dict[book_str[i]] += 1

    return word_dict

def compute_IDF(dict_list):
    """
    Compute the IDF values
    :param dict_list: dictionaries of corpus files
    :return: IDF_vectors containing vector values per document
    """
    IDF_dict_list = []
    IDF_vectors = []
    frequency_dict = defaultdict(int)

    corpus_size = len(dict_list)

    # Sum the dictionaries together
    dictkeys = sum(
        (Counter(dict(x)) for x in dict_list),
        Counter()
    )

    # Get number of times the word appears
    for ele in dict_list:
        for word in dictkeys.keys():
            if word in ele.keys():
                frequency_dict[word] += 1

    # Calculate the IDF value
    for ele in dict_list:
        IDF_dict = defaultdict(int)
        for word in dictkeys.keys():
            if word in ele.keys():
                # IDF = freq * ln(N/(n+1))
                IDF_dict[word] = float(ele[word]) * math.log(corpus_size / frequency_dict[word] + 1.0)
        IDF_dict_list.append(IDF_dict)

    # Calculate the TF-IDF vectors
    for i in IDF_dict_list:
        vector = 0.0
        for j in i.values():
            vector += j ** 2
        vector = math.sqrt(vector)
        IDF_vectors.append(vector)

    return IDF_vectors

def similarity(d1, d2, length_d1, length_d2):
    vec_list = []
    for i in d1:
        if i in d2:
            vec_list.append(d1[i] * d2[i])

    vec_sum = 0
    for vec in vec_list:
        vec_sum += vec

    sim = vec_sum / (length_d1 * length_d2)

    return sim


main()
