#!/bin/python

from dtree import classify
from dtree import prepare_data
from collections import Counter
import os, sys, argparse, pickle


def predicted_file(fname_predict, results, targ_attr):
  """
  Copy from file to make predictions for, insert the prediction
  result into each record and write out a new file.
  """

  # re-open the file for which to make predictions
  try:
    fp_rd = open(args.filename_predict, "r")
  except IOError:
    sys.stderr.write("Error: file '%s' not found.\n" % args.filename_predict)
    sys.exit(0)

  # open new file to create with predicted results
  try:
    filename_base = os.path.basename(args.filename_predict)
    fpred = filename_base.split(".")
    if len(fpred) <= 1:
      fpred.append("")
    fpred[-1] = "predicted"
    fname_pred = ".".join(fpred)
    fp_wr = open(fname_pred, 'wb')
  except IOError:
    sys.stderr.write("Error: Unable to create '%s' file.\n" % fname_pred)
    sys.exit(0)

  # Insert prediciton result in each record while writing out the file.
  try:
    first_line = fp_rd.readline() # copy 1st line over.
    fp_wr.write(first_line)

    # Get index of target attribute
    line = first_line.lstrip().rstrip(' ,\n\t')
    fields = [field.strip() for field in line.split(',')]
    print fields
    targ_attr_idx = fields.index(targ_attr)

    i= 0
    for line in fp_rd:
      line = line.lstrip().rstrip(' ,\n\t')
      fields = [field.strip() for field in line.split(',')]
      fields[targ_attr_idx] = results[i]
      fp_wr.write(','.join(fields) + '\n')
      i = i + 1
  except IOError:
    sys.stderr.write("Error: copying predict file.\n")
    sys.exit(0)

  fp_rd.close()
  fp_wr.close()


if __name__ == "__main__":
    """
    Given a pickled decision tree file and a file of records which do not
    include a result attribute, go through each record and add a 
    prediction result.
    Extract filename from command line.
    """

    clparser = argparse.ArgumentParser()
    clparser.add_argument(dest='filename_dtree',
                          help='Decision tree filename')
    clparser.add_argument(dest='filename_predict',
                          help='File holding data needing predictions')
    clparser.add_argument('-r', '--results', dest='results_flag', 
                          action='store_true', default=False,
                          help='Give results to stdout as a list.')
    clparser.add_argument('-v', '--verbose', action='store_true', 
                          dest='verbose_flag', default=False,
                          help='More verbose status info.')
    clparser.add_argument('-w', '--write', dest='write_flag', 
                          action='store_true', default=False,
                          help='Write file with prediction result per record.')

    args = clparser.parse_args()

    try:
        fd_dt = open(args.filename_dtree, 'rb')
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" 
                         % args.filename_dtree)
        sys.exit(0)

    attributes_dt = pickle.load(fd_dt)
    attributes_orig = pickle.load(fd_dt)
    targ_attr_idx = pickle.load(fd_dt)
    drop_list = pickle.load(fd_dt)
    target_attr = pickle.load(fd_dt)
    tree = pickle.load(fd_dt)
    fd_dt.close()

    try:
        fd_pd = open(args.filename_predict, "r")
    except IOError:
        sys.stderr.write("Error: file '%s' not found.\n" 
                         % args.filename_predict)
        sys.exit(0)

    # 2nd argument is a null drop list
    pdata, attributes, ignore_attr_orig, ignore_targ_attr = \
      prepare_data(fd_pd, [], targ_attr_idx, args.verbose_flag, learn=False)
    fd_pd.close()

    if args.verbose_flag == True:
        sys.stderr.write("%d records to predict have been read and prepared.\n"
                         % len(pdata))

    results = classify(tree, pdata)

    if args.results_flag == True:
        print("Prediction results in simple list form:\n%s\n"
                         % results)

    # Write a file with predictions by reading given unclassified data
    # file, append prediction to each record and write out new file.
    if args.write_flag == True:
        predicted_file(args.filename_predict, results, target_attr)
