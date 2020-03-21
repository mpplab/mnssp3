import os
import warnings

import numpy as np
import pyBigWig


class WigReader(object):
    """Class for reading and querying wigfiles."""

    def __init__(self, wig_location):
        """
        Parameters
        ---------
        wig_location : string
                       Path to wig file

        """
        self.wig_location = wig_location
        try:
            self.wig = pyBigWig.open(self.wig_location)
        except Exception as e:
            raise Exception('Error reading wig file {} : {}'.format(
                os.path.abspath(self.wig_location), e))

    def query(self, intervals):
        """ Query regions for scores.

        Parameters
        ----------
        intervals : list(tuple)
                    A list of tuples with the following format:
                        (chr, chrStart, chrEnd, strand)

        Returns
        -------
        scores : array_like
                 A numpy array containing scores for each tuple


        .. currentmodule:: .WigReader
        .. autosummary::
            .WigReader

        """
        scores = []
        chrom_lengths = self.get_chromosomes
        for chrom, chrom_start, chrom_end, strand in intervals:
            if chrom not in list(chrom_lengths.keys()):
                warnings.warn(
                    'Chromosome {} does not appear in the bigwig'.format(
                        chrom), UserWarning)
                continue

            chrom_length = chrom_lengths[chrom]
            if int(chrom_start) > chrom_length:
                raise Exception(
                    'Chromsome start point exceeds chromosome length: {}>{}'.
                    format(chrom_start, chrom_length))
            elif int(chrom_end) > chrom_length:
                raise Exception(
                    'Chromsome end point exceeds chromosome length: {}>{}'.
                    format(chrom_end, chrom_length))
            score = self.wig.values(chrom, int(chrom_start), int(chrom_end))
            if strand == '-':
                score.reverse()
            scores.append(score)
        return np.array(scores)

    @property
    def get_chromosomes(self):
        """Return list of chromsome and their sizes
        as in the wig file.

        Returns
        -------
        chroms : dict
                 Dictionary with {"chr": "Length"} format


        .. currentmodule:: .WigReader
        .. autosummary::
            .WigReader
        """
        return self.wig.chroms()
