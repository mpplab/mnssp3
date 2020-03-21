import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def approximate_error(pfm, n_occur):
    """Calculate approximate error for small count motif information content

    Parameters
    ----------
    pfm: dict
        {'A': [0.1,0.3,0.2], 'T':[0.3,0.1,0.2], 'G': [0.1,0.3,0.3], 'C':[0.5,0.3,0.3]}
    n: int
        Number of sites

    Returns
    -------
    approx_error: float
        Approx error


    """

    bases = list(pfm.keys())
    approx_error = (len(bases) - 1) / (2 * np.log(2) * n_occur)
    #print(approx_error)
    return approx_error


def exact_error(pfm, n):
    """Calculate exact error, using multinomial(na,nc,ng,nt)"""
    # Super Slow. O(n^3)
    bases = list(pfm.keys())
    na = sum(motif.counts['A'])
    n = na
    nc = 0
    ng = 0
    nt = 0
    done = False
    exact_error = 0
    while not done:
        print((na, nc, ng, nt))
        exact_error += sum(
            [-p * np.log2(p) for p in [na / n, nc / n, ng / n, nt / n]])
        if nt <= 0:
            # iterate inner loop
            if ng > 0:
                # g => t
                ng = ng - 1
                nt = nt + 1
            elif nc > 0:
                # c -> g
                nc = nc - 1
                ng = ng + 1
            else:
                # a->c
                na = na - 1
                nc = nc + 1
        else:
            if ng > 0:
                # g => t
                ng = ng - 1
                nt = nt + 1
            elif nc > 0:
                # c => g; all t -> g
                nc = nc - 1
                ng = nt + 1
                nt = 0
            elif na > 0:
                # a => c; all g,t -> c
                nc = nt + 1
                na = na - 1
                nt = 0
            else:
                done = True
    return exact_correction


def calc_info_matrix(pfm, n_occur, correction_type='approx'):
    """Calculate information matrix with small sample correction"""
    bases = list(pfm.keys())
    n = len(list(pfm.values())[0])
    if correction_type == 'approx':
        error = approximate_error(pfm, n_occur)
    else:
        error = exact_error(pfm)
    shannon_entropy = [
        sum([-pfm[b][l] * np.nan_to_num(np.log2(pfm[b][l])) for b in bases])
        for l in range(0, n)
    ]
    #print (pd.DataFrame(shannon_entropy))
    info_matrix = [
        2 + sum([pfm[b][l] * np.nan_to_num(np.log2(pfm[b][l])) for b in bases])
        for l in range(0, n)
    ]
    #info_matrix[info_matrix<0] = 0
    return info_matrix


def calc_relative_information(pfm, n_occur, correction_type='approx'):
    """Calculate relative information matrix"""
    bases = list(pfm.keys())
    if correction_type == 'approx':
        info_matrix = calc_info_matrix(pfm, n_occur)
    else:
        info_matrix = calc_info_matrix(pfm, 'exact')
    #print('Info matrix: ')
    #print(pd.DataFrame(info_matrix))
    relative_info = {
        base: [
            np.nan_to_num(prob * info)
            for prob, info in zip(pfm[base], info_matrix)
        ]
        for base in bases
    }
    return relative_info


def calc_pfm(counts):
    """Calculat pfm given counts"""
    df = pd.DataFrame(counts)
    s = df.T.sum()
    df = (df.T / s).T
    df = df.fillna(0)
    return df.to_dict(orient='list'), s.tolist()[0]


def pfm_to_tuple(pfm):
    """Convert a dict of pwm basewise to a list of tuples"""
    motif_pwm = []
    for i in range(0, len(pfm[list(pfm.keys())[0]])):
        scores = []
        for b in bases:
            try:
                value = pfm[b][i]
            except KeyError:
                value = 0
            scores.append((b, value))

        #scores = [(b, pfm[b][i]) for b in bases]

        scores.sort(key=lambda t: t[1])
        motif_pwm.append(scores)
    return motif_pwm


def load_motif(infile=None, counts=None):
    """Load motifs file
    """
    if not counts:
        A, C, G, T = np.loadtxt(infile, unpack=True)
        # Add psuedocounts
        A = np.array(A)  #+ 1
        C = np.array(C)  #+ 1
        G = np.array(G)  #+ 1
        T = np.array(T)  #+ 1
        counts = OrderedDict({'A': A, 'C': C, 'G': G, 'T': T})
    pfm, n_occur = calc_pfm(counts)
    ic = calc_relative_information(pfm, n_occur)

    motif_scores = []
    motif_scores_agg = []
    for i in range(0, len(counts['A'])):
        scores = [(b, ic[b][i]) for b in bases]
        scores.sort(key=lambda t: t[1])
        motif_scores.append(scores)
        motif_scores_agg.append(np.sum([ic[b][i] for b in bases]))
    return motif_scores, motif_scores_agg, pfm, counts


