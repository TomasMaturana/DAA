import sys
import random
import time
import os
import externalBinarySearch as EBS

# Dados dos archivos P y T devuelve la interseccion
# utilizando busqueda binaria sobre el archivo T
def intersectionBS(pfile, tfile):
    inter = []
    P = EBS.read_file(pfile).split('\n')
    P.pop()
    for n in P:
        t = EBS.e_binary_search(n, tfile)
        if t: inter.append(n)
    return inter

if __name__ == '__main__':
    P = sys.argv[1]
    T = sys.argv[2]
    a = EBS.SearchAlgorith(intersectionBS)
    #a.not_generate()
    a.run(P, T)
    #a.run_print_time(P, T, 1)