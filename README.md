# baltic3
The Python 3 version of Baltic: the *Backronymed Adaptable Lightweight Tree Import Code*. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic). That `readme`'s worth a read to explain how the class structures are set up. Gytis' original version is being migrated over to Python3, but I'm not sure if it's still under active development.

The main libraries are:

* `baltic3` - contains the `tree`, `node` and `leaf` class definitions, and class methods.
* `baltic3_utils` - function library that contains public methods.
* `experimental` - function library that contains new methods which are still under development.

### Is this easy to learn?

Short answer: no.

Long answer: I'm not sure. In my use cases, I set up baltic to work (somewhat) like HTML(rendering)/CSS(parameter or attribute value definitions)/JS(any programmatic functionality), so if you're already familiar with that sort of setup, it might be that much easier. Otherwise, I've been learning D3JS on my own, which is similar - and it's difficult.

If you're new to Python, this is not a good starting point. 

# Input Tree File Format
`Baltic` was originally written to accept BEAST MCC trees in mind, so any `.tre` file or `.nex` file needs to be wrangled into a `nexus` format. Most tree computation software like `raxml`, `fasttree` or `treesub` will only spit out the newick string. There are 2 blocks which need for be formatted: the taxa block, and the tree block.

Say, we have a newick string like this:

```
(A_2010:0.1,B_2017:0.2,(C_2015:0.3,D_2012:0.4)[&branch="B1"]:0.5);
```

We'll need to add some stuff around it, so that `baltic` knows where to read in tipnames, labels, and so on (1).

### "Taxa" Block

This is a list of the taxa/virus/tip names, `Taxa1`, `Taxa2`...etc.

```
Begin taxa;
    Dimensions ntax=300;
        Taxlabels
        Taxa1
        Taxa2
        ...
        Taxa300
;
End;
```

(Previously, the `austechia_read_tree()` function required tipnames to have dates appended to the end; that requirement has been removed.)

### "Trees" Block
This is the block containing the actual tree itself, in Newick format.

```
begin trees;
    tree TREE1 = [&R] <start of newick format...>
```

Altogether, the following `Nexus` format is a valid format. Note that the node labels, `[&branch="something"]`, are optional. If this is, for instance, a RAXML tree with bootstrap labels at the nodes, then it would be something like `[&label=93]`, or something like that. The following is a full example of a formatted input `.tre` file:

```
#NEXUS
begin taxa;
    dimensions ntax=4;
	Taxlabels
	A_2010
	B_2017
	C_2015
	D_2012
;
end;

begin trees;
    tree TREE1 = [&R] (A_2010:0.1,B_2017:0.2,(C_2015:0.3,D_2012:0.4)[&branch="B1"]:0.5)[&branch="B2"];
end;
```

Produces a tree in Baltic tree like:

![Image of Wikitree](https://github.com/Don86/baltic3/blob/master/assets/wiki_tree.png)

---
# To Do/Dev Notes

Gytis is apparently upgrading his original `baltic` library to python3, but I'm reluctant to switch over because (A)
he hasn't fixed a None-type comparison error yet (comparing `float >= None`, no longer a permissible operation in Py3) and (B) `baltic3` has been aggressively used over 2017, even landing in publications and grant proposals. It _works_.

 - Find a way to accept just a tree string, without dates. IIRC when it currently can accept a tree string, but the resulting tree object won't have tip names, or something like that. Not sure if the tip/node attributes will be properly read as well (e.g. bootstrap values). Does `btu.read_tree()` work?
 - Find a way to allocate node identifiers of some kind, in either of the 3 tree-traversal methods.
 - Perform tip-to-mrca-to-tip computations. Problem is: can't identify the MRCA of two given tips, because the nodes don't have a unique identifier. These computations are currently done in `Bio.Phylo`; but calling to an external library seems inelegant.

### Porting over to Biopython

This would be tremendously useful primarily because Biopython is faster with I/O, and already accepts different kinds of inputs, and already has the associated `Bio.Phylo` tree classes and related functions. However, this would warrant a massive code overhaul; that is, translating a `Bio.Phylo()` object to a `baltic` object.

* Only one missing function: allocating (x, y) coords to each node.
* `Biopython` loads trees faster. `baltic` can take several minutes for a large tree. A rule of thumb is 1 minute per thousand tips (on a Macbook Pro 2015).
* `baltic` is too fussy about the tree input format (has to be nexus format).
* `baltic` can't handle asterisks, because it parses the newick string with regex, where '\*' is a wildcard character.
