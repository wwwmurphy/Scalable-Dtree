"""
    Functions for calculating the information gain of a
    dataset as defined by ID3 (Information Theoretic) heuristic.
    Throughout here map() is used instead of list comprehensions 
    because this code will be ported to Hadoop.
"""

import math


def entropy(data, attr): 
    """ 
    Calculates entropy of the given data set for given attribute. 
    The data set coming in here is typically a subset of the full data.
    In information theory, entropy is a measure of the uncertainty in a
    random variable. In this context, the term usually refers to the 
    Shannon entropy, which quantifies the expected value of the 
    information contained in a message. Entropy is typically measured
    in bits. Shannon entropy is the average unpredictability in a
    random variable, which is equivalent to its information content.
    
    Data as a Markov Process: A common way to define entropy for text
    is based on the Markov model of text. For an order-0 source (each
    character is selected independent of the last characters), the
    binary entropy is: H(S)= -sum( prob_i * log_2(prob_i) )
    """ 

    # Count the frequency of values within a given 
    # attribute for this data subset.

    col = map(lambda rec: rec[attr], data)
    nrecs = len(col)
    uniq_vals = set(col)
    uniq_cnts = map(lambda val: col.count(val), uniq_vals)

    # Calculate the entropy of attr within this data subset.
    ent_pieces = map(lambda freq: math.log(float(freq)/nrecs, 2) *
                                  float(freq)/nrecs, uniq_cnts)

    return -1.0 * reduce(lambda x,y: x+y, ent_pieces)



def gain(data, attr, target_attr): 
    """ 
    Calculates information gain (inverse entropy) that 
    results by splitting the data on chosen attribute (attr). 
    """
 
    # Count the frequency of values within a given 
    # attribute for this data subset.
    col = map(lambda rec: rec[attr], data)
    uniq_val = set(col)
    uniq_cnt = map(lambda val: col.count(val), uniq_val)
    val_freq = dict(zip(uniq_val, uniq_cnt))
    # val_sum is generally the same as quantity of records unless 
    # an attribute is missing for a record.
    val_sum = sum(uniq_cnt)
    
    # Calculate sum of entropy for each subset of records weighted 
    # by their probability of occuring in training set.

    # extract all records with particular attribute value.
    # calculate entropy of the target value for that record subset.
    ent_pieces = map(lambda val: entropy(filter(lambda rec: rec[attr] == val, 
                   data), target_attr) * float(val_freq[val]), uniq_val)
    subset_entropy = reduce(lambda x,y: x+y, ent_pieces) / val_sum

    # Subtract entropy of chosen attribute from entropy of whole 
    # data set with respect to target attribute and return it 
    return (entropy(data, target_attr) - subset_entropy)
