"""
Functions to analyse PG data.

M Gerlach & F Font-Clos
Sept 2018
"""
import pandas as pd
import importlib.util
import sys
sys.path[0] = "../gutenberg/src"
from metaquery import meta_query


def filter_bookshelves(df, min_books=50, max_books=150):
    """Filter bookshelves by size, overlap and language."""
    # filter by size
    cmin = df.sum() > min_books
    cmax = df.sum() <= max_books
    sdf = df.loc[:, cmin & cmax].dropna(how="all")

    # deal with overlaps
    sdf = sdf.loc[sdf.sum(axis=1) == 1].dropna(how="all", axis=1)

    # get rid of esperanto
    sdf = sdf.drop("Esperanto_(Bookshelf)", axis=1).dropna(how="all")

    # filter by language
    mq = meta_query(path="metadata/metadata.csv", filter_exist=True)
    mq.filter_lang("en", how="only")
    allPGs = mq.df.set_index("id").index
    sdf = sdf.loc[np.intersect1d(sdf.index, allPGs)].dropna(how="all", axis=1)
    print("after language", sdf.shape)
    return sdf
