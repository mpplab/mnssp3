# motifFinding

http://weblogo.berkeley.edu/logo.cgi

Gibbs sampling paper (for proteins): http://science.sciencemag.org/content/262/5131/208.full.pdf+html

### Step 1 : Generate datasets
```python generateData.py```

Or, to create all datasets asked in the requirements, </br>
```source generateDatasets.sh```

### Step 2 : Find motifs
```source motifFinderGibbsAlgo.sh```

This program runs the gipps.py for all <b>dataset*</b> folders in the directory </br>
The output generated is insite the datasets folders named <b>gibbs_output</b> </br>
10 Runs have been carried out for each dataset, so that later proper analysis can be done </br>

### Step 3 : Analysis
In addition to the <b>predictedmotif.txt</b> and <b>predictedsites.txt</b> (as required), an <b>IC.npy</b> file is generated which can be visualized using the following code as an example:

```
import numpy as np
data1=np.load('gibbs_01_IC.npy')
data2=np.load('gibbs_02_IC.npy')
data3=np.load('gibbs_03_IC.npy')

import matplotlib.pylab as plt

plt.figure(figsize=(10,2))
plt.plot(data1)
plt.plot(data2)
plt.plot(data3)
plt.xlabel('Number of rounds')
plt.ylabel('Information Content (per bit)')
plt.semilogx()

plt.show()
```
