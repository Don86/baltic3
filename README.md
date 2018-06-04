# baltic3
The Python 3 version of Baltic: the Backronymed Adaptable Lightweight Tree Import Code. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic). That `readme`'s worth a read to explain how the class structures are set up. Gytis' original version is being migrated over to Python3, but I'm not sure if it's still under active development.

The main libraries are:

* `baltic3` - contains the `tree`, `node` and `leaf` class definitions, and class methods.
* `baltic3_utils` - function library that contains public methods.
* `experimental` - function library that contains new methods which are still under development.

---
### To Do/Dev Notes

Gytis is apparently upgrading his original `baltic` library to python3, but I'm reluctant to switch over because (A)
he hasn't fixed a None-type comparison error yet (comparing `float >= None`, no longer a permissible operation in Py3) and (B) `baltic3` has been aggressively used over 2017, even landing in publications and grant proposals. It _works_. I'll continue to upkeep `baltic3_utils.py` until he adds a sufficient number of useful features to warrant switching over.

 - Find a way to accept just a tree string, without dates. IIRC when it currently can accept a tree string, but the resulting tree object won't have tip names, or something like that. Not sure if the tip/node attributes will be properly read as well (e.g. bootstrap values). Does `btu.read_tree()` work?
 - Find a way to allocate node identifiers of some kind, in either of the 3 tree-traversal methods.
 - Perform tip-to-mrca-to-tip computations. Problem is: can't identify the MRCA of two given tips, because the nodes don't have a unique identifier. These computations are currently done in `Bio.Phylo`; but calling to an external library seems inelegant.

Porting over to Biopython

* Only one missing function: allocating (x, y) coords to each node.
* `Biopython` loads trees faster. `baltic` can take several minutes for a large tree (thousands of tips)
* `baltic` is too fussy about the tree input format (has to look like a BEAST tree)
* `baltic` can't handle asterisks, because it parses the newick string with regex, where '\*' is a wildcard character.
