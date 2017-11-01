#!/usr/bin/python

from decision_tree import *
from dataset_functions import * 

raw_examples = read_dataset ("../../project/DatasetRetry/data-splits/data.train", 16)
training_set, feature_descriptions, feature_values = make_discrete_features (raw_examples, "feature_desc.txt", debug = 0)
cv_set = gen_cv_set (training_set, 10)
# for i in range (10) : print cv_set [i]
D = decision_tree(attr_names = feature_descriptions, attr_table = feature_values)
# D.create_tree(training_examples = training_set)
D.max_depth = 2
print D.cross_validate (cv_set)
D.max_depth = 10
print D.cross_validate (cv_set)
