import re
import copy
import math
import datetime as dt

import baltic3 as bt

"""A bunch of functions which I wrote to support my own baltic3.py.
"""




def preorder_traverse(node, preorder_ls, verbose=True):
    """Recursive algorith to traverse a tree, given a starting (current) node.
    Typical usage: input my_tree.cur_node, where my_tree is a baltic tree object.
    This tells preorder_traverse() to start traversal from the root.
    Prints out the order in which the nodes are visited.

    Usage:
    >>> preorder_ls = [] # init list to fill
    >>> preorder_traverse(my_input_node, preorder_ls)
    """
    preorder_ls.append(node)
    if node.branchType == "node":
        if verbose:
            print(node)
        preorder_traverse(node.children[0], preorder_ls)
        preorder_traverse(node.children[1], preorder_ls)
    elif node.branchType == "leaf":
        if verbose:
            print(node, node.name)


def postorder_traverse(node):
    opers = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv}
    res1 = None
    res2 = None
    if tree:
        res1 = postordereval(node.children[0])
        res2 = postordereval(node.children[1])
        if res1 and res2:
            return opers[node.parent](res1,res2)
        else:
            return node.parent


def read_tree(tree_path, sort_descending=True):
    """A simple tree reading function which reads just a tree string. Wraps:
    1. make_tree()
    2. my_tree.sortBranches(). This step gives each node/tip (x, y) coords.
    3. Extract tip names using leaf.index, searching until it encounters a ":"

    Notes
    -----
    * Doesn't need tip dates, but as a result, will not populate absoluteTime
    attributes either.
    * Can't read treesub trees. Error in Gytis' original make_tree()
    logic; I'm guessing this is something to do with being unable to read newick
    strings with named nodes/branches.

    Params
    ------
    tree_path: str; path to tree file.

    Returns
    -------
    my_tree: baltic tree object.
    """
    my_tree = bt.tree() # init empty tree object
    with open(tree_path) as f:
        tree_string = f.read()

    bt.make_tree(tree_string, my_tree)

    # Computes node heights and lengths, and sets treeHeight
    my_tree.traverse_tree()
    my_tree.sortBranches(descending=False)

    # Get tipnames straight from the tree string
    leaf_index_ls = [k.index for k in my_tree.leaves]
    leaf_name_dict = {} # leaf.index : leaf.name
    for idx in leaf_index_ls:


    return my_tree


def austechia_read_tree(tree_path, date_delim="_", make_tree_verbose=False):
    """Lifted from the austechia.ipynb. Best used for BEAST trees.

    THIS WORKS, DON'T TOUCH ANYTHING. Don't even add a verbosity param.
    I don't know why.
    """
    tipFlag=False
    tips={}

    for line in open(tree_path,'r'): ## iterate through FigTree lines
        l=line.strip('\n') ## strip newline characters from each line

        cerberus=re.search('dimensions ntax=([0-9]+);',l.lower()) ## check how many tips there are supposed to be
        if cerberus is not None:
            tipNum=int(cerberus.group(1))

        #####################
        cerberus=re.search('tree TREE([0-9]+) = \[&R\]',l) ## search for beginning of tree string in BEAST format
        if cerberus is not None:
            treeString_start=l.index('(') ## tree string starts where the first '(' is in the line
            ll=bt.tree() ## new instance of tree
            bt.make_tree(l[treeString_start:],ll, verbose=make_tree_verbose) ## send tree string to make_tree function, provide an empty tree object
        #####################

        if tipFlag==True: # I think this never procs
            cerberus=re.search('([0-9]+) ([A-Za-z\-\_\/\.\'0-9 \|?]+)',l) ## look for tip name map, where each tip is given an integer to represent it in tree
            if cerberus is not None:
                tips[cerberus.group(1)]=cerberus.group(2).strip("'") ## if you give tips an integer (in the form of a string), it will return the full name of the tip
            elif ';' not in l: ## something's wrong - nothing that matches the tip regex is being captured where it should be in the file
                print('tip not captured by regex:',l.replace('\t',''))

        if 'translate' in l.lower(): ## start looking for tips
            tipFlag=True
        if ';' in l: ## stop looking for tips
            tipFlag=False

    print("Number of objects found in tree string: %d"%(len(ll.Objects)))

    ## rename tips, find the highest tip (in absolute time) in the tree
    if len(tips)==0:
        for k in ll.Objects:
            if isinstance(k,bt.leaf):
                k.name=k.numName

        # read the tip date. Accepts decimal or calendar dates;
        # converts to a decidate if required.
        highestTip=max([decimalDate(x.name.strip("'").split(date_delim)[-1],variable=True) for x in ll.Objects if isinstance(x,bt.leaf)])
    else: ## there's a tip name map at the beginning, so translate the names
        ll.renameTips(tips) ## give each tip a name
        highestTip=max([decimalDate(x.strip("'").split(date_delim)[-1],variable=True) for x in tips.values()])

    ll.treeStats()
    ll.sortBranches(descending=False)
    ll.setAbsoluteTime(highestTip)
    print('Highest tip date: %.4f'%(highestTip))

    return ll


def decimalDate(date,fmt="%Y-%m-%d",variable=False,dateSplitter='-'):
    """ Converts calendar dates in specified format to decimal date.

    If the input date is already a float, does nothing.
    THIS IS NOT AN ADVISABLE HACK BECAUSE IT HIDES ERRORS.
    """

    if isfloat(date):
        #print("date already a decimal year, pass.")
        result = float(date)
    else:
        if variable==True: ## if date is variable - extract what is available
            dateL=len(date.split(dateSplitter))
            if dateL==2:
                fmt=dateSplitter.join(fmt.split(dateSplitter)[:-1])
            elif dateL==1:
                fmt=dateSplitter.join(fmt.split(dateSplitter)[:-2])

        adatetime=dt.datetime.strptime(date,fmt) ## convert to datetime object
        year = adatetime.year ## get year
        boy = dt.datetime(year, 1, 1) ## get beginning of the year
        eoy = dt.datetime(year + 1, 1, 1) ## get beginning of next year

        ## return fractional year
        result = year + ((adatetime - boy).total_seconds() / ((eoy - boy).total_seconds()))

    return result


def isfloat(value):
    """Checks if a string can be converted into a float.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


#def unique(o, idfun=repr):
#    """Reduce a list down to its unique elements."""
#    seen = {}
#    return [seen.setdefault(idfun(e),e) for e in o if idfun(e) not in seen]
