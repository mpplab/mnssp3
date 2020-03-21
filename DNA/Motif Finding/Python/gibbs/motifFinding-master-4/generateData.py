"""
	Generate dataset for CSS 466 motif finding project 
	Team members: Shriyaa Mittal, Zahra Shamsi and Melanie Paige Muller
"""

import sys
import random
import time
import os

## Constants
nuc = ['A','C','G','T']
freq = [0.25,0.25,0.25,0.25]
filename='uniform_bg_ICPC_to_p.txt'
sequence_filename='sequences.fa'
site_filename='sites.txt'
folder='dataset'

def generate_seq(SL,freq):
	seq=[]
	for i in range(0,SL):
		random.seed(time.time())
		x=random.random()
		if (x<freq[0]):
			seq.append(nuc[0])
		elif (x<freq[0]+freq[1]):
			seq.append(nuc[1])
		elif (x<freq[0]+freq[1]+freq[2]):
			seq.append(nuc[2])
		else:
			seq.append(nuc[3])
	return ''.join(seq)


def plant_motifs_in_seqs(seq_to_modify,motifs,ML,SL):
	random.seed(time.time())
	pos=random.randrange(0,SL-ML)
	motif_num=random.randrange(0,SC)
	new_seq=seq_to_modify[:pos]+motifs[motif_num]+seq_to_modify[pos+ML:]
	return new_seq,pos
	

if __name__ == "__main__":

	## Inputs
	if (len(sys.argv)>0 and len(sys.argv)<5):
		print "Command line usage: python benchmark.py <ICPC -- value [0,2] with maximum 2 significant digits> <ML -- positive integer> <SL -- postive integer> <SC --positive integer>"
		print "Information content per column (ICPC):",
		ICPC = float(raw_input())
		print "motif lenght (ML):",
		ML = int(raw_input())
		print "sequence length (SL):",
		SL = int(raw_input())
		print "sequence count (SC):",
		SC = int(raw_input())
	else:
		ICPC = float(sys.argv[1])
		ML = int(sys.argv[2])
		SL = int(sys.argv[3])
		SC = int(sys.argv[4])
	sum_freq=sum(freq)
	if sum_freq != 1:
		raise Exception, 'Sum of frequency of nucleotides is not 1.'
	if ML>SL:
		raise Exception, 'Motif length is greater than sequence length.'
	if (ICPC<0 or ICPC>2 or ML<=0 or SL<=0 or SC<=0 or len(str(ICPC))>4):
		raise Exception, 'Incorrect input values.\n<ICPC -- value [0,2] with maximum 2 significant digits> <ML -- positive integer> <SL -- postive integer> <SC --positive integer>'

	## Create dataset folder
	dataset_folder=folder
	cmd='mkdir '+dataset_folder
	os.system(cmd)

	## Generate SC random sequences of length SL and store in list, seqs
	seqs=[]
	for i in range(0,SC):
		temp=generate_seq(SL,freq)
		seqs.append(temp)		

	## Read ICPC to p mapping
	f=open(filename,'rb')
	icpc_to_p=[]
	flag=0
	for line in f:
		if (flag==0):
			flag=1
			continue;
		temp=line.strip().split()
		temp = [float(x) for x in temp]
		icpc_to_p.append(temp)
	f.close()
	for i in range(0,len(icpc_to_p)):
		if (ICPC==icpc_to_p[i][0]):
			p=icpc_to_p[i][1]
	q=(1-p)/3.0

	## Generate a random motif and write to file motif.txt
	random_motif=generate_seq(ML,freq)
	f_motif=open('./'+dataset_folder+'/motif.txt','wb')
	f_motif.write('>'+random_motif+'\t'+str(ML)+'\n')

	## Generate SC motifs of length ML
	motifs_temp=[]
	for i in range(0,ML):
		motif_freq=[q,q,q,q]
		for j in range(0,len(nuc)):
			if(random_motif[i]==nuc[j]):
				motif_freq[j]=p
		temp=generate_seq(SC,motif_freq)
		motifs_temp.append(temp)
	motifs=[]
	for i in range(0,SC):
		temp=[]
		for j in range(0,ML):
			temp.append(motifs_temp[j][i])
		motifs.append(''.join(temp))
	
	## Writing PWM to motif.txt
	profile_matrix_tuples=[]
	profile_matrix=[]
	### Calculate profile matrix
	for i in range(0,ML):
		count=[0,0,0,0]
		for j in range(0,SC):
			for k in range(0,len(nuc)):
				if (motifs[j][i]==nuc[k]):
					count[k]=count[k]+1
		profile_matrix.append(count)
	### Write profile matrix to motif.txt in the required file
	for i in range(0,len(profile_matrix)):
		for j in range(0,len(profile_matrix[0])):
			f_motif.write(str(profile_matrix[i][j])+'\t')
		f_motif.write('\n')
	f_motif.write('<')
	f_motif.close()

	## Planting motifs in seqs
	new_seq=[]
	position=[]
	for i in range(0,SC):
		temp,pos=plant_motifs_in_seqs(seqs[i],motifs,ML,SL)
		new_seq.append(temp)
		position.append(pos)
	
	## Write new sequences to sequences.fa file
	f=open('./'+dataset_folder+'/'+sequence_filename,'wb')
	for i in range(0,SC):
		f.write('>seq'+str(i+1)+'\n'+new_seq[i]+'\n')
	f.close()

	## Write plant positions to sites.fa file (these are indexed starting from 0)
	f=open('./'+dataset_folder+'/'+site_filename,'wb')
	for i in range(0,SC):
		f.write(str(position[i])+'\n')
	f.close()
	
	## Write motiflength
	f=open('./'+dataset_folder+'/'+'motiflength.txt','wb')
	f.write(str(ML))
	f.close()
		
