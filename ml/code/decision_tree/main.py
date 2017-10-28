#!/usr/bin/python

import sys
from decision_tree import *

def trial_run () :
   # Create the dataset in problem 1.2
   attr_names = [
      "technology",
      "environment",
      "human",
      "distance",
      "invade"]

   attr_table = [
      ["Y", "N"],       # superior technology   (attr 0)
      ["Y", "N"],       # environment           (attr 1)
      ["X", "L", "H"],  # human                 (attr 2)
      [1, 2, 3, 4],     # distance              (attr 3)
      ["Y", "N"]]       # Invade? (output)      (attr 4)

   raw_training_examples = [
      ["N", "Y", "X", 1, "Y"],
      ["N", "Y", "L", 3, "N"],
      ["N", "N", "X", 4, "Y"],
      ["Y", "Y", "L", 3, "Y"],
      ["Y", "N", "L", 1, "N"],
      ["N", "Y", "X", 2, "Y"],
      ["N", "N", "H", 4, "N"],
      ["N", "Y", "X", 3, "Y"],
      ["Y", "N", "L", 4, "N"]]

   training_examples = []
   for r in raw_training_examples :
      tr_ex_row = []
      for ind, f in enumerate(r):
         for attr_ind, attr_val in enumerate(attr_table[ind]) :
            if f == attr_val :
               tr_ex_row.append(attr_ind)
      training_examples.append(tr_ex_row)

   for row in training_examples :
      print row 

   D = decision_tree(attr_names, attr_table, training_examples)
   dec_tree_root = D.create_tree()
   tree_latex = print_tree(dec_tree_root, D)
   gen_tree_latex(tree_latex)
   #print classify ([1, 1, 2, 3, 1], dec_tree_root)

def gen_tree_latex (s) :
   f = open ("tree1.tex", "w")
   tex = """
   \documentclass{article} 
   \usepackage{tikz}
   \usepackage[pass, paperwidth=20in, paperheight=11in]{geometry}
   \usetikzlibrary{trees}
   \\begin{document}
   \\begin{tikzpicture}[level distance=3cm,
     level 1/.style={sibling distance=25cm},
     level 2/.style={sibling distance=15cm},
     level 3/.style={sibling distance=10cm},
     level 4/.style={sibling distance=5cm},
     level 5/.style={sibling distance=2cm},
     level 6/.style={sibling distance=1.5cm},
     level 8/.style={sibling distance=1.5cm},
     level 9/.style={sibling distance=1.5cm},
     scale = 0.25, transform shape
      ]
     \\"""+s+""";
   \end{tikzpicture}
   \end{document}"""
   f.write(tex)
   f.close()

