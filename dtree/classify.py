"""
    Functions responsible for using decision tree for data classification.
    Throughout here map() is used instead of list comprehensions 
    because this code will be ported to Hadoop.
    IE: This "out = map(function, L)" instead of this:
             "out = [function(item) for item in L]"
"""

def get_class(record, node):
    """
    Traverses decision tree, returns classification for given record.
    """
    # Leaf nodes are of type string. Traverse tree until leaf node found.
    while type(node) != type(" "):
        attr = node.keys()[0]
        node = node[attr][record[attr]]
    return node


def classify(tree, data):
    """
    Returns list of classifications for each record in data
    list as determined by decision tree.
    """
    return map(lambda rec: get_class(rec, tree), data)

