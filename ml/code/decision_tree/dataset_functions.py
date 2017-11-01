#!/usr/bin/python

def gen_cv_set (examples, num_splits) :
    cv_set = []
    l = len(examples)/float(num_splits)
    for i in range (num_splits) :
        s = int(i*l)
        if i == num_splits - 1:
            cv_set.append (examples[s:])
        else :
            cv_set.append (examples[s:s+int(l)])
    return cv_set

def print_examples (examples, feature_values) :
    for ex in examples :
        s = ""
        for i, val in enumerate(ex) :
            s+=feature_values[i][val]+", "
        print s

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

    f.close()

    return examples

def make_discrete_features (examples, feat_desc_file, feat_en_file, debug = 0) :
    # takes in a list of examples that are not discretized
    # reads the features descrption file that tells how to discretize
    # returns discreteized examples, string description of features, string description of each range


    ## Parse the feature description file and populate the feature_descriptions, features_values and feature_ranges lists.
    f = open (feat_desc_file)
    lines = f.readlines ()
    f.close ()

    ex_len = len(examples[0])
    feature_descriptions = [0 for _ in range(ex_len)]
    feature_ranges       = [0 for _ in range(ex_len)]
    feature_values       = [0 for _ in range(ex_len)]
    feature_enables      = [0 for _ in range(ex_len)]

    ind = -1
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
        elif line[0] == 'e' : # enabled
            words = line[:-1].split()
            feature_enables[ind] = int (words[1])
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

    if debug :
        print "Before Filtering"
        print_examples (disc_examples, feature_values)

    f = open(feat_en_file)
    lines = f.readlines ()
    f.close ()

    for line in lines :
        if line[0] == '#' :
            pass
        else :
            words = line[:-1].split()
            feature_enables[int(words[0])-1] = int(words[1])

    # from each example, discard the features that are not enabled
    disc_examples_filtered = []
    feature_descriptions_filtered = []
    feature_ranges_filtered = []
    feature_values_filtered = []

    for ex in disc_examples :
        ex_filt = []
        for en, val in zip (feature_enables, ex) :
            if en :
                ex_filt.append (val)
        disc_examples_filtered.append(ex_filt)

    for i, en in enumerate (feature_enables) :
        if en :
            feature_descriptions_filtered.append (feature_descriptions[i])
            feature_ranges_filtered.append       (feature_ranges[i])
            feature_values_filtered.append       (feature_values[i])

    if debug :
        print "After Filtering"
        print_examples (disc_examples_filtered, feature_values_filtered)

    return [disc_examples_filtered, feature_descriptions_filtered, feature_values_filtered]

def gen_tree_latex (s) :
   f = open ("tree.tex", "w")
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