def check_vowel (c) :
   return (c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u' or c == 'A' or c == 'E' or c == 'I' or c == 'O' or c == 'U')

def vowel_count (s) :
   s1 = s.lower()
   return (s1.count('a') + s1.count('e') + s1.count('i') + s1.count('o') + s1.count('u'))

FN_G_LN     = 1 << 0 # first name longer than last name
MN          = 1 << 1 # does middle name exit?
FNFL_E_LNFL = 1 << 2 # first letter of first name == first letter of last name
FN_B_LN     = 1 << 3 # first name appears before last name in dictionary
FN2_VOW     = 1 << 4 # 2nd letter of first name is a vowel
LN_EVEN     = 1 << 5 # number of letters in last name == even
LN1_VOW     = 1 << 6 # first letter of last name is a vowel
FN_EVEN     = 1 << 7 # number of letters in first name == even
FN1_VOW     = 1 << 8
FNL_VOW     = 1 << 9
LNL_VOW     = 1 << 10
FN_DOT      = 1 << 11
LN_DOT      = 1 << 12
FN_LEN      = 1 << 13
LN_LEN      = 1 << 14
FN_E_LN_LEN = 1 << 15
LN2_VOW     = 1 << 16
HYP         = 1 << 17
MN_G_1      = 1 << 18
FLFN_LLFN   = 1 << 19
FLLN_LLLN   = 1 << 20
VOW_CNT     = 1 << 21
FVOW_CNT    = 1 << 22
LVOW_CNT    = 1 << 23
FLFN        = 1 << 24
FLLN        = 1 << 25

def gen_training_examples (file_name, attr_table, enabled_attributes) : # s is one line from the training data
   global FN_G_LN    
   global MN         
   global FNFL_E_LNFL
   global FN_B_LN    
   global FN2_VOW    
   global LN_EVEN    
   global LN1_VOW    
   global FN_EVEN    
   global FN1_VOW    
   global FNL_VOW    
   global LNL_VOW    
   global FN_DOT     
   global LN_DOT     
   global FN_LEN     
   global LN_LEN     
   global FN_E_LN_LEN
   global LN2_VOW
   global HYP
   global MN_G_1
   global FLFN_LLFN
   global FLLN_LLLN
   global VOW_CNT
   global FVOW_CNT
   global LVOW_CNT
   global FLFN
   global FLLN

   # read the training data file
   f = open (file_name)
   g = open (file_name)
   lines = g.readlines()

   training_examples = []
   for line in f :
      # generate training example (extract features)
      s = line[:-1]
      training_example = []

      names = s[2:].split ()
      # num_names = len(names)
      first_name = names[0]
      last_name = names[-1]

      # check if first name longer than last name
      if enabled_attributes & 1 :
         if len(first_name) > len(last_name) :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # check if there is a middle name
      if enabled_attributes & 2 :
         if len(names) >= 3 :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # first letter of first name and first letter of last name are same
      if enabled_attributes & (1<<2) :
         if first_name[0].lower() == last_name[0].lower() :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # first name appears before last name in the dictionary
      if enabled_attributes & (1<<3) :
         if first_name < last_name :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # second letter of first name is a vowel
      if enabled_attributes & (1<<4) :
         if len(first_name) >= 2 :
            if check_vowel(first_name[1]) :
               training_example.append ("Y")
            else :
               training_example.append ("N")
         else :
            training_example.append ("N")

      # is number of letters in last name even?
      if enabled_attributes & (1<<5) :
         if len(last_name)%2 == 0 :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # Feature 7 : is the first letter of last name a vowel
      if enabled_attributes & (1<<6) :
         if check_vowel(last_name[0]) :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # Number of letters in first name is even
      if enabled_attributes & (1<<7) :
         if len(first_name)%2 == 0 :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # first letter of first name is a vowel
      if enabled_attributes & FN1_VOW :
         if check_vowel(first_name[0]) :
            training_example.append("Y")
         else :
            training_example.append("N")

      # last letter of first name is a vowel
      if enabled_attributes & FNL_VOW :
         if check_vowel(first_name[-1]) :
            training_example.append("Y")
         else :
            training_example.append("N")

      # last letter of last name is a vowel
      if enabled_attributes & LNL_VOW :
         if check_vowel(last_name[-1]) :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # there is a '.' in the first name
      if enabled_attributes & FN_DOT :
         if '.' in first_name :
            training_example.append("Y")
         else :
            training_example.append("N")

      # there is a '.' in the last name
      if enabled_attributes & LN_DOT :
         if '.' in last_name :
            training_example.append("Y")
         else :
            training_example.append("N")

      # length of first name
      if enabled_attributes & FN_LEN :
         if len(first_name) < 3 :
            training_example.append("3")
         elif len(first_name) > 8 :
            training_example.append("8")
         else :
            training_example.append(str(len(first_name)))

      # length of last name
      if enabled_attributes & LN_LEN :
         if len(last_name) < 3 :
            training_example.append("3")
         elif len(last_name) > 8 :
            training_example.append("8")
         else :
            training_example.append(str(len(last_name)))

      # length of first name == length of last name
      if enabled_attributes & FN_E_LN_LEN :
         if len(first_name) == len(last_name) :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # 2nd letter of last name is a vowel
      if enabled_attributes & LN2_VOW :
         if len(last_name) >= 2 :
            if check_vowel (last_name[1]) :
               training_example.append ("Y")
            else :
               training_example.append ("N")
         else :
            training_example.append ("N")

      # Does the name contain a '-'?
      if enabled_attributes & HYP :
         if '-' in s[2:] :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # is there more than one middle name?
      if enabled_attributes & MN_G_1 :
         if len(names) >= 4 :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # first letter of first name == last letter of firs name
      if enabled_attributes & FLFN_LLFN :
         if first_name[0].lower() == first_name[-1].lower() :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # first letter of last name == last letter of last name
      if enabled_attributes & FLLN_LLLN :
         if last_name[0].lower() == last_name[-1].lower() :
            training_example.append ("Y")
         else :
            training_example.append ("N")

      # vowel count in the entire name
      if enabled_attributes & VOW_CNT :
         num_vowels = vowel_count (s[2:])
         #print s[2:], num_vowels
         if num_vowels > 6 :
            training_example.append ("7")
         else :
            training_example.append (str(num_vowels))

      # vowel count in the first name
      if enabled_attributes & FVOW_CNT :
         num_vowels = vowel_count (first_name)
         if num_vowels > 3 :
            training_example.append ("4")
         else :
            training_example.append (str(num_vowels))

      # vowel count in the last name
      if enabled_attributes & LVOW_CNT :
         num_vowels = vowel_count (last_name)
         if num_vowels > 3 :
            training_example.append ("4")
         else :
            training_example.append (str(num_vowels))

      # first letter of the first name
      if enabled_attributes & FLFN :
         c = first_name[0].lower()
         if c.isalpha() :
            training_example.append(c)
         else :
            training_example.append('0')

      # first letter of last name
      if enabled_attributes & FLLN :
         c = last_name[0].lower()
         if c.isalpha() :
            training_example.append(c)
         else :
            training_example.append('0')

      # Finally, append the result (output label)
      training_example.append(s[0])

      t = []
      i = 0
      for attr_ind, value in enumerate(training_example) :
         i+=1
         try :
            t.append(attr_table[attr_ind].index(value))
         except :
            print "value not found is ", value
            print "attr index is ", attr_ind
            print attr_table[attr_ind]
            print t
            print lines[i]
            sys.exit(0)

      training_examples.append(t)

   f.close()

   return training_examples

def check_classify_acc (examples, root) : # all should be in the form of indices
   match_count = 0
   for e in examples :
      if classify (e, root) == e[-1] :
         match_count+=1

   return match_count/float(len(examples))

def find_stddev (data) :
   #print "data: ", data
   mean = sum(data)/float(len(data))
   s = 0
   for d in data :
      s+=(d-mean)**2

   return (s/(len(data)-1))**0.5

def main () :
   global FN_G_LN    
   global MN         
   global FNFL_E_LNFL
   global FN_B_LN    
   global FN2_VOW    
   global LN_EVEN    
   global LN1_VOW    
   global FN_EVEN    
   global FN1_VOW    
   global FNL_VOW    
   global LNL_VOW    
   global FN_DOT     
   global LN_DOT     
   global FN_LEN     
   global LN_LEN     
   global FN_E_LN_LEN
   global LN2_VOW
   global HYP
   global MN_G_1
   global FLFN_LLFN
   global FLLN_LLLN
   global VOW_CNT
   global FVOW_CNT
   global LVOW_CNT
   global FLFN
   global FLLN

   enabled_attributes = (
   FN_G_LN        | # first name longer than last name
   MN             | # does middle name exit?
   FNFL_E_LNFL    | # first letter of first name == first letter of last name
   FN_B_LN        | # first name appears before last name in dictionary
   FN2_VOW        | # 2nd letter of first name is a vowel
   LN_EVEN        | # number of letters in last name == even
   LN1_VOW        | # first letter of last name is a vowel
   FN_EVEN        | # number of letters in first name is even
   FN1_VOW        |  # first letter of first name is a vowel
   FNL_VOW        |  # last letter of first name is a vowel
   LNL_VOW        |  # last letter of last name is a vowel
   FN_DOT         |  # there is a '.' in the first name
   LN_DOT         |  # there is a '.' in the last name
   # FN_LEN         |  # length of first name
   # LN_LEN         |  # length of last name
   FN_E_LN_LEN    |  # length of first name == length of last name
   LN2_VOW        | # 2nd letter of last name is a vowel
   HYP            | # Is there a '-' in the name?
   MN_G_1         | # are there more than one middle names?
   FLFN_LLFN      | # first letter of first name == last letter of first name
   FLLN_LLLN      | # first letter of last name == last letter of last name
   VOW_CNT        | # number of vowels in the name
   FVOW_CNT       | # number of vowels in the first name
   LVOW_CNT       | # number of vowels in the last name
   # FLFN           | # first letter of the first name
   # FLLN           | # first letter of the last name
   0
   )

   if debug : print "enabled attributes = ", hex(enabled_attributes)

   attr_names = []
   if enabled_attributes & FN_G_LN     : attr_names.append ("FN G LN"      )
   if enabled_attributes & MN          : attr_names.append ("MN?"          )
   if enabled_attributes & FNFL_E_LNFL : attr_names.append ("FNFL == LNFL" )
   if enabled_attributes & FN_B_LN     : attr_names.append ("FN bef LN"    )
   if enabled_attributes & FN2_VOW     : attr_names.append ("FN2 vow"      )
   if enabled_attributes & LN_EVEN     : attr_names.append ("LN even"      )
   if enabled_attributes & LN1_VOW     : attr_names.append ("LN1 vow"      )
   if enabled_attributes & FN_EVEN     : attr_names.append ("FN even"      )
   if enabled_attributes & FN1_VOW     : attr_names.append ("FN1 VOW"      )
   if enabled_attributes & FNL_VOW     : attr_names.append ("FNL VOW"      )
   if enabled_attributes & LNL_VOW     : attr_names.append ("LNL VOW"      )
   if enabled_attributes & FN_DOT      : attr_names.append ("FN DOT "      )
   if enabled_attributes & LN_DOT      : attr_names.append ("LN DOT "      )
   if enabled_attributes & FN_LEN      : attr_names.append ("FN LEN "      )
   if enabled_attributes & LN_LEN      : attr_names.append ("LN LEN "      )
   if enabled_attributes & FN_E_LN_LEN : attr_names.append ("FN EQ LN LEN" )
   if enabled_attributes & LN2_VOW     : attr_names.append ("LN2 VOW"      )
   if enabled_attributes & HYP         : attr_names.append ("HYP"          )
   if enabled_attributes & MN_G_1      : attr_names.append ("MG GT 1"      )
   if enabled_attributes & FLFN_LLFN   : attr_names.append ("FLFN LLFN"    )
   if enabled_attributes & FLLN_LLLN   : attr_names.append ("FLLN LLLN"    )
   if enabled_attributes & VOW_CNT     : attr_names.append ("VOW CNT"      )
   if enabled_attributes & FVOW_CNT    : attr_names.append ("FVOW CNT"     )
   if enabled_attributes & LVOW_CNT    : attr_names.append ("LVOW CNT"     )
   if enabled_attributes & FLFN        : attr_names.append ("FLFN"         )
   if enabled_attributes & FLLN        : attr_names.append ("FLLN"         )
   attr_names.append("sign")

   attr_table = []
   if enabled_attributes & FN_G_LN     : attr_table.append(["Y", "N"])
   if enabled_attributes & MN          : attr_table.append(["Y", "N"])
   if enabled_attributes & FNFL_E_LNFL : attr_table.append(["Y", "N"])
   if enabled_attributes & FN_B_LN     : attr_table.append(["Y", "N"])
   if enabled_attributes & FN2_VOW     : attr_table.append(["Y", "N"])
   if enabled_attributes & LN_EVEN     : attr_table.append(["Y", "N"])
   if enabled_attributes & LN1_VOW     : attr_table.append(["Y", "N"])
   if enabled_attributes & FN_EVEN     : attr_table.append(["Y", "N"])
   if enabled_attributes & FN1_VOW     : attr_table.append(["Y", "N"])
   if enabled_attributes & FNL_VOW     : attr_table.append(["Y", "N"])
   if enabled_attributes & LNL_VOW     : attr_table.append(["Y", "N"])
   if enabled_attributes & FN_DOT      : attr_table.append(["Y", "N"])
   if enabled_attributes & LN_DOT      : attr_table.append(["Y", "N"])
   if enabled_attributes & FN_LEN      : attr_table.append(["3", "4", "5", "6", "7", "8"])
   if enabled_attributes & LN_LEN      : attr_table.append(["3", "4", "5", "6", "7", "8"])
   if enabled_attributes & FN_E_LN_LEN : attr_table.append(["Y", "N"])
   if enabled_attributes & LN2_VOW     : attr_table.append(["Y", "N"])
   if enabled_attributes & HYP         : attr_table.append(["Y", "N"])
   if enabled_attributes & MN_G_1      : attr_table.append(["Y", "N"])
   if enabled_attributes & FLFN_LLFN   : attr_table.append(["Y", "N"])
   if enabled_attributes & FLLN_LLLN   : attr_table.append(["Y", "N"])
   if enabled_attributes & VOW_CNT     : attr_table.append(["0", "1", "2", "3", "4", "5", "6", "7"])
   if enabled_attributes & FVOW_CNT    : attr_table.append(["0", "1", "2", "3", "4"])
   if enabled_attributes & LVOW_CNT    : attr_table.append(["0", "1", "2", "3", "4"])
   if enabled_attributes & FLFN        : attr_table.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0'])
   if enabled_attributes & FLLN        : attr_table.append(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0'])
   attr_table.append(["+", "-"])

   if debug :
      print "attributes table"
      for attr in attr_table :
         print attr

   training_examples = gen_training_examples ("./Updated_Dataset/updated_train.txt", attr_table, enabled_attributes)
   training_set = training_examples
   # training_set_size = int(len(training_examples)*0.75)
   # training_set = training_examples [:training_set_size]
   # cv_set = training_examples[training_set_size:]

   D = decision_tree(attr_names, attr_table, training_set)
   dec_tree_root = D.create_tree()
   # tree_latex = print_tree(dec_tree_root, D)
   # gen_tree_latex(tree_latex)

   #print "Using updated_train.txt as the training set"
   print "===== Question 3.1.c ====="
   print "Error on training set is ", (1-check_classify_acc (training_set, dec_tree_root)) * 100, "%"
   # print "accuracy on cv set is ", check_classify_acc (cv_set, dec_tree_root)
   #print "Using updated_test.txt as the test set"
   print "===== Question 3.1.d ====="
   print "Error on test set is ", (1-check_classify_acc (gen_training_examples ("./Updated_Dataset/updated_test.txt", attr_table, enabled_attributes), dec_tree_root)) * 100, "%"
   print "===== Question 3.1.e ====="
   print "tree depth = ", D.depth

   part2 = 1
   verbose = 0
   #dep_file = open ("../DepthData.tex", 'w')
   depth_data = ""
   if part2 :
      print "===== Question 3.2.a ===="
      best_depth = 0
      best_accuracy = 0
      for max_depth in [1,2,3,4,5,10,15,20] :
         print "--- max depth = ", max_depth
         cv_accuracy_accum = 0
         tr_accuracy_accum = 0
         cv_acc_array = []
         for i in range (3, -1, -1) : # {
            training_set = []
            
            str_tr = "Using the following files as training data: "
            str_cv = "Using the following file as cross validation data "
            if i != 0 :
               # print "00"
               str_tr+="updated_training00.txt, "
               training_set+=gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training00.txt", attr_table, enabled_attributes)
            else :
               cv_set = gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training00.txt", attr_table, enabled_attributes)
               str_cv += "updated_training00.txt"

            if i != 1 :
               #print "01"
               str_tr+="updated_training01.txt, "
               training_set+=gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training01.txt", attr_table, enabled_attributes)
            else :
               cv_set = gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training01.txt", attr_table, enabled_attributes)
               str_cv += "updated_training01.txt"

            if i != 2 :
               #print "02"
               str_tr+="updated_training02.txt, "
               training_set+=gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training02.txt", attr_table, enabled_attributes)
            else :
               cv_set = gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training02.txt", attr_table, enabled_attributes)
               str_cv += "updated_training02.txt"

            if i != 3 :
               #print "03"
               str_tr+="updated_training03.txt, "
               training_set+=gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training03.txt", attr_table, enabled_attributes)
            else :
               #print "03"
               cv_set = gen_training_examples ("./Updated_Dataset/Updated_CVSplits/updated_training03.txt", attr_table, enabled_attributes)
               str_cv += "updated_training03.txt"

            # print training_set
            D = decision_tree(attr_names, attr_table, training_set, max_depth = max_depth)
            dec_tree_root = D.create_tree()
            # print "decision tree created"

            if verbose == 1 : print str_tr
            tr_accuracy = check_classify_acc (training_set, dec_tree_root)
            if verbose == 1 : print "accuracy on training set is ", tr_accuracy
            tr_accuracy_accum+=tr_accuracy

            if verbose == 1 : print str_cv
            cv_accuracy = check_classify_acc (cv_set, dec_tree_root)
            if verbose == 1 : print "accuracy on cross validation set is ", cv_accuracy
            if verbose == 1 : print ""
            cv_accuracy_accum+=cv_accuracy
            cv_acc_array.append(cv_accuracy)
         # }

         #print "average accuracy on training set = ", tr_accuracy_accum/4.0
         print "average cross validation accuracy = ", cv_accuracy_accum*100/4.0, "%"
         print "standard deviation in cross validation accuracy = ", find_stddev (cv_acc_array)*100, "%"
         if (cv_accuracy_accum/4.0 > best_accuracy) :
            best_depth = max_depth
            best_accuracy = cv_accuracy_accum/4.0

         #depth_data +=str(max_depth)+'&'+str(round(tr_accuracy_accum*100/4.0,1))+'&'+str(round(cv_accuracy_accum*100/4.0,1))+'&'+str(round(find_stddev (cv_acc_array)*100,1))+'\\\\\n'
         depth_data +=str(max_depth)+'&'+str(round(cv_accuracy_accum*100/4.0,1))+'&'+str(round(find_stddev (cv_acc_array)*100,1))+'\\\\\n'
         #print ""

      print ""
      print "The highest cross validation accuracy is obtained with a tree depth of ", best_depth, "(accuracy =", best_accuracy*100, "%)"
      #dep_file.write(depth_data)
      #dep_file.close()

      print ""
      print "===== Question 3.2.b ====="
      #print "Training the decision tree with updated_train_txt with a max_depth setting of ", best_depth
      training_set = gen_training_examples("./Updated_Dataset/updated_train.txt", attr_table, enabled_attributes)
      D = decision_tree(attr_names, attr_table, training_set, max_depth = best_depth)
      dec_tree_root = D.create_tree()

      #print "Checking accuracy of the decision tree on updated_train.txt"
      #print "accuracy on updated_train.txt is ", check_classify_acc (training_set, dec_tree_root)
      #print "Checking accuracy of the optimal decision tree on updated_test.txt"
      print "accuracy of depth-limited tree on test set is ", check_classify_acc (gen_training_examples ("./Updated_Dataset/updated_test.txt", attr_table, enabled_attributes), dec_tree_root) * 100, "%"

      #tree_latex = print_tree(dec_tree_root, D)
      #gen_tree_latex(tree_latex)
# trial_run ()
main ()
