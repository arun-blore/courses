#!/usr/bin/python

import math, sys
from node import *

debug = 0
debug1 = 0
use_majority_error = 0

def calc_entropy (data_dist) :
   #remember that the data_dist could be list of 0s. Return 0 in that case
   data_size = sum(data_dist)

   if data_size == 0 :
      return 0

   if use_majority_error :
      maj_err = 1 - max(data_dist)/(float(data_size))
      return maj_err
   else :
      entropy = 0
      for data in data_dist :
         fraction = data/float(data_size)
         if fraction != 0 :
            entropy += -1 * (fraction) * math.log(fraction, 2)
      return entropy

def classify (instance, root) :
   if root.leaf == 1 :
      # print "reached leaf, label_id = ", root.label_id
      return root.label_id
   else :
      # print "attr_id = ", root.attr_id
      return classify (instance, root.nbrs[instance[root.attr_id]])

class decision_tree :
   def __init__ (self, attr_names, attr_table, training_examples, max_depth = float('inf')) :
      self.attr_table = attr_table # each element attr_table[i] of this list is a list - which contains all values that attribute i can take. The last attribute is actually the output. So the last list in attr_table is a list of all value that the output can take.
      self.attr_names = attr_names
      self.training_examples = training_examples # each element of this list is a training example - which is represented as a list, a list of all features and the last element is the output label
      self.max_depth = max_depth # max allowed depth of the tree
      self.depth = None # Actual depth of the tree (will be set when ID3 is executed)

   def create_tree (self) :
      examples = [i for i in range(len(self.training_examples))]
      attributes = [i for i in range(len(self.attr_table))]
      return self.id3 (examples, attributes[:-1], 0)

   def check_same_label (self, examples) :
      #print "check same label start"
      #print self.training_examples[examples[0]]
      label_id = self.training_examples[examples[0]][-1]
      for e in examples[1:] :
         #print self.training_examples[e]
         if self.training_examples[e][-1] != label_id :
            return 0
      #print "check same label end"

      return 1

   def find_max_label (self, examples) :
      label_id_count = [0 for i in range (len(self.attr_table[-1]))]

      for e in examples :
         label_id = self.training_examples[e][-1]
         label_id_count[label_id]+=1

      return label_id_count.index(max(label_id_count))

   def print_examples (self, ex_ind) : # ex is a list of indices of examples in self.training_examples
      f = open("./Updated_Dataset/updated_train.txt")
      lines = f.readlines()
      for e in ex_ind :
         print lines[e][:-1]
      print ""
      # for e in ex_ind :
      #    print e, [self.attr_table[i][self.training_examples[e][i]] for i in range(len(self.training_examples[e]))]

   def find_best_attr (self, examples, attributes) :
      a_best = -1
      min_entropy = float('inf')
      for a in attributes :
         if (debug) : print "attribute = ", self.attr_names[a]
         # compute the information gain/entropy if the examples are partitioned according to attribute a
         # create a bucket for each value of attribute a
            # what does each bucket contain? 
         # go through each example in examples, look at attribute a of that example, put it into the appropriate bucket

         # forget buckets.. 
         a_breakup = [] # list of size = number of values that attribute a can take. Element i of the list corresponds to a taking on value attr_table[a][i]. Each element is a list of size 2. [0] contains number of examples for which attr a = value i. [1] contains purity (entropy) of examples for which attr a = value i.
         for value_id in range(len(self.attr_table[a])) : # value is
            if (debug) : print "value = ", self.attr_table[a][value_id]
            # we are looking for the distribution of output labels in those examples in examples for which attribute a == value
            # go through every example in examples and compare the attribute a of example with value
            # out_dist is a dictionary, each value that output can take on is a key. create an empty distribution
            # out_dist = {}
            # for out_label in self.attr_table[-1] :
            #    out_dist[out_label] = 0

            out_dist = [0 for i in range(len(self.attr_table[-1]))]
            count = 0 # number of examples for which attr a = value
            for e in examples :
               if self.training_examples[e][a] == value_id :
                  if (debug) : print "example ", self.training_examples[e], " matches", [self.attr_table[i][self.training_examples[e][i]] for i in range(len(self.training_examples[e]))]
                  # increment count
                  count+=1
                  # what is this example's output label?
                  # increment the count corresponding to the label
                  out_dist[self.training_examples[e][-1]]+=1

            if (debug) : print "number of examples with attribute ", self.attr_names[a], " = ", self.attr_table[a][value_id], " is ", count
            if (debug) : print "distribution for ", self.attr_names[a], " = ", self.attr_table[a][value_id], " is ", out_dist
            # compute entropy for distribution
            ent = calc_entropy (out_dist)
            if (debug): print "entropy for this distribution is ", ent
            a_breakup.append([count, ent])
         if (debug) : print "entropies when partition w.r.t this attribute", a_breakup

         # Compute total entropy using a_breakup
         tot_entropy = 0
         example_count = len(examples)
         for dist_size, sub_entropy in a_breakup :
            tot_entropy += (dist_size/float(example_count))*sub_entropy

         if debug : print "total entropy when partitioned w.r.t this attribute = ", tot_entropy

         # if this entropy is lower than min_entropy, min_entropy = total entropy, a_best = a
         if tot_entropy < min_entropy :
            min_entropy = tot_entropy
            a_best = a

         if (debug) : print "=================="

      if debug : print "minimum entropy = ", min_entropy
      if debug : print "attribute which delivers minimun entropy = ", self.attr_names[a_best]

      return a_best

   def id3 (self, examples, attributes, depth) : #, node) :
      if (debug) : print "Entering ID3, examples = ", examples, "attributes = ", attributes, "depth = ", depth
      # examples is a list of integers. Integer i in the list points to the training example self.training_examples[i]
      # attributes is a list of integers. Integer i in the list points to the attribute self.attr_table[i]

      # check that examples should never have 0 length.
      if len(examples) == 0  :
         print ("ERROR: examples array has length 0")
         sys.exit(0)

      # if the node has a depth == max allowed depth, make this a leaf node with the label = most common label in the examples set remaining.
      max_label_id = self.find_max_label(examples)
      if depth == self.max_depth :
         if debug : print "Max depth", depth, " reached, adding a leaf node with label = ", self.attr_table[-1][max_label_id]
         if debug1 :
            print "Tree depth limit", depth, " reached, following examples will be given the same label"
            self.print_examples (examples)
         if depth > self.depth :
            self.depth = depth
         return node(leaf = 1, label_id = max_label_id, weight = len(examples))

      if self.check_same_label (examples) :
         # create a leaf node with label = the common label
         label_id = self.training_examples[examples[0]][-1]
         if debug : print "All examples have the same label", self.attr_table[-1][label_id], ". Adding a leaf node with this label"
         if depth > self.depth :
            self.depth = depth
         return node(leaf = 1, label_id = label_id, weight = len(examples))

      # If len(examples) is 0 but len(attributes) is not zero (we dont have enough data). We create a leaf node and assign the label to the most common label
      # If len(attributes) is 0 but len(examples) is not zero. There are 2 possibilities here:
      # All the remaining examples have the same label (this is good). Just create a leaf node and assign it to that common label.
      # The remaining examples have different labels. Create a leaf node with the majority label in examples.
      # find the index of most commonly occuring label in examples
      if len(attributes) == 0 :
         # create a leaf node with max_label_ind
         if debug : print "No more attributes to check, most common label is ", self.attr_table[-1][max_label_id], "adding a leaf node with this label"
         if debug1 :
            print "No more attributes to check for the following examples"
            self.print_examples (examples)
         if depth > self.depth :
            self.depth = depth
         return node(leaf = 1, label_id = max_label_id, weight = len(examples))

      # find the best attribute w.r.t which to partition the data
      a_best = self.find_best_attr (examples, attributes)

      # create a node for attribute a_best
      new_node = node(leaf = 0, attr_id = a_best, weight = len(examples))
      if depth > self.depth :
         self.depth = depth

      # create a new array of attributes after removing the attribute a_best
      new_attributes = attributes[:]
      new_attributes.remove(a_best)
      for value_id in range(len(self.attr_table[a_best])) :
         examples_with_value = []
         for e in examples :
            if self.training_examples[e][a_best] == value_id :
               examples_with_value.append(e)

         if len(examples_with_value) == 0 :
            if (debug) : print "No examples with attribute", self.attr_names[a_best], " = ", self.attr_table[a_best][value_id], "adding leaf node with label ", self.attr_table[-1][max_label_id]
            if depth+1 > self.depth :
               self.depth = depth+1
            new_node.add_nbr(node(leaf = 1, label_id = max_label_id, weight = 0))
         else :
            if (debug) : print "Calling ID3 for attribute ", self.attr_names[a_best], " = ", self.attr_table[a_best][value_id]
            new_node.add_nbr(self.id3 (examples_with_value, new_attributes, depth+1))

      return new_node
