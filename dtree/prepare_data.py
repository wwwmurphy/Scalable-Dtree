"""
    Parse CSV input data.
    The first line is taken to be the attribute labels and the last label,
    the last column, is the target attribute.
    Return a list giving the prepared data, attribute list and target attribute.
"""

import sys

def prepare_data(fd, drop_list, verbose, learn=True):
    """
    Parse CSV input data.
    The first line is taken to be the attribute labels and the last label,
    the last column, is the target attribute.
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
    attributes = attributes_orig[:]
    num_attributes = len(attributes)

    if verbose == True:
        sys.stderr.write("Initial Attribute count: %s\n" % num_attributes)
        sys.stderr.write("Initial Attribute list:\n%s\n" % attributes)
        sys.stderr.write("Attribute DropList: %s\n" % drop_list)

    if len(drop_list) > 0:
        attributes = drop_fields(attributes_orig, drop_list)
        num_attributes = len(attributes)
        if verbose == True:
            sys.stderr.write("New Attribute count: %s\n" % num_attributes)
            sys.stderr.write("New Attribute list:\n%s\n" % attributes)

    # Last header field is target attribute.
    target_attr = attributes[-1]

    # Create list of all lines from data file
    lines = [line.strip() for line in fd.readlines()]

    if learn is False:
        # remove last attribute for this next step
        del(attributes[-1])
        num_attributes = num_attributes - 1

    # Label every field in every data record by creating field:value tuples.
    # When 'learn' is False, the target attribute value will be None.
    data = []
    num_records = 0
    num_bad = 0
    if learn:   # Path for 'learn' function
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
    else:       # Path for 'predict' function
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
            fields.append(None) # placeholder for attribute to be predicted
            data.append(dict(zip(attributes, fields)))

    if verbose == True:
        sys.stderr.write("Number of records used: %s\n"
                         "Number of error records skipped: %s\n"
                         % (num_records, num_bad))
        sys.stderr.write("Attribute to predict: %s\n" % target_attr)

    return [data, attributes, attributes_orig, target_attr]


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

