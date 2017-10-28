#!/usr/bin/python

from decision_tree import *

def parse_line (line) :
    words = line.split()
    # example[0] = 0,
    # example[1-16] are the features
    # example[17] is the label
    example = [0 for i in range (18)]
    for word in words [1:] :
        pair = word.split(":")
        example[int(pair[0])] = float(pair[1])
    example[17] = int (words[0])
    return example

def gen_training_examples (file_name) : #, attr_table, attr_en) :

    # read the training data file
    f = open (file_name)
    g = open (file_name)
    lines = g.readlines()
    training_examples = []

    for line in f :
        s = line[:-1]
        training_example = []

        raw_example = parse_line (line)
        if attr_en.len_screen_name :
            len_screen_name = int (raw_example[1])
        
        print raw_example

def main () :
    gen_training_examples ("../../project/DatasetRetry/data-splits/data.train")

main ()
