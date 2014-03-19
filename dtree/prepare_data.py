"""
    Parse CSV input data.
    The first line is taken to be the attribute labels.
    Return a list giving the prepared data, attribute list and target attribute.
"""

import sys

def prepare_data(fd, drop_list, targ_attr_idx, verbose, learn=True):
    """
    Parse CSV input data.
    The first line is taken to be the attribute labels.
    The target attribute is among those labels and is designated 
    with a target attribute index. Indexing can be Pythonic, 
    eg: the last attribute can be specified with index -1.
    If 'learn' is True, 
        prepare full records for decision tree building.
    If 'learn' is False, 
        prepare records with missing target attribute value for prediction. 
        Each data record is expected to be 1 column shorter than the first
        record- the attribute list. The missing field is the value of
        the target attribute. 
    Return a list giving prepared data, attribute list and target attribute.
    """

    # Read first line from data file. It is taken to be the 
    # column header, aka: the Decision Tree Attributes.
    firstline = fd.readline().strip()
    attributes_orig = [attr.strip() for attr in firstline.split(",")]

    # Get target attribute. targ_attr_idx can use pythonic relative addressing
    try:
        target_attr = attributes_orig[targ_attr_idx]
    except:
        sys.stderr.write("Error in Index of Attribute to predict: %d\n" %\
                         targ_attr_idx)
        sys.exit(1)

    targ_attr_idx_norm = attributes_orig.index(target_attr) + 1

    if verbose == True:
        sys.stderr.write("Initial Attribute count: %s\n" % len(attributes_orig))
        sys.stderr.write("Initial Attribute list:\n%s\n" % attributes_orig)
        sys.stderr.write("Target Attribute index: %d\n" % targ_attr_idx_norm)
        sys.stderr.write("Attribute DropList: %s\n" % drop_list)

    if learn is False:
        # Remove predict attribute from attr list by adding to drop list.
        drop_list.append(targ_attr_idx_norm)

    attributes = drop_fields(attributes_orig, drop_list)
    num_attributes = len(attributes)

    if verbose == True:
        sys.stderr.write("New Attribute count: %s\n" % num_attributes)
        sys.stderr.write("New Attribute list:\n%s\n" % attributes)

    # Create list of all lines from data file
    lines = [line.strip() for line in fd.readlines()]

    # Label every field in every data record by creating field:value tuples.
    # When in 'predict' mode, the target attribute value will be None.
    data = []
    num_records = 0
    num_bad = 0
    fields_g = []
    for line in lines:
        line = line.strip().rstrip(',')
        if len(line) == 0:
            continue  # allow blank lines
        num_records = num_records + 1
        fields = [field.strip() for field in line.split(",")]
        fields = drop_fields(fields, drop_list)
        if len(fields) != num_attributes:
            num_bad = num_bad + 1
            print "Record #%d is malformed." % (num_records + 1)
            continue
        data.append(dict(zip(attributes, fields)))
        fields_g = fields

    if verbose == True:
        sys.stderr.write("Number of records used: %s\n"
                         "Number of error records skipped: %s\n"
                         % (num_records, num_bad))
        sys.stderr.write("Attribute to predict: %s\n" % target_attr)

    return [data, attributes, attributes_orig, target_attr]


# Drop list indices are based on 1.
def drop_fields(fields, drop_list):
    newfields = fields[:]
    if len(drop_list) == 0:
        return newfields
    nfields = len(newfields)
    for i in range(nfields):
        if (i+1) in drop_list:
            newfields[i] = None
    keep_list = filter(lambda i: newfields[i] != None, range(nfields)) 
    return map(lambda i: newfields[i], keep_list) 

