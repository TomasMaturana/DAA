import bloom
import random
import csv 
import math
import time
import numpy as np
import string
import os
import sys
import tracemalloc
from pympler import asizeof

FILE="L.txt"
MIN_LETTER=4
MAX_LETTER=20
VERBOSE=0
LETTERS='abcdefghijklmnopqrstuvwxyz'

class Testing:
  def __init__(self, m, n, k, p, prob):
    self.m = m
    self.n = n
    self.k = k
    self.p = p
    self.prob = prob
  
  def run(self, use_filter):
    start = time.perf_counter()
    if use_filter:
      filter_blm = bloom.Bloom(self.m, self.k)
      data_filter = exp(self.n, self.p, self.prob, filter_blm=filter_blm, use_filter=True)
    else:
      data_filter = exp(self.n, self.p, self.prob)
    data_filter.append(time.perf_counter() - start)
    if use_filter:
      data_filter += [self.m,self.n,self.k,self.prob]
    else:
      data_filter += [self.n,self.prob]

    return data_filter

def generateL(str_array):
  with open(FILE, 'w') as f:
    for i in range(len(str_array)):
      f.write(str_array[i])

# Pregunta 9
# inserta n strings aleatorios a un filtro de Bloom y a un archivo en disco L
def insertN(n, filter_blm, use_filter):
  str_array=[]
  #tracemalloc.start()
  with open(FILE, 'w') as f:
    for i in range(n):
      rand= (random.randint(0,2**10)%MAX_LETTER) + MIN_LETTER
      name=""
      for l in range(rand):
        name=name+random.choice(LETTERS)
      if use_filter:
        filter_blm.insertar(name)
      str_array.append(name)

      host = "".join(random.sample(LETTERS,3))
      domain = "".join(random.sample(LETTERS,random.randint(2,3)))
      
      emailString=f"{name}@{host}.{domain}"
      user_reg = name + ' ' + emailString + '\n'
      f.write(user_reg)
  f.close()
  size_file = os.path.getsize(FILE)
  #space_filter, peak = tracemalloc.get_traced_memory()
  space_filter = asizeof.asizeof(filter_blm)
  #tracemalloc.stop()
  return [str_array, space_filter, size_file]

# Pregunta 10
# Busca en L las palabras que son pasan el filtro
def searchUser(name, filter_blm, use_filter):
  if use_filter and filter_blm.revisar(name):
    if VERBOSE: print("[*] El usuario " + name + " puede estar en L")
    cmd = f"grep '{name}' L.txt"
    if VERBOSE: print("[*] Resultado de búsqueda: ")
    os.system(cmd)
    return 1
  elif not use_filter:
    cmd = f"grep '{name}' L.txt"
    os.system(cmd)
    return 1
  else:
    if VERBOSE: print("[*] No existe usuario " + name)
    return 0

# Experimento
def exp(n, p, prob, filter_blm=None, use_filter=False):  ## n inserciones y p cantidad de pruebas
  buscados=0
  false_positives=0
  siEstan=0
  str_array, space_filter, size_L=insertN(n, filter_blm, use_filter)
  for i in range(p):
    if np.random.choice([0, 1], p=[prob, (1-prob)]):  #se preguntará por string aleatorio
      rand= (random.randint(0,2**10)%MAX_LETTER) + MIN_LETTER
      while True:
        name=""
        for l in range(rand):
          name += random.choice(LETTERS)
        if not (name in str_array):
          false_positives+=searchUser(name, filter_blm, use_filter)
          if VERBOSE: print('\n')
          break
    else:                       #se preguntará por string que está en L.txt
      siEstan += 1
      user = random.choice(str_array)
      buscados += searchUser(user[0:user.find(' ')], filter_blm, use_filter)
      if VERBOSE: print('\n')
  if VERBOSE: resumen(test=p, user_valid=siEstan, user_invalid=p-siEstan, searched=buscados, false_pos=false_positives)
  data = [p, siEstan, p-siEstan, buscados, false_positives, space_filter, size_L]
  return data       #debería tender a cero si el filtro funciona

def generate_csv(a, name, header):
  with open(f"{name}.csv", 'w', newline='', encoding='utf-8') as test:
    file_writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(header)
    for i in a:
      file_writer.writerow(i)

