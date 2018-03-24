import numpy as np
from collections import Counter
import random
import os,sys

from ent import D_alpha
from data_io import get_dict_words_counts
from data_io import get_p12_same_support


def jsdalpha(
        f1,
        f2,
        alpha=1.0,
        normalized=False,
        weights=False
    ):
    """
    Calculate the generalized Jensen-Shannon-divergence between two prob-distributions
    p1 and p2 as described in 
        Gerlach, Font-Clos, Altmann, Phys. Rev. X 6 (2016) 021009
        https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.021009


    INPUT:
    - f1, filename
    - f2, filename
        those files contain the counts in the format:
            word1   count(word1) \n
            word2   count(word2) \n
            ...
    optional:
    - alpha, float or array (default:1.0); alpha=1 corresponds to the 
        normal Jensen-Shannon divergence
    - normalized, bool (default:False); normalize the JSD by the maximum possible JSD
    - weights, bool (default:False); if True assign weights according to number of tokens.
    OUTPUT:
    - JSD-alpha, same shape as alpha
    """
    ## For each file obtain dictionary {word:count}
    dict_wc1 = get_dict_words_counts(f1)
    dict_wc2 = get_dict_words_counts(f2)
    ## Make two array containing the probabilities p1 and p2 (SAME SUPPORT!)
    arr_p1, arr_p2 = get_p12_same_support(dict_wc1,dict_wc2)
    ## Weighting of the two distributions
    if weights == False:
        pi1 = 0.5
    else:
        N1 = sum(list(dict_wc1.values()))
        N2 = sum(list(dict_wc2.values()))
        pi1 = N1/float(N1+N2)

    ## alpha-JSD
    if isinstance(alpha, (int,float)):
        jsd = D_alpha(arr_p1,arr_p2,alpha=alpha,pi1=pi1,normalized=normalized)
    elif isinstance(alpha,(list,np.ndarray)):
        jsd = []
        for alpha_tmp in alpha:
            jsd_tmp = D_alpha(arr_p1,arr_p2,alpha=alpha_tmp,pi1=pi1,normalized=normalized)
            jsd += [jsd_tmp]
    return jsd





def jsdalpha_null(
        f1,
        f2,
        alpha=1.0,
        normalized=False,
        weights=False,
        n_rep=1,
        perc = [2.5,97.5]
    ):
    """
    Calculate generalized JSD expected from a random null model.
    That is, we assume that both texts were generated from the same 'source'.
    In practice we simply shuffle all tokens across the two texts and measure the
    JSD which simply comes from the finite-size effect.

    We repeat n_rep times and report average and confidence interval.

   INPUT:
    - f1, filename
    - f2, filename
        those files contain the counts in the format:
            word1   count(word1) \n
            word2   count(word2) \n
            ...
    optional:
    - alpha, float or array (default:1.0); alpha=1 corresponds to the 
        normal Jensen-Shannon divergence
    - normalized, bool (default:False); normalize the JSD by the maximum possible JSD
    - weights, bool (default:False); if True assign weights according to number of tokens.
    - n_rep, int (default:10) number of random realizations of null model
    - perc, list of floats (default [2.5,97.5]); percentiles, .e.g 5% confidence interval

    OUTPUT:
    - jsd_null_mu, avg of jsd_null over n_rep realizations; same shape as alpha
    - jsd_null_perc, percentiles of jsd_null over n_rep realizations; 
        list of len=len(perc); same shape as alpha 

    """


    if isinstance(alpha, (int,float)):
        arr_jsd_null = np.zeros(n_rep)
    elif isinstance(alpha,(list,np.ndarray)):
        arr_jsd_null = np.zeros((n_rep,len(alpha)))

    ## For each file obtain dictionary {word:count}
    dict_wc1 = get_dict_words_counts(f1)
    dict_wc2 = get_dict_words_counts(f2)

    ## construct list o tokens which can be shuffled
    N1 = sum(list(dict_wc1.values()))
    N2 = sum(list(dict_wc2.values()))

    list_tokens =[]
    for w,n in dict_wc1.items():
        list_tokens +=[w]*n
    for w,n in dict_wc2.items():
        list_tokens +=[w]*n


    for i_n_rep in range(n_rep):
        random.shuffle(list_tokens)
        list_tokens_1 = list_tokens[:N1]
        list_tokens_2 = list_tokens[N1:]

        c1 = Counter(list_tokens_1)
        c2 = Counter(list_tokens_2)

        f1_tmp ='f1_tmp'
        with open(f1_tmp,'w') as f:
            for w,n in c1.items():
                f.write('%s \t %s \n'%(w,n))
        f2_tmp ='f2_tmp'
        with open(f2_tmp,'w') as f:
            for w,n in c2.items():
                f.write('%s \t %s \n'%(w,n))
        arr_jsd_null_tmp = jsdalpha(f1_tmp,f2_tmp,alpha=alpha,weights=weights,normalized=normalized)
        os.system('rm -f %s %s'%(f1_tmp,f2_tmp))
        arr_jsd_null[i_n_rep] = arr_jsd_null_tmp

    arr_jsd_null_mu = np.mean(arr_jsd_null,axis=0)
    arr_jsd_null_err = np.percentile(arr_jsd_null,q=perc,axis=0)
    return arr_jsd_null_mu, arr_jsd_null_err












# def jsd_null(
#         f1,
#         f2,
#         alpha=1,
#         n = 1,
#         normalized=False,
#         weights=False
#     ):
#     jsd = 0.0
#     return jsd

## just create random shuffle and write two temp-files