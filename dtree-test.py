#!/bin/python

from dtree import classify
from dtree import prepare_data
from collections import Counter
import sys, argparse, pickle


if __name__ == "__main__":
    """
    Given a pickled decision tree file and a file of known correct test 
    records, compile test scores indicating the number of good and bad 
    test results and the percentage correctness.
    Extract filename from command line.
    """

    clparser = argparse.ArgumentParser()
    clparser.add_argument(dest='filename_dtree',
                          help='Decision tree filename')
    clparser.add_argument(dest='filename_testdata',
                          help='Test data filename')
    clparser.add_argument('-v', '--verbose', action='store_true', 
                          dest='verbose_flag', default=False,
                          help='More verbose status info.')

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

    try:
        fd_td = open(args.filename_testdata, "r")
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" 
                         % args.filename_testdata)
        sys.exit(0)

    tdata, attributes, ignore_attr_orig, ignore_targ_attr = \
        prepare_data(fd_td, drop_list, targ_attr_idx, args.verbose_flag)
    fd_td.close()

    if args.verbose_flag == True:
        sys.stderr.write("Test data read and prepared.\n")

    # make a list of predictions, one per tdata record
    results = classify(tree, tdata)
    res_map = map(lambda j,k: j==k[target_attr], results, tdata)
    sums = dict(Counter(res_map).most_common(2))
    sum_true = 0
    sum_false = 0
    if True in sums:
        sum_true = sums[True]
    if False in sums:
        sum_false = sums[False]
    total_recs = sum_true + sum_false
    print "Total record count: %d" % total_recs
    print "Correct predictions: %0.3f%%(%0.3f%%)" % \
          (float(100 * sum_true)  / float(total_recs),
           float(100 * sum_false) / float(total_recs))

    if args.verbose_flag == True:
        bad_recs = map(lambda m,n: (n+1) if m==False else True, res_map, 
                       range(len(res_map)))
        bad_recs = list(set(bad_recs))
        bad_recs.remove(True)
        bad_recs.sort()
        print "List of failed record indices, quantity %d, from test file %s:\n%s" % \
              (len(bad_recs), args.filename_testdata, bad_recs)
