#!/bin/python

from dtree import prepare_data
from dtree import create_dtree
from dtree import print_tree_gv
from dtree import gain
from datetime import datetime
import sys, argparse, pickle


if __name__ == "__main__":
    """
    Build dtree from training data.
    Extract filename from command line.
    Open the file and return it.
    """

    starttime = datetime.now()

    clparser = argparse.ArgumentParser()
    clparser.add_argument('-g', '--graphviz',  action='store_true',
                          dest='gv_flag', default=False,
                          help='enable graphviz-formatted tree output')
    clparser.add_argument(dest='filename_traindata',
                          help='training data filename')
    clparser.add_argument('-n', '--notree', action='store_true',
                          dest='notree_flag', default='False',
                          help="Validate data, don't build tree")
    clparser.add_argument('-v', '--verbose', action='store_true', 
                          dest='verbose_flag', default=False,
                          help='More verbose status info.')
    clparser.add_argument('-c', '--cut', dest='cut_list', default="",
                          help='Fields to drop from each record.')
    clparser.add_argument('-t', '--tree-write', action='store_true', 
                          dest='pickle_flag', default="False",
                          help='Save tree to file.')

    args = clparser.parse_args()


    try:
        fd = open(args.filename_traindata, "r")
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" %
                         args.filename_traindata)
        sys.exit(0)

    data, attributes, target_attr = \
               prepare_data(fd, args.cut_list, args.verbose_flag)
    fd.close()

    if args.verbose_flag == True:
        sys.stderr.write("Data read and prepared.\n")
    if args.notree_flag == True:
        print "Program runtime is %s" % (datetime.now() - starttime)
        sys.exit(0)

    tree = create_dtree(data, attributes, target_attr, gain)

    if args.verbose_flag == True:
        sys.stderr.write("Decision Tree Created.\n")

    ftree = args.filename_traindata.split(".")
    if len(ftree) <= 1:
        ftree.append("")

    # Capture tree graph in file, run thru: "dot -Tpdf -O file"
    if args.gv_flag:
        ftree[-1] = "gv"
        fname_gv = ".".join(ftree)
        try:
            fout = open(fname_gv, 'wb')
        except IOError:
            sys.stderr.write("Error: Unable to create '%s' file.\n" % fname_gv)
            sys.exit(0)
        print_tree_gv(tree, fout, "dtree ")

    # Dump decision tree to a pickle file.
    if args.pickle_flag:
        ftree[-1] = "dtree"
        fname_tree = ".".join(ftree)
        try:
            fout = open(fname_tree, 'wb')
        except IOError:
            sys.stderr.write("Error: Unable to create '%s' file.\n"
                             % fname_tree)
            sys.exit(0)
        # Pickle the tree using highest protocol available.
        pickle.dump(attributes, fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(target_attr, fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(tree, fout, pickle.HIGHEST_PROTOCOL)
        fout.close()

    if args.verbose_flag == True:
        print "Program runtime is %s" % (datetime.now() - starttime)
