"""
    Create draw commands in 'dot'/graphviz language format.
    Output can be run through this command:
        dot -Tpdf -O file.dot
"""

label_fmt  = "\"%s\" -> \"%s\" [label = \"%s\"]\n"
label_fmt_s= "\"%s\" -> \"%s\"\n"
box_fmt    = "\"%s\" [shape = \"box\"]\n"
circle_fmt = "\"%s\" [shape = \"circle\"]\n"

label_cache = {}
# These globals are used to reduce stack load in a recursive function.
fout = 0
leaf = None
collapse = False

def print_tree_gv(tree, fn_out, attr_collapse, str):
    global fout, collapse

    fout = fn_out
    collapse = attr_collapse
    fout.write("digraph %s {\n\n" % str)

    # Collect attributes so their shapes can be pre-declared
    attrs = []
    print_dotattr(tree, attrs)
    for item in set(attrs):
        fout.write(box_fmt % item)
    fout.write('\n')

    # Collect leaves so their shapes can be pre-declared
    leaves = []
    print_dotleaf(tree, leaves)
    for item in set(leaves):
        fout.write(circle_fmt % item)
    fout.write('\n')

    print_dotworker(tree, None, None)
    fout.write("\n}\n")


def print_dotattr(tree, attrs):
    if type(tree) == dict:
        attrs.append(tree.keys()[0])
        for item in tree.values()[0].keys():
            print_dotattr(tree.values()[0][item], attrs)


def print_dotleaf(tree, leaves):
    if type(tree) == dict:
        for item in tree.values()[0].keys():
            print_dotleaf(tree.values()[0][item], leaves)
    else:
        leaves.append(tree)


def edge_cache(attr, leaf, value):
    """
    This function is used when graph edges are collapsed.
    """
    if collapse == False:
        fout.write(label_fmt % (attr, leaf, value))
        return

    if leaf == None:
        return
    key = attr + leaf
    if key in label_cache:
        return

    fout.write(label_fmt_s % (attr, leaf))
    label_cache[key] = 0


def print_dotworker(tree, attr, value):
    # Of course globals are usually a bad idea, but since this is a 
    # recursive function and stack size matters, no parameters that 
    # don't change should be on the stack. The only reason 'leaf' can
    # be a global is because it's always a terminal node.
    global fout, leaf

    if type(tree) == dict:
        attr_old = attr
        attr = tree.keys()[0]
        if value != None:
            if leaf == None:
                edge_cache(attr_old, attr, value)
            else:
                edge_cache(attr, leaf, value)
        for item in tree.values()[0].keys():
            value = item
            print_dotworker(tree.values()[0][item], attr, value)
    else:
        leaf = tree
        if value != None:
            edge_cache(attr, leaf, value)
        leaf = None
