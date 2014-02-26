

ToDo:
- Bug, or maybe design deficiency:
./test-dtree.py test/cen1k.txt test/cen1k.dtree
Traceback (most recent call last):
  File "./test-dtree.py", line 59, in <module>
    total_recs = sums[True] + sums[False]
KeyError: False

- port to hadoop.
- refactor tree building to be scalable in map-reduce
- add features from C4.5
- Control GUI ??


Done:
Jan 23, 2014
- Evaluate separating initial node processing from
  work_list processing. Decided not to do it.
- Remove final loops in dtree.py
- Add pickling of tree.
- Program to read pickle and write graphviz file.
- Create prediction program to read in pickled dtree and evaluate test records.
  Mode to do large quantities and write result file.
- Write test program. Read pickled dtree, evaluate test records,
  provide accuracy results.
- Refactor