def set_test():
  array_prob = [.7,.9]
  array_m = np.arange(1000, 10000, step=2000)
  array_n = np.vectorize(lambda x: x//5)(array_m)
  data_filter = []
  data_not_filter = []
  for i in range(len(array_m)):
    for prob in array_prob:
      m = array_m[i]
      array_p = [m*2]
      for p in array_p:
        n = array_n[i]
        k = math.ceil(array_m[i]/array_n[i] * math.log(2))
        test = Testing(m=m, n=n, k=k, p=p, prob=prob)  
        data_filter.append(test.run(True))
        data_not_filter.append(test.run(False))

  generate_csv(data_filter, "analize_filter")
  generate_csv(data_not_filter, "analize_not_filter")

def set_test_nk():
  array_prob = [.1, .3, .7, .9]
  array_m = np.arange(100, 1000, step=100)
  n = 100
  data_filter = []
  data_not_filter = []
  for i in range(len(array_m)):
    for prob in array_prob:
      m = array_m[i]
      array_p = [m//2, m*2]
      for p in array_p:
        #k_v = math.ceil(array_m[i]/n * math.log(2))
        #if k_v>1:
          #array_k = [k_v-1, k_v, k_v+1]
        #else:
          #array_k = [k_v, k_v+1, k_v+2]
        k = math.ceil(array_m[i]/n * math.log(2))
        test = Testing(m=m, n=n, k=k, p=p, prob=prob)  
        data_filter.append(test.run(True))
        data_not_filter.append(test.run(False))
  
  generate_csv(data_filter, "analize_filter")
  generate_csv(data_not_filter, "analize_not_filter")


# grafico de tiempo
def grafico_1():
  prob = [.1, .9]
  m = 2500
  n = 500
  n_queries = np.arange(100, 1100, step=100)
  data_filter = []
  data_not_filter = []
  for i in range(len(n_queries)):
    for p in prob:
      k = math.ceil(m/n * math.log(2))
      test = Testing(m=m, n=n, k=k, p=n_queries[i], prob=p)  
      data_filter.append(test.run(True))
      data_not_filter.append(test.run(False))
  header_1 = ["queries", "num_user_valid", "num_user_invalid", "searched", "user_invalid_searched_FP", "space_filter", "size_L", "time", "m", "n", "k", "prob_is_L"]
  header_2 = ["queries", "num_user_valid", "num_user_invalid", "searched", "user_invalid_searched_FP", "space_filter", "size_L", "time", "n", "prob_is_L"]
  generate_csv(data_filter, "analize_filter_time_2", header_1)
  generate_csv(data_not_filter, "analize_not_filter_time_2", header_2)


# grafico de k
def grafico_2():
  prob = [.1, .5 ,.9]
  m = 2500
  n = 500
  n_queries = 1000
  data_filter = []
  data_not_filter = []
  k_optimo = math.ceil(m/n * math.log(2))
  for p in prob:
    for k in range(1,11):
      test = Testing(m=m, n=n, k=k, p=n_queries, prob=p)  
      data_filter.append(test.run(True))
      data_not_filter.append(test.run(False))
  for r in data_filter:
    r.append(k_optimo)
  header_1 = ["queries", "num_user_valid", "num_user_invalid", "searched", "user_invalid_searched_FP", "space_filter", "size_L", "time", "m", "n", "k", "prob_is_L", "k_optimo"]
  generate_csv(data_filter, "graph_k", header_1)


# grafico de espacio
def grafico_3():
  prob = .1
  n = 1000
  array_filter = np.arange(100, 2200, step=200)
  n_queries = 2000
  data_filter = []
  data_not_filter = []
  for m in array_filter:
    k = math.ceil(m/n * math.log(2))
    test = Testing(m=m, n=n, k=k, p=n_queries, prob=prob)  
    data_filter.append(test.run(True))
    data_not_filter.append(test.run(False))
  header_1 = ["queries", "num_user_valid", "num_user_invalid", "searched", "user_invalid_searched_FP", "space_filter", "size_L", "time", "m", "n", "k", "prob_is_L"]
  generate_csv(data_filter, "graph_espacio", header_1)


def resumen(test, user_valid, user_invalid, searched, false_pos):
  print("-"*50)
  print("[*] RESUMEN")
  print("-"*50)
  print("[+] Se hicieron "+ str(test) +" pruebas, de las cuales "+ str(user_valid) +" eran usuarios que estaban en L y "+ str(user_invalid) +" usuarios que no estan en L.")
  print("[+] De los "+ str(user_valid) +" que estaban en L, "+ str(searched) +" se buscaron en L.")
  print("[+] De los "+ str(user_invalid) +" usuarios que no estaban, "+ str(false_pos) +" se buscaron en L (falsos positivos).")


if __name__ == '__main__':
  if len(sys.argv) != 6 or float(sys.argv[5])<0 or float(sys.argv[5])>1:
    if len(sys.argv) == 1:
      grafico_3()
    else:
      print('Use: '+sys.argv[0]+' m k n pruebas probabilidad_de_estar_en_L')
    sys.exit(1)
  m=int(sys.argv[1])
  k=int(sys.argv[2])
  n=int(sys.argv[3])
  p=int(sys.argv[4])
  prob=float(sys.argv[5])
  blm=bloom.Bloom(m, k)
  exp(n, p, prob, filter_blm=blm, use_filter=True)






