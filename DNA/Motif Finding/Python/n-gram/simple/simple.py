# -*- coding:utf-8 -*-
from __future__ import print_function
from collections import Counter
import numpy as np
import Levenshtein
import ngram
import copy
import itertools
import sys
def Read_Truncate_Data(input_file,l_max):
	'''
	1.按行读取数据
	2.按l_max分割每条数据,如果长度小于lmax则忽略不计
	'''
	f = open(input_file,'r')
	lines = f.readlines()
	sequences = []
	countline = 0
	for line in lines:
		if line.startswith('>'):
			pass
		else:
			countline = countline + 1
			string = line.strip()
			for i in range(0,len(string),l_max):
					#print string[i:i+l_max]
				if len(string[i:i+l_max].strip() )== l_max:
					sequences.append(string[i:i+l_max].strip())
	# print len(sequences[0])
	print (sequences)
	return sequences


def motif(sequences,L_Left,L_UP):
	len_motifs_sup = {}
	for i in range(L_Left,L_UP+1):
		motif = Counter() 
		for x in sequences:
			G = ngram.NGram(N = i)
			motif.update(G.ngrams(x))
			len_motifs_sup[i] = motif
	print(len_motifs_sup)
	return len_motifs_sup



def simple(len_motifs_sup,l_max,L_Left,L_UP,epsilon,theta,top_k,output_filename):
	l = L_Left
	N = {}
	
	len_motifs_laplacesup  = copy.deepcopy(len_motifs_sup)
	len_motifs_consolidatesup = copy.deepcopy(len_motifs_laplacesup)

	#len_motifs_laplacesup ={}
	#len_motifs_consolidatesup ={}
	alphabet = 'AGCT'

	while l <= L_UP:
		scale =((l_max- l + 1) * (L_UP - L_Left+1))/epsilon
		allsequence =itertools.product(alphabet,repeat = l)
		Seq_l = len_motifs_sup[l]
		for x in allsequence:
			seql = ''.join(x)
			if seql in Seq_l.keys():
				len_motifs_laplacesup[l][seql] = len_motifs_sup[l][seql] + np.random.laplace(0,scale,1)[0]
			else:
				len_motifs_sup[l][seql] = 0
				len_motifs_laplacesup[l][seql] = np.random.laplace(0,scale,1)[0]
		Seq_x = len_motifs_sup[l]
		for each_seq1 in Seq_x.keys():
			len_motifs_consolidatesup[l][each_seq1]  = 0
			for each_seq2 in Seq_l.keys():
				if 0 <= Levenshtein.hamming(each_seq1, each_seq2) <= theta :
					len_motifs_consolidatesup[l][each_seq1] += len_motifs_laplacesup[l][each_seq2]
	           
		'''
		for w in allsequence:
			seql=''.join(w)
			len_motifs_consolidatesup[l][seql]  = 0
			for y in allsequence:
				seql2=''.join(y)
				if 0 <= Levenshtein.hamming(seql, seql2) <= theta :
					len_motifs_consolidatesup[l][seql] += len_motifs_laplacesup[l][seql2]
		'''
		N = TopN(N,len_motifs_consolidatesup[l],top_k)
		l += 1
        
	f = open(output_filename,'w')
	for i in dict(sorted(N.iteritems(),key=lambda t:t[1],reverse=True)).keys():
		f.write( i + ':' + str(N[i]) + '\n')
	return len_motifs_consolidatesup

def TopN(dicta,dictb,top_K):
	dictMerged = dict( dicta.items() + dictb.items() )
	d = sorted(dictMerged.iteritems(),key=lambda t:t[1],reverse=True)[:top_K]
	return dict(d)

def main(name,L_Left,epsilon,theta,filename):


	l_max = 100
	# L_Left = 4
	# L_UP = 4
	# epsilon = 1
	# theta = 2
	N = 30

	# print "name (name):",
	# name = str(raw_input())
	# print "motif lenght (ML):",
	# L_Left = int(raw_input())
	# print "epsilon (epsilon):",
	# epsilon = int(raw_input())
	# print "theta (theta):",
	# theta = int(raw_input())
	name = name
	L_Left=int(L_Left)
	epsilon=int(epsilon) 
	theta=int(theta)
	filename=filename
	L_UP = L_Left

	input_dir = "data/input/"
	output_dir = "MNSS/result/"
	dataset_name = "realall"
	# out_dataset_name = dataset_name + "N =%d[%d,%d]theta=%deps=%.2f-noise3"%(N,L_Left,L_UP,theta,epsilon)
	out_dataset_name = name
	# input_filename = input_dir + dataset_name + ".fasta"
	input_filename = 'C:\wamp64\www\simple\data\input\\'+filename
	output_filename = 'C:\wamp64\www\simple\MNSS\\result\\' + out_dataset_name  + ".fa"
	
	motif_Seq = Read_Truncate_Data(input_filename,l_max)
	len_motifs_sup=motif(motif_Seq,L_Left,L_UP)



	# print len_motifs_sup
	# print len_motifs_sup[1]
	# return
	len_motifs_consolidatesup= simple(len_motifs_sup,l_max,L_Left,L_UP,epsilon,theta,N,output_filename)
	#print len_motifs_consolidatesup
	#print len_motifs_consolidatesup
if __name__ == "__main__":
    main(name=sys.argv[1],L_Left=sys.argv[2],epsilon = sys.argv[3],theta = sys.argv[4],filename = sys.argv[5]) 
	#GTACGA