from Bio.Alphabet import IUPAC
from Bio.SubsMat import FreqTable

dna_letters = IUPAC.unambiguous_dna.letters
rna_letters = IUPAC.unambiguous_rna.letters
protein_letters = IUPAC.protein.letters

dna_naive_freq = {k: 0.25 for k in dna_letters}
rna_naive_freq = {k: 0.25 for k in rna_letters}
aa_naive_freq = {k: 0.05 for k in protein_letters}

dna_naive_freq_table = FreqTable.FreqTable(dna_naive_freq, FreqTable.FREQ,
                                           IUPAC.unambiguous_dna)

rna_naive_freq_table = FreqTable.FreqTable(rna_naive_freq, FreqTable.FREQ,
                                           IUPAC.unambiguous_rna)

aa_naive_freq_table = FreqTable.FreqTable(aa_naive_freq, FreqTable.FREQ,
                                          IUPAC.protein)

naive_freq_tables = {
    'aa': aa_naive_freq_table,
    'dna': dna_naive_freq_table,
    'rna': rna_naive_freq_table
}
