import sys
import random
import os
import externalBinarySearch as EBS

B = 500

# Busqueda binaria pero que devuelve el indice 
# donde se encuentra el elemento en el arreglo
def binary_search(value, array):
    hi = len(array) - 1
    lo = 0 
    mid = 0
    while lo<=hi:
        mid = (hi + lo)//2
        a_m = array[mid] 
        if value > a_m:
            lo = mid + 1
        elif value < a_m:
            hi = mid - 1
        else:
            return mid
    if value > array[mid]: 
        return mid
    else: 
        return mid - 1

# Algoritmo de busqueda indexada
def indexedSearchInter(P,T):
    sizeT = os.path.getsize(T)
    out = []
    S = []
    numB = sizeT//B
    pArray = EBS.read_file(P).split('\n')
    pArray.pop()
    for i in range(numB):
        S.append(EBS.read_index(T,i*500))
    for pe in pArray:
        index_block= binary_search(value=pe,array=S)
        tblock = EBS.read_block(T, index_block*500).split('\n')
        tblock.pop()
        if pe in tblock:
            out.append(pe)
    return out

if __name__ == '__main__':
    P = sys.argv[1]
    T = sys.argv[2]
    s = EBS.SearchAlgorith(indexedSearchInter)
    #s.run(P,T)
    #s.not_generate()
    s.run_print_time(P, T, 1)