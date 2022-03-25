import sys
import random
import os
import externalBinarySearch as EBS

B = 500

# Realiza busqueda binaria en un arreglo
def binary_search(value, array):
    hi = len(array) - 1
    lo = 0 
    while lo<=hi:
        mid = (hi + lo)//2
        a_m = array[mid] 
        if value > a_m:
            lo = mid + 1
        elif value < a_m:
            hi = mid - 1
        else:
            return True
    return False

# Verifica si un elemento t pertece al arreglo a 
# realizando una búsqueda lineal
def isIn(t, a):
    for i in a:
        if(t==i): return True
    return False

# Algoritmo de busqueda lineal
def linear_search(P,T):
    sizeT = os.path.getsize(T)
    out = []
    pArray = EBS.read_file(P).split('\n')
    pArray.pop()
    numB = sizeT//B
    for i in range(numB):
        bt = EBS.read_block(T, i*B).split('\n')
        bt.pop()
        for t in bt:
            if isIn(t, pArray):
                out.append(t)
    return out

# Busqueda lineal combinada con busqueda binaria
def linear_binary_search(P,T):
    sizeT = os.path.getsize(T)
    out = []
    pArray = EBS.read_file(P).split('\n')
    pArray.pop()
    numB = sizeT//B
    for i in range(numB):
        bt = EBS.read_block(T, i*B).split('\n')
        bt.pop()
        for p in pArray:
            e = binary_search(p, bt)
            if e: out.append(p)
    return out

# Busqueda lineal combinada con proceso de merge
def linear_binary_merge(P,T):
    def merge(a1, a2, out):
        i = 0
        j = 0
        while(i<len(a1) and j<len(a2)):
            if a1[i] < a2[j]:
                i += 1
            elif a1[i] > a2[j]:
                j += 1
            else:
                out.append(a1[i])
                i += 1
                j += 1

    sizeT = os.path.getsize(T)
    out = []
    pArray = EBS.read_file(P).split('\n')
    pArray.pop()
    pArray.sort()
    numB = sizeT//B
    for i in range(numB):
        bt = EBS.read_block(T, i*B).split('\n')
        bt.pop()
        merge(pArray, bt, out)
    return out


# Por defecto el script corre el algoritmo de busqueda lineal
if __name__ == '__main__':
    P = sys.argv[1]
    T = sys.argv[2]
    s = EBS.SearchAlgorith(linear_search)
    #s.not_generate()
    s.run_print_time(P, T, 1)
