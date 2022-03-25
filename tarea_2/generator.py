import sys
import random
from numpy import random as nprand

'''
 * Uso : python generator.py <number_nodes> <density> 
         Devuelve un string que representa un grafo con una densidad = density
         y un numero de nodos = number_nodes
'''

def generator(nnodes, density):
    all_nodes = int((nnodes*(nnodes-1))//2)
    generator = nprand.binomial(n=1, p=density, size=all_nodes)
    total = ""
    graph = []
    i = 0
    for v in range(1,nnodes+1):
      for u in range(v+1,nnodes+1):
        node = [v, u]
        if generator[i] or v+1==u:
          index = random.randint(0, nnodes-1)
          w = random.randint(1, 10**9)
          node.append(w)
          graph.append(node)
          node_s = " ".join(list(map(lambda x: str(x), node)))
          total += f"{node_s}\n"
        i+=1
    s = random.randint(1, nnodes)
    print(nnodes, len(graph))
    print(total+ str(s))

if __name__ == "__main__":
    if len(sys.argv)>1:
        nnodes = int(sys.argv[1])
        density = float(sys.argv[2])
        generator(nnodes, density)
    else:
      raise "Error in number of arguments"
