"""
    Functions responsible for creating a new decision tree.
    Throughout here map() is used instead of list comprehensions 
    because this code will be ported to Hadoop.
    IE: This "out = map(function, L)" instead of this:
             "out = [function(item) for item in L]"
"""

from collections import Counter, deque

def leaf_detect(data, attributes, target_attr):
    """
    Link-Leaf detection
    """

    vals = map(lambda rec: rec[target_attr], data)
    # If dataset is empty or attributes list is empty, return the most
    # frequent target attribute value. When checking the attributes 
    # list for emptiness, subtract 1 to account for target attribute.
    if (len(attributes) - 1) <= 0:
        return Counter(vals).most_common(1)[0][0]

    # If all records in dataset have same classification, return that.
    if vals.count(vals[0]) == len(vals):
        return vals[0]

    return None


def node_choose(data, attributes, target_attr, fitness_func):
    """
    Choose next node
    """

    # Choose best attribute to best classify data. Look through all
    # attributes and find one with highest info gain, aka lowest entropy
    qual = filter(lambda attr: attr != target_attr, attributes)
    gains = map(lambda attr: fitness_func(data, attr, target_attr), qual)
    best_gain = max(gains)

    return qual[gains.index(best_gain)]


def create_dtree(data, attributes, target_attr, fitness_func):
    """
    Create list of Decision Tree nodes, each with up and down link info.
    Works breadth-first.
    Returns a new decision tree based on given attributes.
    """

    work_deque=deque()  # WQ
    node_deque=deque()  # NQ
    leaf_deque=deque()  # LQ

    work_deque.append([data, attributes, None, None])  # WQ
    while len(work_deque) != 0:
        data, attributes, inlink, upnode = work_deque.popleft()  # WQ

        # Leaf Detect
        vals = map(lambda rec: rec[target_attr], data)
        # If only the target attribute is left then the most 
        # frequent target attribute value is a leaf.
        if len(attributes) == 1:
            leaf = Counter(vals).most_common(1)[0][0]
            leaf_deque.append([leaf, inlink, upnode])  # LQ
            continue
        # If all records in dataset have same classification, got leaf.
        if vals.count(vals[0]) == len(vals):
            leaf_deque.append([vals[0], inlink, upnode])  # LQ
            continue

        # Choose best attribute to best classify data. Look through all
        # attributes, find one with highest info gain, aka lowest entropy
        qual = filter(lambda attr: attr != target_attr, attributes)
        gains = map(lambda attr: fitness_func(data, attr, target_attr), qual)
        best_attr = qual[gains.index(max(gains))]

        node = {best_attr:{}}
        attr_values = map(lambda rec: rec[best_attr], data)
        best_atvals = set(attr_values)
        for outlink in best_atvals:
            subdata = filter(lambda rec: rec[best_attr] == outlink, data)
            subattr = filter(lambda attr: attr != best_attr, attributes)
            node[best_attr][outlink] = None
            work_deque.append([subdata, subattr, outlink, node])  # WQ

        node_deque.append([node, inlink, upnode])  # NQ

    # Create connected nodes from node list.
    # The method used above creates nodes breadth first.

    # The first entry created is the root.
    root_node, inlink, upname = node_deque.popleft()  # NQ

    nlist = list(node_deque)  # NQ
    # Follow a node's uplink and edit it into the parent node.
    for n in xrange(len(nlist)):  # NL
        node, inlink, upnode = nlist[n]  # NL
        upnode[upnode.keys()[0]][inlink] = node

    llist = list(leaf_deque)  # LQ
    # Follow a leaf's uplink and edit it into the parent node.
    for n in xrange(len(llist)):
        name, inlink, upnode = llist[n]
        upnode[upnode.keys()[0]][inlink] = name

    return root_node

