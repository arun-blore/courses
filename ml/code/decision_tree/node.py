#!/usr/bin/python

class node :
   def __init__ (self, leaf, label_id = 0, attr_id = 0, weight = 0) :
      self.nbrs      = []
      self.leaf      = leaf
      self.label_id  = label_id
      self.attr_id   = attr_id
      self.weight    = weight

   def add_nbr (self, nbr_node) :
      self.nbrs.append(nbr_node)

   def print_node (self) :
      print "data = ", self.data

def main () :
   root = node (0)
   root.add_nbr(node(1))
   root.add_nbr(node(2))
   root.add_nbr(node(3))

   print_tree (root)

# main ()
