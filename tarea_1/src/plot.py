from matplotlib import pyplot
import random
import numpy as np

data = np.genfromtxt("bb.csv", delimiter=",", skip_header=1, names=['k', 't'])
c = 0 
q = 0
qv = []
for d in data:
    c += d[1]
    q = c/(d[0]-1)
    qv.append([d[0], q])
qv = np.array(qv)
yerror = np.std(qv[:,1]) / np.sqrt(np.array(qv[:,0]))
pyplot.errorbar(qv[:, 0], qv[:, 1], yerr=yerror, fmt='o', linestyle='-', capsize=3)
pyplot.xlabel('numero de repeticiones')
pyplot.ylabel('Costo promedio experimental (s)')
pyplot.plot()
pyplot.grid(True)
pyplot.show()