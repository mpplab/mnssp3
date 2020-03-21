"""
	Run the gibbs sampling algorith on the geenrated dataset for CSS 466 motif finding project 
	Team members: Shriyaa Mittal, Zahra Shamsi and Melanie Paige Muller
"""

import random
import time
import numpy as np
import math

### Constants
ITERATIONS=100000
acceptableIC=1.7
nuc = ['A','C','G','T']
freq = [0.25,0.25,0.25,0.25]

def getPWM(sequences,N,W,L,sites):
	## Generate random number from 0,SC for the sequence to be ignored
	random.seed(time.time())
	z=random.randrange(0,N)
	## Calculate PWM
	PWM=np.zeros((4,W))
	count=0 ## count goes from 0,N-1
	for i in range(0,N):
		if (i==z):
			continue;
		else:
			for j in range(0,W):
				if (sequences[i][sites[count]+j]==nuc[0]):
					PWM[0][j]+=1
				elif (sequences[i][sites[count]+j]==nuc[1]):
					PWM[1][j]+=1
				elif (sequences[i][sites[count]+j]==nuc[2]):
					PWM[2][j]+=1
				elif (sequences[i][sites[count]+j]==nuc[3]):
					PWM[3][j]+=1
		count+=1
	return PWM/(N-1),z


def getOdds(PWM,z,sequences,W,L):
	candidates_seq=[]
	for i in range(0,L-W+1):
		candidates_seq.append(sequences[z][i:i+W])
	candidates_odds=[]
	for i in range(0,len(candidates_seq)):
		P=1
		Q=1
		for j in range(0,W):
			if (candidates_seq[i][j]==nuc[0]):
				P*=freq[0]
				Q*=PWM[0][j]
			elif (candidates_seq[i][j]==nuc[1]):
				P*=freq[1]
				Q*=PWM[1][j]
			elif (candidates_seq[i][j]==nuc[2]):
				P*=freq[2]
				Q*=PWM[2][j]
			elif (candidates_seq[i][j]==nuc[3]):
				P*=freq[3]
				Q*=PWM[3][j]
		candidates_odds.append(Q/P)
	normed_odds=list(candidates_odds/sum(candidates_odds))
	## Retun the max odds index
	return normed_odds.index(max(normed_odds))
	## Return an index sampled proportionally from the odds (takes longer run-time)
#	random.seed(time.time())
#	x = random.random()
#	index = 0
#	while(x >= 0 and index 	< len(normed_odds)):
#		x -= normed_odds[index]
#		index += 1
#	return index-1

			
def getIC(sites,sequences,W,N,old_PWM):
	## Calculate new PWM
	new_PWM=np.zeros((4,W))
	count=0 ## count goes from 0,N
	for i in range(0,N):
		for j in range(0,W):
			if (sequences[i][sites[count]+j]==nuc[0]):
				new_PWM[0][j]+=1
			elif (sequences[i][sites[count]+j]==nuc[1]):
				new_PWM[1][j]+=1
			elif (sequences[i][sites[count]+j]==nuc[2]):
				new_PWM[2][j]+=1
			elif (sequences[i][sites[count]+j]==nuc[3]):
				new_PWM[3][j]+=1
		count+=1
	PWM=new_PWM/(N)
	IC=0
	for i in range(0,W):
		for j in range(0,4):	## 4 nucleotides
			if (j==0):
				temp=PWM[j][i]/freq[0]
			elif (j==1):
				temp=PWM[j][i]/freq[1]
			elif (j==2):
				temp=PWM[j][i]/freq[2]
			elif (j==3):
				temp=PWM[j][i]/freq[3]
			if (temp==0):
				continue;
			IC+=PWM[j][i]*math.log(temp,2)
	return IC,PWM
	

if __name__ == "__main__":

	## Read input files
	f_motiflength=open('motiflength.txt','rb')
	for line in f_motiflength:
		W=int(line)	## motiflength
	f_motiflength.close()
	f_sequences=open('sequences.fa','rb')
	sequences=[]
	flag=0
	for line in f_sequences:
		if (flag==0):
			flag=1
		elif (flag==1):
			flag=0
			sequences.append(line.strip('\n'))
	f_sequences.close()	

	N=len(sequences)	## Number of sequences
	L=len(sequences[0])	## Length of sequences, assumed all are of same length)
	info=[['IC'],['sites']]

	## Select starting point, generate motif site for the N-1 sequences
	sites=[]
	random.seed(time)
	for i in range(0,N-1):
		k=random.randrange(0,L-W)
#		k=0	## Fix the starting point for all runs
		sites.append(k)
	flag=0

	maxIC=0

	## Do multiple iterations
	for ITER in range(0,ITERATIONS):
		## Calculate PWM for N-1 sequences
		PWM,z=getPWM(sequences,N,W,L,sites)
		## Predict the site in the ignored sequence
		z_site=getOdds(PWM,z,sequences,W,L)
		if (flag==0):
			sites.insert(z,z_site)
			flag=1
		else:
			sites[z]=z_site
		temp=sites[:]
		## Calculate information content in the current iteration prediction
		info[1].append(temp)
		IC,PWM=getIC(sites,sequences,W,N,PWM)
		## Save information for analysis
		info[0].append(IC)
		if IC>maxIC:
			maxIC=IC
			maxPWM=PWM
		if (IC>(acceptableIC*W)):
			break;
	IC=maxIC
	PWM=maxPWM

	## Writing to predictedsites.txt file
	predicted_sites=info[1][-1]
	f=open('predictedsites.txt','wb')
	for i in range(0,len(predicted_sites)):
		f.write(str(predicted_sites[i])+'\n')
	f.close()

	## Finding the motif
	profile_matrix=np.transpose(PWM)*N
	motif=[]
	for i in range(0,W):
		temp=list(profile_matrix[i])
		max_val=max(temp)
		## check if the max_val occurs twice in the list i.e. two nucleotides may have equal probability of occurence
		duplicate_indx=[]
		for p in range(0,len(temp)):
			if (temp[p]==max_val):
				duplicate_indx.append(p)
		if (len(duplicate_indx)>1): ## Means there are duplicates
			indx=random.choice(duplicate_indx)
		else:
			indx=temp.index(max(temp))
		## Determine the motif based on the PWM
		motif.append(nuc[indx])
	finalmotif=''.join(motif)
	
	## Writing to predictedmotif.txt file
	f=open('predictedmotif.txt','wb')
	f.write('>'+finalmotif+'\t'+str(len(finalmotif))+'\n')
	for i in range(0,len(profile_matrix)):
		for j in range(0,len(profile_matrix[i])):
			f.write(str(int(profile_matrix[i][j]))+'\t')
		f.write('\n')
	f.write('<')
	f.close()

	## Data for plot
	## x-axis can be Number of Rounds and y-axis is Information Content (per bit, or per letter in the motif)
	for i in range(1,len(info[0])):
		info[0][i]=info[0][i]/W

	np.save('IC.npy',info[0][1:])
	
