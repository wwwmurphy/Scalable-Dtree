#!/bin/python

from dtree import prepare_data
from dtree import create_dtree
from dtree import print_tree_gv
from dtree import gain
from datetime import datetime
import os, sys, argparse, pickle


if __name__ == "__main__":
    """
    Build dtree from training data.
    Extract filename from command line.
    """

    starttime = datetime.now()

    clparser = argparse.ArgumentParser()
    clparser.add_argument(dest='targ_attr_idx',
                          help='Index of attribute to learn/predict. '\
                               '1 based.')
    clparser.add_argument(dest='filename_traindata',
                          help='Training data filename')
    clparser.add_argument('-c', '--cut', dest='cut_list', default="",
                          help='Fields to drop from each record.')
    clparser.add_argument('-g', '--graphviz',  action='store_true',
                          dest='gv_flag', default=False,
                          help='Enable graphviz-formatted tree output')
    clparser.add_argument('-t', '--tree-write', action='store_true', 
                          dest='pickle_flag', default="False",
                          help='Save tree to file.')
    clparser.add_argument('-v', '--verbose', action='store_true', 
                          dest='verbose_flag', default=False,
                          help='More verbose status info.')

    args = clparser.parse_args()
    targ_attr_idx = int(args.targ_attr_idx)
    # If <0, leave unchanged so relative addressing can be used, eg: -1
    # If >0, decrement so the index becomes 0-based.
    if targ_attr_idx == 0:
        sys.stderr.write("Target Attribute index must start at 1\n")
        sys.exit(0)
    if targ_attr_idx > 0:
        targ_attr_idx -= 1

    try:
        fd = open(args.filename_traindata, "r")
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" %
                         args.filename_traindata)
        sys.exit(0)

    drop_list = []
    if len(args.cut_list) > 0:
        drop_list = [int(item) for item in args.cut_list.split(',')]
    data, attributes, attributes_orig, target_attr = \
          prepare_data(fd, drop_list, targ_attr_idx, args.verbose_flag)
    fd.close()

    if args.verbose_flag is True:
        sys.stderr.write("Data read and prepared.\n")
    if args.gv_flag is False and args.pickle_flag is False:
        print "Program runtime is %s" % (datetime.now() - starttime)
        sys.exit(0)

    tree = create_dtree(data, attributes, target_attr, gain)

    if args.verbose_flag is True:
        sys.stderr.write("Decision Tree Created.\n")

    filename_base = os.path.basename(args.filename_traindata)
    ftree = filename_base.split(".")
    if len(ftree) <= 1:
        ftree.append("")

    # Capture tree graph in file, run thru: "dot -Tpdf -O file"
    if args.gv_flag is True:
        ftree[-1] = "gv"
        fname_gv = ".".join(ftree)
        try:
            fout = open(fname_gv, 'wb')
        except IOError:
            sys.stderr.write("Error: Unable to create '%s' file.\n" % fname_gv)
            sys.exit(0)
        print_tree_gv(tree, fout, False, "dtree ")

    # Dump decision tree to a pickle file.
    if args.pickle_flag is True:
        ftree[-1] = "dtree"
        fname_tree = ".".join(ftree)
        try:
            fout = open(fname_tree, 'wb')
        except IOError:
            sys.stderr.write("Error: Unable to create '%s' file.\n"
                             % fname_tree)
            sys.exit(0)
        # Pickle the tree using highest protocol available.
        pickle.dump(attributes,      fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(attributes_orig, fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(targ_attr_idx,   fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(drop_list,       fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(target_attr,     fout, pickle.HIGHEST_PROTOCOL)
        pickle.dump(tree,            fout, pickle.HIGHEST_PROTOCOL)
        fout.close()

    if args.verbose_flag is True:
        print "Program runtime is %s" % (datetime.now() - starttime)
