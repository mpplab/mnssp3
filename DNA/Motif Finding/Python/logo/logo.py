import math

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import dmslogo
from dmslogo.colorschemes import CBPALETTE
import string
import random
import tempfile
import urllib.request
import numpy
from pyseqlogo.pyseqlogo import draw_logo, setup_axis
import matplotlib.ticker as ticker
import sys

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 500)

msa = list()

class case:
    def __init__(self, key, H):
        self.key = key
        self.H = H
    def __repr__(self):
        return repr((self.key, self.H))
    def dic(self):
        return (self.key, self.H)


def entropy_DNA(positions):
    # allEntropies = {}
    # BA_all = []
    # BT_all = []
    # BC_all = []
    # BG_all = []
    # BA,BT,BC,BG is the height of the block at each position/column

    Loc_all = []
    for position in positions:

        countA = position.count('A')
        countT = position.count('T')
        countC = position.count('C')
        countG = position.count('G')

        pA = countA/len(msa) #relative probability
        pT = countT/len(msa)
        pC = countC/len(msa)
        pG = countG/len(msa)

        HA = 0
        HT = 0
        HC = 0
        HG = 0

        if countA != 0:
            HA = -pA * math.log2(pA) #shannon entropy
        if countT != 0:
            HT = -pT * math.log2(pT)
        if countC != 0:
            HC = -pC * math.log2(pC)
        if countG != 0:
            HG = -pG * math.log2(pG)


        totH = HA + HT + HC + HG #total Entropy at each position for each nucleotid
        e = (1 / math.log(2)) * 3 / (2 * len(msa))  # approximation for the small-sample correction
                                                    #works only if number of sequences >=30
        e = 0
        R = math.log2(4) - (totH + e) #Total block height at each position #(R = math.log2(4) - (totH + e))
        BA = pA * R # Block height of A
        BT = pT * R
        BC = pC * R
        BG = pG * R

        list = [case('C', BC), case('T', BT), case('A', BA), case('G', BG)]

        list = sorted(list, key=lambda case: case.H)
        # print(list)

        list2 = []
        for c in list:
            list2.append(c.dic())
        print(list2)
        Loc_all.append(list2)


        #print('R',R)
        # BA_all.append(BA) #rolling over each sequence at this position
        # BT_all.append(BT)
        # BC_all.append(BC)
        # BG_all.append(BG)
        #end of for-loop
        #end of entropy function
        # BA_all.append(countA)  # rolling over each sequence at this position
        # BT_all.append(countC)
        # BC_all.append(countG)
        # BG_all.append(countT)

    #print(totalEntropy)
    # allEntropie
    #
    # allEntropies.append(BA_all)
    # allEntropies.append(BT_all)
    # allEntropies.append(BC_all)
    # allEntropies.append(BG_all)
    # allEntropies = {'A':BA_all,'C':BT_all,'G':BC_all,'T':BG_all}
    return Loc_all


def main(name, file):

    DNA_letters = ['A', 'T', 'C', 'G']
    Amino_acids = ['D', 'P', 'N', 'W', 'S', 'C', 'H', 'K', 'M', 'R', 'V', 'A', 'L', 'G', 'Y', 'E', 'Q', 'I', 'F', 'T']

    # filename = input('Enter MSA file name: ')
    filename = file
    file = open(filename, 'r')

    for line in file:
        if line.startswith('>'):
            pass
        else:
            line = line.replace('\n', '')
            if line != '':
                msa.append(line)
        # line = line.replace('\n', '')
        # if line != '':
        #    msa.append(line)
    print('msa', msa)

    # length = len(msa[0])

    positions = list(zip(*msa))
    print(positions)

    for position in positions:
        str = ''.join(position)  # string from tuple to be able to 'count'
        # print(str.count('A'))

    S = entropy_DNA(positions)
    print(S)

    matplotlib.use('TkAgg')
    plt.rcParams['figure.dpi'] = 300
    fig, axarr = draw_logo(S, data_type='bits', nrow=1, ncol=1)
    # fig.tight_layout()
    plt.savefig('C:/wamp64/www/MNSS3/MNSS/result/' + name + '.png', dpi=300, bbox_inches='tight')
    # plt.show()

if __name__ == "__main__":
    main(name=sys.argv[1],file=sys.argv[2])




