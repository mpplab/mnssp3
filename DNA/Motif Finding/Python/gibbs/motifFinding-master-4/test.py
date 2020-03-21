import numpy as np
data1=np.load('name-IC.npy')
print data1
# data2=np.load('gibbs_02_IC.npy')
# data3=np.load('gibbs_03_IC.npy')

import matplotlib.pylab as plt

# plt.figure(figsize=(4,4))
# data1 = [1,2,3,4]
plt.plot(data1)
# plt.plot(data2)
# plt.plot(data3)
plt.xlabel('Number of rounds')
plt.ylabel('Information Content (per bit)')
plt.semilogx()
plt.show()