def aggregate_motif_ic(ic):
    """Return per base motif information content"""
    motif_scores_agg = []
    for position in ic:
        motif_scores_agg.append(sum([x[1] for x in position]))
    return motif_scores_agg


def max_motif_ic(ic):
    """"Return per base max info"""
    bases = ['A', 'C', 'G', 'T']
    max_bases = []
    max_ic = []
    for postion in ic:
        max_base, m_ic = position[-1]
        max_ic.append(m_ic)
        max_bases.append(max_base)

    return max_ic, max_base


def _set_spine_position(spine, position):
    """
    Set the spine's position without resetting an associated axis.
    As of matplotlib v. 1.0.0, if a spine has an associated axis, then
    spine.set_position() calls axis.cla(), which resets locators, formatters,
    etc.  We temporarily replace that call with axis.reset_ticks(), which is
    sufficient for our purposes.

    License: MIT
    https://github.com/mwaskom/seaborn/blob/0beede57152ce80ce1d4ef5d0c0f1cb61d118375/seaborn/utils.py#L265
    """
    axis = spine.axis
    if axis is not None:
        cla = axis.cla
        axis.cla = axis.reset_ticks
    spine.set_position(position)
    if axis is not None:
        axis.cla = cla


def despine(fig=None,
            ax=None,
            top=True,
            right=True,
            left=False,
            bottom=False,
            offset=None,
            trim=False):
    """Remove the top and right spines from plot(s).
    Parameters
    ----------

    fig : matplotlib figure, optional
        Figure to despine all axes of, default uses current figure.
    ax : matplotlib axes, optional
        Specific axes object to despine.
    top, right, left, bottom : boolean, optional
        If True, remove that spine.
    offset : int or dict, optional
        Absolute distance, in points, spines should be moved away
        from the axes (negative values move spines inward). A single value
        applies to all spines; a dict can be used to set offset values per
        side.
    trim : bool, optional
        If True, limit spines to the smallest and largest major tick
        on each non-despined axis.

    Returns
    -------
    None

    License
    -------
    MIT

    This is borrowed from here: https://github.com/mwaskom/seaborn/blob/0beede57152ce80ce1d4ef5d0c0f1cb61d118375/seaborn/utils.py#L184
     """
    # Get references to the axes we want
    if fig is None and ax is None:
        axes = plt.gcf().axes
    elif fig is not None:
        axes = fig.axes
    elif ax is not None:
        axes = [ax]

    for ax_i in axes:
        for side in ["top", "right", "left", "bottom"]:
            # Toggle the spine objects
            is_visible = not locals()[side]
            ax_i.spines[side].set_visible(is_visible)
            if offset is not None and is_visible:
                try:
                    val = offset.get(side, 0)
                except AttributeError:
                    val = offset
                _set_spine_position(ax_i.spines[side], ('outward', val))

        # Set the ticks appropriately
        if bottom:
            ax_i.xaxis.tick_top()
        if top:
            ax_i.xaxis.tick_bottom()
        if left:
            ax_i.yaxis.tick_right()
        if right:
            ax_i.yaxis.tick_left()

        if trim:
            # clip off the parts of the spines that extend past major ticks
            xticks = ax_i.get_xticks()
            if xticks.size:
                firsttick = np.compress(xticks >= min(ax_i.get_xlim()),
                                        xticks)[0]
                lasttick = np.compress(xticks <= max(ax_i.get_xlim()),
                                       xticks)[-1]
                ax_i.spines['bottom'].set_bounds(firsttick, lasttick)
                ax_i.spines['top'].set_bounds(firsttick, lasttick)
                newticks = xticks.compress(xticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_xticks(newticks)

            yticks = ax_i.get_yticks()
            if yticks.size:
                firsttick = np.compress(yticks >= min(ax_i.get_ylim()),
                                        yticks)[0]
                lasttick = np.compress(yticks <= max(ax_i.get_ylim()),
                                       yticks)[-1]
                ax_i.spines['left'].set_bounds(firsttick, lasttick)
                ax_i.spines['right'].set_bounds(firsttick, lasttick)
                newticks = yticks.compress(yticks <= lasttick)
                newticks = newticks.compress(newticks >= firsttick)
                ax_i.set_yticks(newticks)
