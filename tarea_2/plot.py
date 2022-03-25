from matplotlib import pyplot
import random
import numpy as np
import pandas as pd

df1 = pd.read_csv('output_binary.csv')
df2 = pd.read_csv('output_fibonacci.csv')

rho1 = df1[df1["density"]==0.1]
rho2 = df2[df2["density"]==0.1]
rho3 = df1[df1["density"]==0.9]
rho4 = df2[df2["density"]==0.9]

#bin
#fib
pyplot.errorbar(rho1["edges"], rho1["comparations"], yerr=rho1["error"], fmt='o', linestyle='-', capsize=3, color='b')
pyplot.errorbar(rho2["edges"], rho2["comparations"], yerr=rho2["error"], fmt='o', linestyle='-', capsize=3, color='r')
pyplot.errorbar(rho3["edges"], rho3["comparations"], yerr=rho3["error"], fmt='o', linestyle='-', capsize=3, color='y')
pyplot.errorbar(rho4["edges"], rho4["comparations"], yerr=rho4["error"], fmt='o', linestyle='-', capsize=3, color='g')
pyplot.xlabel('edges')
pyplot.ylabel('comparations')
pyplot.plot()
pyplot.grid(True)
pyplot.show()