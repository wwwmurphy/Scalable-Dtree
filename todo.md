

ToDo:
-----
- store cut_list in the pickled dtree. Remove -c from test-dtree.py
- allow target attribute to not be at end; specify with index.
- write program 'dtree-info' to report tree characteristics.
- write program 'dtree-sub' to extract subtrees.
- port to hadoop.
- refactor tree building to be scalable in map-reduce
- add features from C4.5
- Control GUI ??


Done:
-----
Feb 26, 2014
- Account for a classification record not having a particular attribute.
- Fix key error produced during tree testing where dictionary True and False values counted.
- rename learn-dtree.py -> dtree-learn.py; test-dtree.py -> dtree-test.py;
  predict-dtree.py -> dtree-predict.py; tree2graph.py -> dtree2graph.py

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

