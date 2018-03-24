
import sys, os
import numpy as np
import argparse
src_dir = 'src/'
sys.path.append(src_dir)
from jsd import jsdalpha
from jsd import jsdalpha_null

##############################################################################
def jsda(
    filename1 = None,
    filename2 = None,
    alpha = 1.0,
    weights= False,
    normalized = False,
    n_rep = 0
    ):
    jsd_alpha = jsdalpha(filename1,filename2,alpha=alpha,weights=weights,normalized=normalized)
    print('For alpha = %s, normalized =  %s, weighted = %s:'%(alpha,normalized, weights))
    print('')
    print('JSD = %s'%(jsd_alpha))

    if n_rep>0:
        jsd_null_mu,jsd_null_perc = jsdalpha_null(filename1,filename2,alpha=alpha,weights=weights,normalized=normalized,n_rep=n_rep)
        print('')
        print('Random null model with %s realization yields:'%(n_rep))
        print('JSD null average: %s'%(jsd_null_mu))
        print('JSD null 5-percent confidence interval: %s '%(jsd_null_perc))

if __name__=='__main__':

    parser = argparse.ArgumentParser("Jensen-Shannon-alpha divergence.")
    parser.add_argument(
        "-f1", "--filename1",
        help="Words-Counts File #1",
        default='data/PG299_counts.txt',
        type=str)
    parser.add_argument(
        "-f2", "--filename2",
        help="Words-Counts File #2",
        default='data/PG304_counts.txt',
        type=str)
    parser.add_argument(
        "-a", "--alpha",
        help="alpha-parameter for JSD-alpha (default:1.0 == normal Jensen-Shannon divergence)",
        default=1.0,
        type=float)
    parser.add_argument(
        "-w", "--weights",
        help="Weights for each distribution according to number of tokens \
        (default:False == same weight for each independent of # of tokens)",
        default=False,
        type=bool)
    parser.add_argument(
        "-n", "--normalized",
        help="Normalize JSD-alpha (default:False)",
        default=False,
        type=bool)

    parser.add_argument(
        "-s", "--sampling",
        help="# random realizations for JSD-alpha from random null model (default: 0) ",
        default=0,
        type=int)

    args = parser.parse_args()

    ## do the hsbm on a corpus
    jsda(    
        filename1 = args.filename1,
        filename2 = args.filename2,
        alpha = args.alpha,
        weights= args.weights,
        normalized = args.normalized,
        n_rep = args.sampling
        )
