# Standardized Project Gutenberg Corpus Tutorial
This repository contains some example notebooks that illustrate how to use the Standardized Project Gutenberg Corpus (SPGC) and reproduce the analysis presented in the manuscript

[A standardized Project Gutenberg corpus for statistical analysis of natural language and quantitative linguistics](https://arxiv.org/abs/1812.08092)  
M. Gerlach, F. Font-Clos, arXiv:1812.08092, Dec 2018

The data is not included in this repository, but you can easily get in in two ways:
1. Run the [code](https://github.com/pgcorpus/gutenberg) yourself to get the latest version of the corpus, which will include all books in PG as of today.
2. Download the [pre-processed data](https://doi.org/10.5281/zenodo.2422560) to get exactly the same books we used in the manuscript (those available up to July 18, 2018)


We assume that you have the two folders at the same level in your folder-hierarchy:
1. `gutenberg/` in which you have the data.
2. `gutenberg-analysis/`   with the code in this repository.


You find example notebooks how to access and analyze the data in `notebooks_tutorial/`.
- [Tutorial 01: Loading a book and metadata queries](notebooks_tutorial/tutorial_01_how-to-read-a-book-metadata.ipynb)
has some basic examples on how to easily load a single book; or how to query the metadata to get a selection of books, e.g. from the same author.
- more will be added.

You find the notebooks we used to create the figures in our manuscript in `notebooks_manuscript`.


