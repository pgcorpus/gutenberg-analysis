import numpy as np


def get_dict_words_counts(filename):
    '''
    Read a file and make a dictionary with words and counts.
        word   count
    INPUT:
    - filename
    OUTPUT:
    - dict, {word:count}
    '''
    with open(filename,'r') as f:
        x=f.readlines()
    if x[0] == '\n':
        ## an empty book
        words = []
        counts = []
    else:  
        words = [h.split()[0] for h in x]
        counts = [int(h.split()[1]) for h in x]
    return dict(zip(words,counts))

def get_p12_same_support(
        dict_wc1,
        dict_wc2):
    """
    For two dictionaries {word:count}
    make two arrays p1 and p2 (probabilities) 
    in which the two distributions have the same support.
    INPUT:
    - dict_wc1, dict {word:count}
    - dict_wc2, dict {word:count}
    OUTPUT:
    - arr_p1, array of float - with sum(arr_p1)=1 
    - arr_p2, array of float - with sum(arr_p2)=1
    """
    N1 = sum(list(dict_wc1.values()))
    N2 = sum(list(dict_wc2.values()))
    ## union of all words sorted alphabetically
    words1 = list(dict_wc1.keys())
    words2 = list(dict_wc2.keys())
    words_12 = sorted(list(set(words1).union(set(words2))))
    V = len(words_12)
    arr_p1 = np.zeros(V)
    arr_p2 = np.zeros(V)
    for i_w,w in enumerate(words_12):
        try:
            arr_p1[i_w] = dict_wc1[w]/N1
        except KeyError:
            pass
        try:
            arr_p2[i_w] = dict_wc2[w]/N2
        except KeyError:
            pass
    return arr_p1,arr_p2

