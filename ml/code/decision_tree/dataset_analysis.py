#!/usr/bin/python

from dataset_functions import * 
import matplotlib.pyplot as plt

num_features = 16 # excluding label
raw_examples = read_dataset ("../../project/DatasetRetry/data-splits/data.train", num_features)
training_set, feature_descriptions, feature_values = make_discrete_features (raw_examples, "feature_desc.txt", "fe_all_enabled.txt", debug = 0)

def find_avg (l) :
    avg = sum(l)/float(len(l))
    variance = sum([(el-avg)**2 for el in l])/float(len(l))
    sigma = variance**0.5
    return (round(avg,2), round(sigma,2))

def find_range (examples, feature_descriptions) :
    len_ex = len(examples[0])
    min_ = [ float("inf") for i in range (len_ex)]
    max_ = [-float("inf") for i in range (len_ex)]
    
    for e in examples :
        for i in range (len_ex) :
            if e[i] < min_[i] :
                min_[i] = e[i]
            if e[i] > max_[i] :
                max_[i] = e[i]

    for desc, min_val, max_val in zip (feature_descriptions, min_, max_) :
        print desc, ": ", min_val, ", ", max_val

def separate (examples, ind) :
    l = []
    l_bot = []
    l_nobot = []
    for e in examples :
        l.append(e[ind])
        if e[-1] == 1 :
            l_nobot.append (e[ind])
        else :
            l_bot.append (e[ind])

    return (l, l_bot, l_nobot)

def find_avg_and_sd (examples, feature_descriptions, num_features) :
    for ind in range (num_features) :
        l, l_bot, l_nobot = separate (examples, ind)
        print "w.r.t feature", feature_descriptions[ind]
        print "overall average, sd= ", find_avg(l)
        print "average, sd for bots = ", find_avg(l_bot)
        print "average, sd for non bots = ", find_avg(l_nobot)
        print ""

def plot_distribution (examples, ind, feature_descriptions) :
    l, l_bot, l_nobot = separate (examples, ind)

    if ind == 15 : # delta_fol
        hrange = (-1,1)
    elif ind == 6 : # num_following
        hrange = (0,1000)
    elif ind == 7 : # num_followers
        hrange = (0,2000)
    elif ind == 2 : # days
        hrange = (0,50)
    elif ind == 11 : # links_in_tweet
        hrange = (0,2)
    elif ind == 12 : # ulinks_in_tweet
        hrange = (0,2)
    elif ind == 13 : # uname_in_tweet
        hrange = (0,1)
    elif ind == 14 : # uname_in_tweet
        hrange = (0,1)
    elif ind == 0 : # scr_nam_len
        hrange = (0,30)
    elif ind == 1 : # desc_len
        hrange = (0,100)
    else :
        hrange = None
    
    plt.subplots (2,2)
    
    plt.subplot(2,2,1)
    plt.hist(l,bins=50,range=hrange)
    plt.title(feature_descriptions[ind]+" combined")
    
    plt.subplot(2,2,3)
    plt.hist(l_bot,bins=50,range=hrange)
    plt.title("bots")
    
    plt.subplot(2,2,4)
    plt.hist(l_nobot,bins=50,range=hrange)
    plt.title("not bots")
    
    plt.show()

find_range (raw_examples, feature_descriptions)
find_avg_and_sd (raw_examples, feature_descriptions, num_features)
plot_distribution (raw_examples, 2, feature_descriptions)
