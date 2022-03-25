import os
import time

B=500           # Numeros de bloques
IO_count = 0    # Cantidad de operaciones I/O realizadas

# Dada una posicion del archivo, comienza a leer un bloque desde esa posición
def read_block(filename, position=None):
    global IO_count
    with open(filename, 'r') as f:
        if position:
            f.seek(position)
        block = f.read(B)
    IO_count += 1
    return block

# Lee una linea de largo 10 bytes de un archivo dada una posicion
def read_index(filename, position):
    global IO_count
    with open(filename, 'r') as f:
        f.seek(position)
        value = f.read(9)
    IO_count += 1
    return value 

# Lee un archivo completo de a bloques de tamaño B
def read_file(filename):
    global IO_count
    file_content_array = []
    with open(filename, 'r') as f:
        while True:
            block = f.read(B)
            if not block:
                break
            IO_count += 1
            file_content_array.append(block)
    return str().join(file_content_array)

def e_binary_search(str_element, tfile):
    size_file = os.path.getsize(tfile)
    size_block = size_file // B
    l = 0
    r = size_block - 1
    while l <= r:
        m = (l + r)//2
        position_to_read = m*B
        block = read_block(tfile, position_to_read)
        str_numbers = block.split('\n')
        str_numbers.pop()
        if str_element in str_numbers:
            return True
        first_block = str_numbers[0]
        last_block = str_numbers[-1]
        if str_element >= first_block and str_element <= last_block:
            return False
        if str_element < first_block:
            r = m - 1
        else:
            l = m + 1
    position_to_read = l*B
    block = read_block(tfile, position_to_read)
    return str_element in block.split('\n')

# Genera un string que representa un numero de 9 digitos
def format_int(n):
    s = str(n)
    return '{}{}{}'.format('0'*(9-len(s)), s, '\n')

# Escribe un
def write_int_file(toWrite, file_name='output.txt'):
    global IO_count
    T_content = str().join(list(map(format_int, toWrite)))
    with open(file_name, 'w') as f:
        number_blocks = len(T_content) // B
        if (number_blocks>0):
            for i in range(number_blocks):
                IO_count += 1
                f.write(T_content[i*B:(i+1)*B])
        else:
            IO_count += 1
            f.write(T_content)

class SearchAlgorith():
    def __init__(self, function, output_name='output'):
        self.f = function
        self.out = output_name
        self.generate = True

    # Cambia la generacion de un archivo
    def not_generate(self):
        self.generate = False

    # Corre el algoritmo con los archivos P y T
    # k es un parametro opcional para repetir el proceso
    def run(self, P, T, k=1):
        start = time.perf_counter()
        inter = self.f(P, T)
        print(inter)
        if self.generate:
            write_int_file(inter, file_name=f'{self.out}_{k}.txt')
        elapsed_time = time.perf_counter() - start
        return elapsed_time

    # Corre el algoritmo imprimiendo el tiempo que dedicado en calcular el algoritmo
    def run_print_time(self, P, T, k):
        global IO_count
        for i in range(1, k+1):
            elapsed_time = self.run(P, T, i)
            if i==1: print(f"I/O: {IO_count}")
            print(f"{i}, {elapsed_time}")