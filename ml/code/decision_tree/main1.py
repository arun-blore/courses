#!/usr/bin/python

from decision_tree import *
from dataset_functions import * 

raw_examples = read_dataset ("../../project/DatasetRetry/data-splits/data.train", 16)
training_set, feature_descriptions, feature_values = make_discrete_features (raw_examples, "feature_desc.txt", "fe_current.txt", debug = 0)
cv_set = gen_cv_set (training_set, 10)

D = decision_tree(attr_names = feature_descriptions, attr_table = feature_values)

def find_best_depth () :
    # cross validate and find the best depth
    for max_depth in range (5,13) :
        D.max_depth = max_depth
        print "max_depth = ", max_depth, "cross validation accuracy = ", D.cross_validate (cv_set)

def train_best_depth (best_max_depth) :
    # create and train the tree with the best depth
    D.max_depth = best_max_depth
    D.create_tree (training_set)

    # check test set accuracy
    raw_examples = read_dataset ("../../project/DatasetRetry/data-splits/data.test", 16)
    test_set, feature_descriptions, feature_values = make_discrete_features (raw_examples, "feature_desc.txt", "fe_current.txt", debug = 0)
    print "test set accuracy = ", D.check_classify_acc (test_set)
 
def final () :
    raw_examples = read_dataset ("../../project/DatasetRetry/data-splits/data.eval.anon", 16)
    test_set, feature_descriptions, feature_values = make_discrete_features (raw_examples, "feature_desc.txt", "fe_current.txt", debug = 0)
    res = D.classify (test_set)
    # print "length of result list = ", len(res)
    
    f = open ("../../project/DatasetRetry/data-splits/data.eval.id")
    ids = f.readlines ()
    f.close ()
    # print "length of ids = ", len(ids)
    s = "Id,Prediction"
    for id_,res_ in zip(ids,res) :
        s+="\n"+id_[:-1]+","+str(res_)
    f = open ("./data.eval.pred", 'w')
    print >> f, s
    f.close ()

# find_best_depth ()
train_best_depth (7)
final ()
