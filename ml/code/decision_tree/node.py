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

def print_tree (root, dec_tree) :
   # root.print_node ()
   if root.leaf :
      # s = "node {"+ str(dec_tree.attr_table[-1][root.label_id])+  "} edge from parent [->] node [left] {\\tiny 1}"
      s = "node {"+ str(dec_tree.attr_table[-1][root.label_id]) + " " + str(root.weight) +  "}"
   else :
      # s = "node {"+ str(dec_tree.attr_names[root.attr_id])+  "} edge from parent [->] node [left] {\\tiny 1}"
      s = "node {"+ str(dec_tree.attr_names[root.attr_id]) + str(root.weight) +  "}"

   for nbr in root.nbrs :
      s += "child {" + print_tree (nbr, dec_tree) + "} "
   return s

def main () :
   root = node (0)
   root.add_nbr(node(1))
   root.add_nbr(node(2))
   root.add_nbr(node(3))

   print_tree (root)

# main ()
