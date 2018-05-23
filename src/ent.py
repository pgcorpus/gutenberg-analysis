"""Functions to compute generalized entropies."""
import numpy as np


def H_alpha(arr_p, alpha=1.0):
    r"""
    Calculate generalized entropy of order-alpha.

    $$
    H_{\alpha}(\vec{p}) = \frac{1}{1-\alpha}( \sum_i p_i^{\alpha} - 1  )
    $$
    See [Tsallis entropy](https://en.wikipedia.org/wiki/Tsallis_entropy)

    Parameters
    ----------
    arr_p : np.array
        Normalized probability distribution.
    alpha : float
        Order of the entropy. The default alpha=1 gives
        the standard Boltzmann-Shannon-Gibbs entropy.

    Returns
    -------
    H_alpha : float
        The alpha-order entropy.

    Notes
    -----
    Two special cases are handled separately:
    - $alpha=0$; if $p_i=0$: $p_i^0=0$ and $p_i>0$: p_i^0=1
    - $alpha=1$; $H = -\sum_i p_i log(p_i)$ and $0*log(0)=0$

    """
    # consider only entries with p>0
    arr_p_pos = np.array([p for p in arr_p if p > 0])
    H = 0.0
    if alpha == 0.0:
        H = len(arr_p_pos) - 1
    elif alpha == 1.0:
        H = -np.sum(arr_p_pos*np.log(arr_p_pos))
    else:
        H = 1.0/(1.0-alpha)*(np.sum(arr_p_pos**alpha) - 1.0)
    return H


def D_alpha_max(H1, H2, pi1, pi2, alpha=1.0):
    r"""
    Compute maximum Jensen-Shanon divergence.

    This function compute the maximum Jensen-Shanon divergence of two prob
    distributions p1 and p2 with entropies H1 and H2 and weights pi1 and pi2.
    The maximum jsd is obtained by assuming the support of both distributions
    is disjunct.

    For more information see:
    Gerlach, Font-Clos, Altmann, Phys. Rev. X 6 (2016) 021009
    https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.021009

    Parameters
    ----------
    H1, H2 : float
        alpha-entropy of p1, p2.

    pi1, pi2 : float
        Weight given to p1, p2.

    alpha : float
        Order of the entropy. The default alpha=1 gives
        the standard Boltzmann-Shannon-Gibbs entropy.

    Returns
    -------
    D_max : float
        Maximum JSD.

    """
    D_max = 0.0
    if alpha == 1.0:
        D_max = -pi1*np.log(pi1)-pi2*np.log(pi2)
    else:
        D_max = (pi1**alpha-pi1)*H1 + \
                (pi2**alpha-pi2)*H2 + \
                1.0/(1.0-alpha)*(pi1**alpha+pi2**alpha-1)
    return D_max


def D_alpha(arr_p1, arr_p2, alpha=1.0, pi1=0.5, normalized=False):
    r"""
    Compute generalized Jensen-Shannon divergence.

    This function computes the generalized JSD, quantifying the divergence
    between probability distributions p1 and p2, as proposed in:

    Gerlach, Font-Clos, Altmann, Phys. Rev. X 6 (2016) 021009
    https://journals.aps.org/prx/abstract/10.1103/PhysRevX.6.021009

    arr_p1, arr_p2 : np.array
        Normalized probability distributions.
    alpha : float
        Order of the entropy. The default alpha=1 gives
        the standard Boltzmann-Shannon-Gibbs entropy.
    pi1 : float
        Weight given to p1. The weight for p2 is 1-pi1.
    normalized : bool (False)
        If True, return normalized version of alpha-JSD.

    Returns
    -------
    JSD : float
        The order-alpha JSD.

    Notes
    -----
    Assumes that $p1$ and $p2$ are defined over the *same* support, i.e.
    for any index $i$ the probabilities $p1_i$ and $p2_i$ refer to the same
    symbol. If, for example a symbol $j$ only appears in $p1$, then $p1_j>0$
    and $p2_j=0$ (and vice versa).

    """
    pi2 = 1.0-pi1

    H_1 = H_alpha(arr_p1, alpha=alpha)
    H_2 = H_alpha(arr_p2, alpha=alpha)
    arr_p12 = pi1*arr_p1 + pi2*arr_p2
    H_12 = H_alpha(arr_p12, alpha=alpha)

    D = H_12 - pi1*H_1 - pi2*H_2

    if normalized is False:
        norm = 1.0
    else:
        norm = D_alpha_max(H_1, H_2, pi1, pi2, alpha=alpha)
    D /= norm
    return D
