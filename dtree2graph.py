#!/bin/python

from dtree import print_tree_gv
import sys, argparse, pickle


if __name__ == "__main__":
    """
    Build displayable graph in graphviz format from  pickled decision tree.
    Get filename from command line.
    """

    clparser = argparse.ArgumentParser(
               description='Transform tree file to GraphViz command file.'
                           ' Try: "dot -Tpdf -O file.gv"')
    clparser.add_argument(dest='filename_dtree',help='decision tree filename')
    clparser.add_argument('-c', '--console',action='store_true',default=False,
                       dest='stdout_flag',help='Send graph output to STDOUT.')
    args = clparser.parse_args()

    try:
        fd = open(args.filename_dtree, 'rb')
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" % args.filename_dtree)
        sys.exit(0)

    attributes = pickle.load(fd)
    target_attr = pickle.load(fd)
    drop_list = pickle.load(fd)
    tree = pickle.load(fd)
    fd.close()

    if args.stdout_flag:
        fout = sys.stdout
    else:
        try:
            fdtree = args.filename_dtree.split(".")
            if len(fdtree) <= 1:
                fdtree.append("")
            fdtree[-1] = "gv"
            fname_gv = ".".join(fdtree)
            fout = open(fname_gv, 'wb')
        except IOError:
            sys.stderr.write("Error: Unable to create '%s' file.\n" % fname_gv)
            sys.exit(0)

    print_tree_gv(tree, fout, "dtree ")

    fout.close()
