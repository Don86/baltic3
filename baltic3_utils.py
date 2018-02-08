import matplotlib.pyplot as plt

import re
import copy
import math
import numpy as np
import pandas as pd
import datetime as dt

import baltic3 as bt

"""A bunch of functions which I wrote to support my own baltic3.py.
"""
def treesub_to_bt(fn_in, fn_out, verbose=True):
    """Reads raw treesub output, which is assumed to be in nexus format, does a
    bunch of necessary wrangling, then returns a format that can be read by
    austechia_read_tree(). Still requires a tree with dates, delimited by '_'.

    Params
    ------
    fn_in: string; treesub output, like "substitutions.tree"
    fn_out: filename to write the modified nexus format out to.

    Returns
    -------
    dm: dataframe of node_num (originally "NUMBER") and the associated non-syn
    subs.
    """
    # Assumes that raw treesub output is in nexus format
    # read treestring
    with open("subs.tre") as f:
        contents = f.readlines()
    contents = [x.strip() for x in contents]

    # Get the row which contains just the newick string
    for i in range(len(contents)):
        if contents[i] == "begin trees;":
            tree_string = contents[i+1]

    # Remove all spaces, and a bit of nexus formatting in front
    tree_string = tree_string.replace(" ", "")
    tree_string = tree_string.replace("treetree_1=[&R]", "")

    # =============== Extract stuff ===============
    # Get tip names
    tip_names_ls = []
    tip_name_start = 0
    for i in range(len(contents)):
        # switch on
        if contents[i] == "taxlabels":
            tip_name_start = 1
        # switch off
        if (contents[i] == ";") and (contents[i+1] == "end;") and (tip_name_start == 1):
            tip_name_start = 0

        if (tip_name_start == 1) and (contents[i] != "taxlabels"):
            pattern = re.compile(r"([\s\S]*?)\[&")
            tipname = re.findall(pattern, contents[i])[0]
            tip_names_ls.append(tipname)

    # Retrieve all treesub node_strings, "[&REALNAME=...]", from tree_string
    pattern = re.compile(r'\[&([\s\S]*?)\]:')
    node_strings_ls = re.findall(pattern, tree_string)

    # Replace the full treesub nodestring with just "NUMBER"
    # Keep a dictionary
    for node_string in node_strings_ls:
        # retrieve "NUMBER"
        pattern = re.compile(r'NUMBER="([\d]*?)",')
        node_num = re.findall(pattern, node_string)[0]
        tree_string = tree_string.replace(node_string, node_num)

    # Extract all the individual bits of node_strings
    contents = []
    for node_string in node_strings_ls:
        pattern = re.compile(r'NUMBER="([\d]*?)",')
        node_num = re.findall(pattern, node_string)[0]

        pattern = re.compile(r'NONSYNSUBS="([\s\S]*?)",')
        nssubs_ls = re.findall(pattern, node_string)
        nssubs = "*"
        if len(nssubs_ls) > 0:
            nssubs = nssubs_ls[0]
            for char in ["[", "]"]:
                nssubs = nssubs.replace(char, "")
        contents.append([node_num, nssubs])

    dm = pd.DataFrame(data=contents, columns=["node_num", "nonsynsubs"])


    # =============== Prep contents to write out a full nexus file ===============
    contents = ["#NEXUS"]
    for ln in ["begin taxa;", "dimensions ntax="+str(len(tip_names_ls))+";", "taxlabels"]:
        contents.append(ln)

    # add taxlabels
    for ln in tip_names_ls:
        contents.append(ln)

    contents.append(";")
    contents.append("end;")

    # add tree block
    tree_block_idx = len(contents)
    contents.append("begin trees;")
    contents.append("tree TREE1 = [&R] "+tree_string)
    contents.append("end;")

    with open(fn_out, "w") as f:
        for line in contents:
            f.write("%s\n" % line)

    # preview contents
    if verbose:
        preview_counter = 10
        for i in range(preview_counter):
            print(contents[i])
        print("...")
        print(contents[tree_block_idx])
        print(contents[tree_block_idx+1][:50]+"...")
        print(contents[tree_block_idx+2])
        print("")
        print("Written out to file %s" % fn_out)

    return dm


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


def quickdraw(my_tree, fig, ax, branch_width=0.5, tip_size=3):
    """Draws the tree, duh. Still doesn't work, though. KIV.
    """
    lines_ls = []
    # ==================== Tree ====================
    for k in my_tree.Objects:
        c = 'k'
        x=k.height # raw (x, y) coords
        y=k.y

        xp = k.parent.height
        if x is None: # matplotlib won't plot Nones, like root
            x = 0
        if xp==None:
            xp = x

        if isinstance(k,bt.leaf) or k.branchType=='leaf':
            #print(k.height)
            ax.scatter(x,y,s=tip_size,facecolor=c,edgecolor='none',zorder=11)
            ax.scatter(x,y,s=tip_size+0.8*tip_size,facecolor='k',edgecolor='none',zorder=10)

        elif isinstance(k,bt.node) or k.branchType=='node':
            #line = np.array([[x, k.children[0].y], [x, k.children[-1].y]])
            ax.plot([x, x], [k.children[0].y, k.children[-1].y], color="k", lw=branch_width)
            #lines_ls.append(line)

        #line = np.array([[xp, y], [x, y]])
        ax.plot([xp, x], [y, y], color="k", lw=branch_width)
        #lines_ls.append(line)

    #ax.add_collection(LineCollection(lines_ls, lw=branch_width,color='k', zorder=10))

    #plt.tight_layout()
    #plt.show()


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
    * Can read FastTree trees
    * Not able to sort tree branches; can only read the newick string exactly.

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
    tipname = ""
    window = tree_string
    for i in range(len(leaf_index_ls)):
        idx0 = leaf_index_ls[i]
        idx = leaf_index_ls[i]
        tipname = ""
        window = tree_string[idx]
        while window != ":":
            window = tree_string[idx]
            idx +=1
            tipname = tipname + window
        leaf_name_dict[idx0] = tipname[:-1]

    # Write name attribute of the original leaf objects
    for k in my_tree.leaves:
        k.name = leaf_name_dict[k.index]

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
