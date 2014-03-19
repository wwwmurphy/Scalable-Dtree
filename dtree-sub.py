#!/bin/python

import os, sys, argparse, pickle

subtree = None

def gen_subtree(tree, node):

    def gen_subtree_r(tree):
        global subtree

        if subtree != None:
            return

        if type(tree) == dict:
            if tree.keys()[0] == node:
                subtree = tree
                return

            for item in tree.values()[0].values():
                gen_subtree_r(item)
        else:
            if tree == node:
                subtree = tree
                return
        return

    gen_subtree_r(tree)

    return subtree


if __name__ == "__main__":
    """
    Extract sub-dtree from input dtree and write out the new sub-tree.
    Get filename and starting node from command line.
    """

    clparser = argparse.ArgumentParser(
               description='Extract sub-tree from larger dtree.')
    clparser.add_argument(dest='filename_dtree',help='Decision tree filename')
    clparser.add_argument(dest='node_start',
                          help='Node in source dtree that will be the root '\
                          'of the extracted subtree.')
    clparser.add_argument(dest='filename_subtree',
                          help='Sub Decision Tree Filename')
    args = clparser.parse_args()

    try:
        fd = open(args.filename_dtree, 'rb')
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" % args.filename_dtree)
        sys.exit(0)

    attributes = pickle.load(fd)
    attributes_orig = pickle.load(fd)
    targ_attr_idx = pickle.load(fd)
    drop_list = pickle.load(fd)
    target_attr = pickle.load(fd)
    tree = pickle.load(fd)
    fd.close()
    # Got the original tree in memory.

    # Generate subtree
    subtree = gen_subtree(tree, args.node_start.strip())
    if subtree == None:
        print "Tree Node Not Found"
        sys.exit(1)

    filename_base = os.path.basename(args.filename_subtree)
    fdtree = filename_base.split(".")
    if len(fdtree) <= 1:
        fdtree.append("")
    fdtree[-1] = "dtree"
    fname_sub = ".".join(fdtree)
    try:
        fout = open(fname_sub, 'wb')
    except IOError:
        sys.stderr.write("Error: Unable to create '%s' file.\n" % fname_sub)
        sys.exit(0)
    # Made new file to hold subtree

    # Store subtree to a pickle file.
    # Pickle the tree using highest protocol available.
    pickle.dump(attributes,      fout, pickle.HIGHEST_PROTOCOL)
    pickle.dump(attributes_orig, fout, pickle.HIGHEST_PROTOCOL)
    pickle.dump(targ_attr_idx,   fout, pickle.HIGHEST_PROTOCOL)
    pickle.dump(drop_list,       fout, pickle.HIGHEST_PROTOCOL)
    pickle.dump(target_attr,     fout, pickle.HIGHEST_PROTOCOL)
    pickle.dump(subtree,         fout, pickle.HIGHEST_PROTOCOL)
    fout.close()
