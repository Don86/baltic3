# baltic3
Python 3 version of Baltic: the Backronymed Adaptable Lightweight Tree Import Code. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic).

## To Do/Dev Notes

I'm following the Unix philosophy of maintaining a library of "small, sharp tools". `baltic3` should accept *only* a tree file as input, with an optional secondary metadata sheet read as a `pandas` dataframe, and that's it (Note that sequence data is being excluded!). This makes `baltic3` more self-contained, smaller, easier to maintain, upgrade and troubleshoot. 

 - Find a way to accept just a tree string, without dates. IIRC when it currently can accept a tree string, but the resulting tree object won't have tip names, or something like that. Not sure if the tip/node attributes will be properly read as well (e.g. bootstrap values)
 - Perform tip-to-mrca-to-tip computations. Problem is: can't identify the MRCA of two given tips, because the nodes don't have a unique identifier. These computations are currently done in `Bio.Phylo`; but calling to an external library seems inelegant. 
