# baltic3
The Python 3 version of Baltic: the Backronymed Adaptable Lightweight Tree Import Code. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic). That `readme`'s worth a read to explain how the class structures are set up. Gytis' original version is being migrated over to Python3, but I'm not sure if it's still under active development.

The main libraries are:

* `baltic3` - contains the `tree`, `node` and `leaf` class definitions, and class methods.
* `baltic3_utils` - function library that contains public methods.
* `experimental` - function library that contains new methods which are still under development.

---
# Tree File Format
`Baltic` was written to accept BEAST MCC trees in mind, so any `.tre` file or `.nex` file needs to be wrangled to look like a BEAST MCC tree. There are 2 blocks which need for be formatted: the taxa block, and the tree block.

### Taxa Block

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

Baltic names *must* have a date at the end, in the format `yyyy-mm-dd`, `yyyy-mm` or `yyyy`, delimited from the rest of the name by some special character, (e.g. "`_`" or "`|`"). Some examples of valid names:

```
A/virusname1/virus_id1_2015-05
A/virusname1/virus_id1_2015-5-31
A/virusname1/virus_id1_2015-05-31
A/virusname1/virus_id1_2015-05-01
A/virusname1/virus_id1_2015

A/virusname1/virus_id1|2015-05
A/virusname1/virus_id1|2015-5-31
A/virusname1/virus_id1|2015-05-31
A/virusname1/virus_id1|2015-05-01
A/virusname1/virus_id1|2015
```

If there's no date to begin with, give the sequence name an arbitrary date. Because Baltic was originally designed for BEAST trees, it uses these dates to compute a decimal year (e.g. 2007-07-01 gets converted to 2007.5) and plots the node positions by decimal year, so that a time-scale can be shown on the x-axis as well. If the input tree is not a BEAST TREE, this is a dummy operation that does not affect the displayed tree topology.

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

![Image of Wikitree](https://github.com/Don86/baltic3/assets/wiki_tree.png)

---
# To Do/Dev Notes

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
