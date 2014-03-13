#!/bin/python

import sys, argparse, pickle

# These are all globals.
nodes_r = 0
leaves_r = 0
leaf_names_r = {}

def tree_stats(tree):
    """
    Count total number of internal nodes, leaf nodes and 
    unique leaf names in the relative tree.
    """
    def tree_stats_r(tree):
        global nodes_r, leaves_r, leaf_names_r
        if type(tree) == dict:
            nodes_r += 1
            for item in tree.values()[0].values():
                tree_stats_r(item)
            return
        else:
            leaves_r += 1
            try:
                leaf_names_r[tree] += 1
            except KeyError:
                leaf_names_r[tree] = 1
        return

    tree_stats_r(tree)
    return nodes_r, leaves_r, leaf_names_r


def tree_geometry(rows):
    """
    Derives width and depth of the relative tree
    from the already prepared row dictionary.
    Returns [width, depth]
    """
    widths = []
    for r in range(len(rows)):
        widths.append(len(rows[r]))
    return max(widths), len(rows)


def tree_list_rows(tree):
    """
    Make list of rows of node attribute names.
    """
    def tree_list_rows_r(node, rows, deep):
        deep += 1
        if deep not in rows:
            rows[deep] = []
        if type(node) == type(""):
            rows[deep].append(node)
            return
        for item in node.values()[0].values():
            if type(item) == dict:
                rows[deep].append(item.keys()[0])
                tree_list_rows_r(item, rows, deep)
            else:
                rows[deep].append(item)
        return

    rows = {}
    deep = 0
    if type(tree) == dict:
        rows[deep] = [tree.keys()[0]]
    else:
        rows[deep] = [tree]
    tree_list_rows_r(tree, rows, deep)

    # Remove leaf nodes from all but the last row.
    leaves = list(set(rows[len(rows)-1]))
    rows[len(rows)-1] = leaves
    for r in range(len(rows)-1):
        new_row = [ node for node in rows[r] if node not in leaves ]
        rows[r]= list(set(new_row))

    # Promote all nodes to be as high in the geometry as they can be
    # (except leaves). Remove node duplicates found at lower levels.
    if len(rows) < 2:
        return rows
    for r in range(len(rows)-1):
        keepthese = rows[r]
        for s in range(r+1,len(rows)-1):
            rows[s] = [ node for node in rows[s] if node not in keepthese ]

    # There can now be empty rows, remove those.
    final_rows = {}
    deep = 0
    for r in range(len(rows)):
        if len(rows[r]) > 0:
            final_rows[deep] = rows[r]
            deep += 1

    return final_rows

 

if __name__ == "__main__":
    """
    Report to STDOUT many characteristics of a pickled decision tree.
    Get filename from command line.
    """

    clparser = argparse.ArgumentParser(
               description='Report decision tree characteristics.')
    clparser.add_argument(dest='filename_dtree',help='decision tree filename')
    clparser.add_argument('-d','--depth', dest='depth_value',
                       help='Dump node names across a given depth. 0 dumps ' +\
                       'all; give integer to select specific row, root is 1.')
    clparser.add_argument('--dump', dest='dump_flag', default=False,
                          action='store_true', help=argparse.SUPPRESS)
    args = clparser.parse_args()

    try:
        fd = open(args.filename_dtree, 'rb')
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" % args.filename_dtree)
        sys.exit(0)

    attributes = pickle.load(fd)
    attributes_orig = pickle.load(fd)
    drop_list = pickle.load(fd)
    target_attr = pickle.load(fd)
    tree = pickle.load(fd)
    fd.close()
    num_attrs = len(attributes)

    print "Decision Tree Information Dump."
    print "Filename: \"%s\"" % args.filename_dtree
    print("%d working Attributes." % num_attrs)
    sys.stdout.write("  ")
    for i in range(len(attributes)):
        sys.stdout.write(attributes[i])
        if i % 4 == 0 and i != 0:
            sys.stdout.write("\n  ")
        else:
            if i < len(attributes)-1:
                sys.stdout.write(", ")
            else:
                sys.stdout.write("\n")

    len_dl = len(drop_list)
    if len_dl > 0:
        print "  Original attribute list contained",
        if len_dl == 1:
            print "1 more attribute, %d: %s." % (drop_list[0], attributes_orig[drop_list[0]-1])
        else:
            dropped_attrs = "  "
            for i in range(len_dl-1):
                dropped_attrs += "%i: %s, " % (drop_list[i], attributes_orig[int(drop_list[i])-1])
            dropped_attrs += "%i: %s."      % (drop_list[len_dl-1], attributes_orig[int(drop_list[len_dl-1])-1])
            print "%d more attributes:\n  %s" % (len_dl, dropped_attrs)

    print "Node Names."
    if type(tree) == dict:
        print "    Root Attribute- \"%s\"" % tree.keys()[0]
    else:
        print "    Root Attribute- \"%s\"" % tree
    print "  Target Attribute- \"%s\"" % target_attr

    nodes, leaves, leaf_names = tree_stats(tree)
    print("Nodes.")
    print("  Internal: {:10,d}".format(nodes))
    print("  Leaf    : {:10,d}".format(leaves))
    print("  Total   : {:10,d}".format(nodes + leaves))
    print("Unique Leaf Nodes.")
    print("  {:s}".format(leaf_names))
    print("  Total: {:d}".format(len(leaf_names)))

    rows = tree_list_rows(tree)
    width, depth = tree_geometry(rows)
    print "Max Tree Geometry."
    print "  Width: %d" % width
    print "  Depth: %d" % depth
    
    if args.depth_value != None:
        desired_depth = int(args.depth_value)
        if desired_depth > depth:
            sys.stderr.write("Error: requested depth doesn't exist.\n")
            sys.exit(0)
        if desired_depth == 0:
            print "All Rows:"
            for i in range(len(rows)):
                print "Row %03d: %s" % (i+1, rows[i])
        else:
            print "Row %03d: %s" % (desired_depth, rows[desired_depth-1])

    if args.dump_flag:
        print
        print tree

