import sys
import random

'''
 * Uso : python generator.py <number_lines_P> <number_lines_T> 
         Devuelve dos archivos con strings de largo 9 
         P: Contiene strings desordenados uniformemente
         T: Contiene strings ordenados de menor a mayor
 
 * Uso alternativo : python generator.py
         Devuelve un conjunto de prueba de los archivos
         P y T
'''

B = 500

def format_int(n):
    s = str(n)
    return '{}{}{}'.format('0'*(9-len(s)), s, '\n')

def set_test():
    def gen_files(arr, narr, sort=True):
        for fn in range(len(arr)):
            if sort: generator(arr[fn], narr[fn], sort)
            else: generator(arr[fn], narr[fn], sort)
    files_t = [f'T_{i}.txt' for i in range(4,7)] # 10**4 < T < 10**7-1
    files_p = [f'P_{i}.txt' for i in range(1,3)] # 10 < T < 10**3
    nlines_t = [10**i - 1 for i in range(4,7)]
    nlines_p = [10**i - 1 for i in range(1,3)]
    gen_files(files_t, nlines_t)
    gen_files(files_p, nlines_p, sort=False)

def generator(file_name, nlines, sort):
    T_array = [random.randint(1, 10**9) for _ in range(nlines)]
    if sort: T_array.sort()
    T_content = str().join(list(map(format_int, T_array)))
    with open(file_name, 'w') as f:
        number_blocks = len(T_content) // B
        if number_blocks == 0:
            f.write(T_content)
        for i in range(number_blocks):
            f.write(T_content[i*B:(i+1)*B])

if __name__ == "__main__":
    if len(sys.argv)>1:
        nlines_p = int(sys.argv[1])
        nlines_t = int(sys.argv[2])
        generator('T.txt', nlines=nlines_t, sort=True)
        generator('P.txt', nlines=nlines_p, sort=False)
    else: set_test()
