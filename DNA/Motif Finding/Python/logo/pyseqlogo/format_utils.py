


from Bio.Align import AlignInfo
from Bio.Seq import Seq
from Bio import motifs
from Bio import SeqIO
from Bio import AlignIO

from .expected_frequencies import naive_freq_tables

import pandas as pd
import numpy as np


def count_to_pfm(counts):
    df = pd.DataFrame(counts)
    total_counts = df.T.sum()
    df = (df.T / total_counts).T
    df = df.fillna(0)
    return (df.to_dict(orient='list'), total_counts.tolist()[0])


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
    return approx_error


def exact_error(pfm, n):
    """Calculate exact error, using multinomial(na,nc,ng,nt)"""
    # Super Slow. O(n^3)
    bases = list(pfm.keys())
    na = sum(pfm[bases[0]])
    n = na
    nc = 0
    ng = 0
    nt = 0
    done = False
    exact_error = 0
    while not done:
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
    return exact_error


def calc_info_matrix(pfm, n_occur, correction_type='approx', seq_type='dna'):
    """Calculate information matrix with small sample correction"""
    bases = list(pfm.keys())
    n = len(list(pfm.values())[0])
    if correction_type == 'approx':
        error = approximate_error(pfm, n_occur)
    else:
        error = exact_error(pfm)
    if seq_type == 'dna':
        shannon_entropy = [
            sum([
                -pfm[b][l] * np.nan_to_num(np.log2(pfm[b][l])) for b in bases
            ]) for l in range(0, n)
        ]
        info_matrix = [
            2 + sum(
                [pfm[b][l] * np.nan_to_num(np.log2(pfm[b][l])) for b in bases])
            for l in range(0, n)
        ]
    elif seq_type == 'aa':
        shannon_entropy = [
            sum([
                -pfm[b][l] * np.nan_to_num(np.log20(pfm[b][l])) for b in bases
            ]) for l in range(0, n)
        ]
        info_matrix = [
            2 + sum([
                pfm[b][l] * np.nan_to_num(np.log20(pfm[b][l])) for b in bases
            ]) for l in range(0, n)
        ]
    else:
        # Custom
        logscale = np.log(len(bases))
        shannon_entropy = [
            sum([
                -pfm[b][l] * np.nan_to_num(np.log(pfm[b][l]) / logscale)
                for b in bases
            ]) for l in range(0, n)
        ]
        info_matrix = [
            2 + sum([
                pfm[b][l] * np.nan_to_num(np.log(pfm[b][l]) / logscale)
                for b in bases
            ]) for l in range(0, n)
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
    relative_info = {
        base: [
            np.nan_to_num(prob * info)
            for prob, info in zip(pfm[base], info_matrix)
        ]
        for base in bases
    }
    return relative_info


def read_alignment(infile, data_type='fasta', seq_type='dna', pseudo_count=1):
    """Read alignment file as motif

    Parameters
    ----------

    infile: str
        Path to input alignment file

    data_type: str
        'fasta', 'stockholm', etc/. as supported by Bio.AlignIO

    seq_type: str
        'dna', 'rna' or 'aa'

    pseudo_count: int
        psuedo counts to add before calculating information cotent

    Returns
    -------

    (motif, information_content) : tuple
        A motif instance followd by total informatio content of the motif

    """
    alignment = AlignIO.read(infile, data_type)
    data = []
    for aln in alignment:
        data.append([x for x in str(aln.seq)])
    df = pd.DataFrame(data)
    df_counts = df.apply(pd.value_counts, 0)
    total = df_counts[[0]].sum()
    df_counts = df_counts[df_counts.index != '-']
    # Remove - from counts
    counts_dict = df_counts.to_dict(orient='index')
    counts = {}
    for key, val in counts_dict.items():
        counts[key] = list(val.values())
    return counts, total
    """
    summary_align = AlignInfo.SummaryInfo(alignment)
    if seq_type == 'dna':
        info_content = summary_align.information_content(e_freq_table = naive_freq_tables['dna'],
                                                         chars_to_ignore = ['N'],
                                                         pseudo_count = pseudo_count)
    elif seq_type == 'rna':
        info_content = summary_align.information_content(e_freq_table = naive_freq_tables['rna'],
                                                         chars_to_ignore = ['N'],
                                                         pseudo_count = pseudo_count)
    else:
        info_content = summary_align.information_content(e_freq_table = naive_freq_tables['aa'],
                                                         pseudo_count = pseudo_count)
    motif = create_motif_from_alignment(alignment)
    return (motif, summary_align.ic_vector)
    """


def create_motif_from_alignment(alignment):
    """Create motif form an alignment object

    Parameters
    ----------
    alignment : Bio.AlignIO
        Bio.AligIO input

    Returns
    -------
    motif : Bio.motifs object

    """
    records = [record.seq for record in alignment]
    motif = motifs.create(records)
    return motif


def format_matrix(matrix):
    scores = []
    for i in range(0, len(matrix[list(matrix.keys())[0]])):
        row_scores = [(b, matrix[b][i]) for b in list(matrix.keys())]
        row_scores.sort(key=lambda t: t[1])
        scores.append(row_scores)
    return scores


def process_data(data, data_type='counts', seq_type='dna'):
    if data_type == 'counts':
        pfm, total = count_to_pfm(data)
        ic = calc_relative_information(pfm, total)
    elif data_type == 'probability':
        pfm = data
        ic = calc_relative_information(pfm, 10)
    elif data_type in ['fasta', 'stockholm']:
        #motif, ic = read_alignment(data, data_type, seq_type)
        #pfm = motif.counts.normalize(pseudocounts=1)
        data, total = read_alignment(data, data_type, seq_type)
        pfm, _ = count_to_pfm(data)
        ic = calc_relative_information(pfm, total)
    elif data_type in [
            'alignace', 'meme', 'mast', 'transfac', 'pfm', 'sites', 'jaspar'
    ]:
        if data_type in ['jaspar', 'transfac']:
            motif = motifs.parse(open(data, 'r'), data_type.upper())[0]
            pfm = dict(motif.counts.normalize())
            total = sum(list(motif.counts.values())[0])
        else:
            motif = motifs.read(open(data, 'r'), data_type)
            try:
                pfm = motif.counts.normalize(psuedocounts=1)
            except:
                pfm = motif.counts.normalize()
            total = motif.counts
        ic = calc_relative_information(pfm, total)
    return (format_matrix(pfm), format_matrix(ic))
