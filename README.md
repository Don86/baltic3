# baltic3

`baltic`(*Backronymed Adaptable Lightweight Tree Import Code*) is a phylogenetic tree visualization library. Originally developed by Dr. Gytis Dudas, a postdoc at Trevor Bedford's lab, it wraps `matplotlib` with its own proprietary `tree` object. The original Python2 version is available over at the [Bedford Lab](https://github.com/blab/baltic). That `readme`'s worth a read to explain how the class structures are set up.

* `baltic` isn't as good as `Biopython` at tree manipulation...
* But it's far superior at visualization for presentation and publication-standard figures.
* `baltic` trades off ease-of-use with flexibility. I'd call it difficult to learn, but easy to master.

The modules are:

* `baltic3` - contains the `tree`, `node` and `leaf` class definitions, and class methods.
* `baltic3_utils` - function library that contains public methods.
* `experimental` - function library that contains new methods which are still under development.

# Installation

There's no installation per se; simply `git clone` or download this repo to a known location (say, your desktop), and, in `Jupyter`, point your `PYTHONPATH` to it. That is, in `Jupyter`:

```
import sys
sys.path.append("path/to/baltic3")

# import the modules of this package
# Only 2 modules
import baltic3 as bt
import baltic3_utils as btu
```

# Tutorials

`baltic` is meant to be executed in Jupyter, since the final output is probably a pdf of your final image. There's a series of example notebooks in the `/tutorials` directory of this repo. In recommended order:

* [Tutorial 1](https://github.com/Don86/baltic3/blob/master/tutorials-and-examples/Tutorial1.md) - Required input format for `baltic`.
* [Tutorial 2](https://github.com/Don86/baltic3/blob/master/tutorials-and-examples/Tutorial2.md) - About the `baltic` tree object.
* [Gallery](https://github.com/Don86/baltic3/blob/master/tutorials-and-examples/Gallery.ipynb) - Gallery of examples, though so far there's only 1 example in there.
* (upcoming) - Drawing simple shapes with `matplotlib`
* (upcoming) - `matplotlib artist objects`: Drawing many, many simple shapes very quickly.

The rest of the examples are more complex examples of different visualisations.

### Is this easy to learn?

(This is the most frequently asked question I get)

Short answer: no.

Long answer: It's easy if you know how to do it, which is a perfectly accurate but perfectly useless answer. In my use cases, I set up baltic to work in `Jupyter` notebooks like the front-end trifecta of HTML/CSS/JS (or: rendering with `matplotlib`/parameter or attribute value definitions/programmatic functionality, respectively).  If that last sentence was gibberish to you, this will have a bit of a learning curve. Otherwise, if you're already familiar with that sort of paradigm, it might be that much easier.

If you're new to Python, this is not a good starting point.

# Dev Notes

The very long to-do list [here](https://github.com/Don86/baltic3/blob/master/assets/dev-notes.md).
