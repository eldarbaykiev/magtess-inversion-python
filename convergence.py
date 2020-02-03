
foldername='result_2degx2deg_apriori_hemant_crust1.0_wolfgang.x0'

import numpy as np


converg = np.loadtxt(foldername+ '/' + 'nlssubprob.dat')

import matplotlib.pyplot as plt


fig, ax = plt.subplots()
ax.plot(converg[:, 0], converg[:, 1], lw=0.6)

ax.set(xlabel='Iteration', ylabel='Projected Gradient norm',
       title='Convergence')
ax.grid()

fig.savefig(foldername+ '/' + "nlssubprob.png")
plt.show()
