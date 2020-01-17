
import gmi_config
gmi_config.read_config()

foldername = gmi_config.PROJECT_NAME
foldername = 'result_' + foldername

import numpy as np
converg = np.loadtxt(foldername+ '/' + 'nlssubprob.dat')

import matplotlib.pyplot as plt



fig, ax = plt.subplots()
ax.plot(converg[:, 0], converg[:, 1])

ax.set(xlabel='Iteration', ylabel='Projected Gradient',
       title='Convergence')
ax.grid()

fig.savefig(foldername+ '/' + "nlssubprob.png")
plt.show()