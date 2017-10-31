#!/usr/bin/python

from decision_tree import *

def read_dataset (file_name, num_features) : # num_features excluding the label
    f = open (file_name)
    lines = f.readlines ()
    examples = []
    for line in lines :
        words = line.split()
        ex = [0 for _ in range (num_features+1)]
        ex[-1] = int (words[0])
        for word in words[1:] :
            ind, val = word.split(":")
            ex[int(ind)-1] = float(val)
        examples.append(ex)

    return examples

def make_discrete_features (examples, feat_desc_file, debug = 0) :
    # takes in a list of examples that are not discretized
    # reads the features descrption file that tells how to discretize
    # returns discreteized examples, string description of features, string description of each range


    ## Parse the feature description file and populate the feature_descriptions, features_values and feature_ranges lists.
    f = open (feat_desc_file)
    lines = f.readlines ()

    ex_len = len(examples[0])
    feature_descriptions = [0 for _ in range(ex_len)]
    feature_ranges       = [0 for _ in range(ex_len)]
    feature_values       = [0 for _ in range(ex_len)]

    for line in lines :
        if line[0] == '#' :
            pass
        elif line[0] == '@' :
            pass
        elif line[0] == 'i' : # id
            words = line[:-1].split()
            ind = int(words[1]) - 1
        elif line[0] == 'd' : # desc
            words = line[:-1].split()
            feature_descriptions[ind] = words[1]
        elif line[0] == 'r' : # range
            cur_f_ranges = []
            cur_f_values = []

            words = line[:-1].split()
            for w in words[1:] :
                if w == ';' :
                    continue

                # split a1,b1,s1 along the ','
                l = w.split(',')
                bounds = []
                values = []
                if l[0] == 'x' :
                    bounds.append (-float("inf"))
                else :
                    bounds.append (float(l[0]))

                if l[1] == 'x':
                    bounds.append (float("inf"))
                else :
                    bounds.append (float(l[1]))

                cur_f_ranges.append (bounds)
                cur_f_values.append (l[2])

            feature_ranges[ind] = cur_f_ranges
            feature_values[ind] = cur_f_values

    if debug :
        print "feature descriptions"
        print feature_descriptions
        print "feature ranges"
        print feature_ranges
        print "feature values"
        print feature_values

    if len(examples[0]) != len(feature_ranges) :
        print "Error: number of features in each example does not match the number of features in feature description file"
        sys.exit(0)

    disc_examples = [] # discretized examples
    ## Read each example. Within each example, find in which range the value lies.
    for ex in examples :
        disc_ex = []
        for value, cur_f_ranges in zip(ex, feature_ranges) :
            for i, range_ in enumerate (cur_f_ranges) :
                if range_[0] <= value and value < range_[1] :
                    disc_ex.append (i)
                    break
        disc_examples.append (disc_ex)

    for ex in disc_examples :
        s = ""
        for i, val in enumerate(ex) :
            s+=feature_values[i][val]+", "
        print s

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

examples = read_dataset ("../../project/DatasetRetry/data-splits/data.train", 16)
for ex in examples[0:10] : print ex
make_discrete_features (examples[0:10], "feature_desc.txt", debug = 1)
