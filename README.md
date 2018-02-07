# DEPRECATED(?)

I'll keep watch on the original `baltic` repo, which is being migrated over to python3 anyway.

## baltic3
Python 3 version of Baltic: the Backronymed Adaptable Lightweight Tree Import Code. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic). That `readme`'s worth a read to explain how the class structures are set up.

* [Input formatting readme](https://github.com/Don86/baltic3/blob/master/examples/input_formatting.md)
* [Tutorial 1](https://github.com/Don86/baltic3/blob/master/examples/Tutorial%201%20-%20Basics.ipynb) - Basics and simple plot
* [Tutorial 2](https://github.com/Don86/baltic3/blob/master/examples/Tutorial%202%20-%20A%20Tree%20and%20Horizontal%20Bar%20Chart.ipynb) - A tree and a bar chart
* [Tutorial 3](https://github.com/Don86/baltic3/blob/master/examples/Tutorial%203%20-%20Tree%20with%20Heatmap.ipynb) - Tree with heatmap

## To Do/Dev Notes

I'm following the Unix philosophy of maintaining a library of "small, sharp tools". `baltic3` should accept *only* a tree file as input, with an optional secondary metadata sheet read as a `pandas` dataframe, and that's it (Note that sequence data is being excluded!). This makes `baltic3` more self-contained, smaller, easier to maintain, upgrade and troubleshoot.

 - Find a way to accept just a tree string, without dates. IIRC when it currently can accept a tree string, but the resulting tree object won't have tip names, or something like that. Not sure if the tip/node attributes will be properly read as well (e.g. bootstrap values)
 - Perform tip-to-mrca-to-tip computations. Problem is: can't identify the MRCA of two given tips, because the nodes don't have a unique identifier. These computations are currently done in `Bio.Phylo`; but calling to an external library seems inelegant.
