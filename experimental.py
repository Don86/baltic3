import time
import numpy as np
import pandas as pd
import itertools

from Bio import Phylo

"""
A bunch of cookbook or wrapper functions related to Bio.Phylo. Not strictly
related to baltic3, but I'm putting them here for git saving convenience.
"""

def tip_to_tip_distance(my_tree, tip1, tip2):
    """Computes the tip-to-mrca-to-tip distance between tip1 and tip2.

    PARAMS
    ------
    my_tree: biopython tree object.
    tip1, tip2: biopython Clade objects

    RETURNS
    -------
    tt_dist: float. tip-to-mrca-to-tip distance between tip1 and tip2.
    """

    mrca = my_tree.common_ancestor(tip1, tip2)
    t1_mrca_dist = my_tree.distance(tip1, mrca)
    t2_mrca_dist = my_tree.distance(tip2, mrca)

    tt_dist = t1_mrca_dist + t2_mrca_dist
    return tt_dist


def genetic_distance_matrix(my_tree, names_ls):
    """Returns an upper triangular similarity matrix of all pairwise branch
    distances between possible pairs of tipnames in names_ls.

    PARAMS
    ------
    my_tree: Bio.Phylo tree object
    names_ls: list of str. List of tipnames to compute genetic distance with,
    using branch lengths as a measure.

    RETURNS
    -------
    hm_data: np array of shape (len(names_ls), len(names_ls)), type float.
    """
    all_pairs = list(itertools.combinations((names_ls), 2))
    gd_ls = []
    n_seq = len(names_ls)
    for pair in all_pairs:
        x, y = pair
        gd = tip_to_tip_distance(my_tree, x, y)
        gd_ls.append(gd)

    # Construct heatmap data
    hm_data = np.zeros((n_seq, n_seq))
    idx = 0
    for i in range(n_seq):
        for j in range(i+1, n_seq):
            hm_data[i][j] = gd_ls[idx]
            idx += 1

    return hm_data


def get_clade_labels(my_tree, ref_names_ls, verbose=True):
    """Computes tip-to-tmrc-to-tip distances for each tipname in my_tree, to
    each reference name in ref_names_ls. my_tree must contain the reference
    names in ref_names_ls.

    PARAMS
    ------
    my_tree: a tree file, readable by Bio.Phylo.
    ref_names_ls: a list of reference tip names.
    verbose: verbosity parameter.

    RETURNS
    -------
    df: pandas dataframe with columns: tip_names, their distance to every given
    reference name, the nearest reference distance, and nearest reference label.

    TODO: implement thresholding by percentile.
    """
    t0 = time.time()

    # Get all tipnames
    names_ls = [x.name for x in my_tree.get_terminals()]

    # Check
    for ref_nm in ref_names_ls:
        if ref_nm not in names_ls:
            print("WARNING: %s not found in input tree!" % ref_nm)

    # Get the non-reference names
    non_ref_names_ls = list(set.difference(set(names_ls), set(ref_names_ls)))

    if verbose:
        print("No. of reference tip names = %s" % len(ref_names_ls))
        print("No. of non-reference tip names = %s" % len(non_ref_names_ls))

    # Compute all possible distances between all tips and all references
    contents = []
    for nm in non_ref_names_ls:
        line = [nm]
        for ref_nm in ref_names_ls:
            tt_dist = tip_to_tip_distance(my_tree, nm, ref_nm)
            line.append(tt_dist)

        contents.append(line)

    col_names = ["tip_name"]
    for ref_nm in ref_names_ls:
        col_names.append("dist_to_"+ref_nm)

    df = pd.DataFrame(data=contents,
                      columns=col_names)

    if verbose:
        print("Done in %.2fs" % (time.time() - t0))

    df_cols = list(df.columns)[1:]
    df["clade_label"] = df[df_cols].idxmin(axis=1)
    df["clade_label"] = df.apply(lambda row: str(row["clade_label"]).replace("dist_to_", ""), axis=1)
    df["min_dist"] = df.loc[:, df_cols].min(axis=1)

    return df
