__author__ = 'anthonylim'

# Anthony Lim
# alim4@ucsc.edu
#
# CMPS 5P, Spring 2014
# Assignment 7
#

import re

def main():
    config_list = load_config()


def load_config():
    """
    loads a config file used to read in books
    :return: list of config strings
    """
    config = raw_input("Choose config file to load (filetype: .txt): ")
    with open("{0}.txt".format(config), 'r') as f:
        read_data = f.readlines()

    # Remove \n from string element
    for idx, item in enumerate(read_data):
        read_data[idx] = item.rstrip()

    return read_data

def process_document(user_input):
    word_dict = dict()

    with open("{0}.txt".format(user_input), 'r') as f:
        read_data = f.read()

    # Split the book into individual words
    book_str = read_data.split()

    # Strip elements of non-alpha characters
    # Uses regular expressions
    for idx, item in enumerate(book_str):
        book_str[idx] = re.sub(r'\W+', '', item).lower()

    # Increment the word counts
    for i in range(len(book_str)):
        if book_str[i] not in word_dict.keys():
            word_dict[book_str[i]] = 1
        else:
            word_dict[book_str[i]] += 1

    return word_dict

main()
