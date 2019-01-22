# baltic3

This is a phylogenetic tree visualization library. Originally developed by Gytis Dudas, it wraps `matplotlib`

The Python 3 version of Baltic: the *Backronymed Adaptable Lightweight Tree Import Code*. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic). That `readme`'s worth a read to explain how the class structures are set up. Gytis' original version is being migrated over to Python3, but I'm not sure if it's still under active development.

The main libraries are:

* `baltic3` - contains the `tree`, `node` and `leaf` class definitions, and class methods.
* `baltic3_utils` - function library that contains public methods.
* `experimental` - function library that contains new methods which are still under development.

### Is this easy to learn?

Short answer: no.

Long answer: I'm not sure. In my use cases, I set up baltic to work (somewhat) like HTML(rendering)/CSS(parameter or attribute value definitions)/JS(any programmatic functionality), so if you're already familiar with that sort of setup, it might be that much easier. Otherwise, I've been learning D3JS on my own, which is similar - and it's difficult.

If you're new to Python, this is not a good starting point.

# Installation

There's no installation per se; simply `git clone` or download this repo to a known location (say, your desktop), and, in `Jupyter`, point your `PYTHONPATH` to it. That is, in `Jupyter`:

```
import sys
sys.path.append("path/to/baltc3")
```

# Tutorials

`baltic` is meant to be executed in Jupyter, since the final output is probably a pdf of your final image. There's a series to tutorial notebooks in the `/tutorials` directory.


# To Do/Dev Notes

Gytis is apparently upgrading his original `baltic` library to python3, but I'm reluctant to switch over because (A)
he hasn't fixed a None-type comparison error yet (comparing `float >= None`, no longer a permissible operation in Py3) and (B) `baltic3` has been aggressively used over 2017, even landing in publications and grant proposals. It _works_.

 - Find a way to allocate unique internal node identifiers of some kind, in either of the 3 tree-traversal methods.
 - Perform tip-to-mrca-to-tip computations. Problem is: can't identify the MRCA of two given tips, because the nodes don't have a unique identifier. These computations are currently done in `Bio.Phylo`; but calling to an external library seems inelegant.

### Porting over to Biopython

This would be tremendously useful primarily because Biopython is faster with I/O, and already accepts different kinds of inputs, and already has the associated `Bio.Phylo` tree classes and related functions. However, this would warrant a massive code overhaul; that is, translating a `Bio.Phylo()` object to a `baltic` object.

* Only one missing function: allocating (x, y) coords to each node.
* `Biopython` loads trees faster. `baltic` can take several minutes for a large tree. A rule of thumb is 1 minute per thousand tips (on a Macbook Pro 2015).
* `baltic` is too fussy about the tree input format (has to be nexus format).
* `baltic` can't handle asterisks, because it parses the newick string with regex, where '\*' is a wildcard character.

# Acknowledgements

* [Dr. Gytis Dudas](https://github.com/evogytis) - Wrote original code base in Python2
