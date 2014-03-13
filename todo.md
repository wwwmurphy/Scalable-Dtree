
ToDo:
-----
- allow target attribute to not be at end; specify with index.
- have generated '.dtree' file be located in cwd, not in location of training data.
- write program 'dtree-sub' to extract subtrees.

- port to hadoop.
- refactor tree building to be scalable in map-reduce
- add features from C4.5
- Control GUI ??


Done:
-----
Mar 13, 2014
- Created program 'dtree-sub' to extract a subtree from larger tree 
  starting at specified node name. New pickle file is written and all
  pickle file header info is kept.
- Fix 'tree-info' to handle trivial 1x1 tree.
Mar 9, 2014
- Created program 'dtree-info'. Shows many dtree characteristics.
  Particularly useful when the tree is very big and therefore hard to 
  dump or render.
- Modify dtree pickle format to show the full list of attributes including 
  those that are dropped.

Feb 26, 2014
- Account for a classification record not having a particular attribute.
- Fix key error produced during tree testing where dictionary True and 
  False values counted.
- rename learn-dtree.py -> dtree-learn.py; test-dtree.py -> dtree-test.py;
  predict-dtree.py -> dtree-predict.py; tree2graph.py -> dtree2graph.py
- store cut_list in the pickled dtree. Remove -c from test-dtree.py
- Clean up cmdline args, when 2 filenames appear put dtree filename first

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

