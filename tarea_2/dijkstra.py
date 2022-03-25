import sys
import numpy as np
import random
import math
import csv
import warnings
import time
from sys import stdin, stdout
from binary import *
from fibonacci import FibonacciHeap
from numpy import random as nprand


class Graph():
  def __init__(self, vertices, edges, queue):
    self.nvertex = vertices
    self.nedges = edges
    self.edges = {}
    if (type(queue)==str):
      self.queue = self.queue_init(queue)
    else:
      self.queue = queue

  def add_edge(self, v1, v2, w):
    if not v1 in self.edges:
      self.edges[v1] = [[v2, w]]
    else:
      self.edges[v1].append([v2, w])
    if not v2 in self.edges:
      self.edges[v2] = [[v1, w]]
    else:
      self.edges[v2].append([v1, w])

  def dijsktra(self, s):
    dist = [sys.maxsize]*(self.nvertex+1)
    dist[s] = 0
    for k in self.edges.keys():
      self.queue.insert(k, dist[k])
    while(not self.queue.empty()):
      u, minimum = self.queue.extract_min()
      for j in self.edges[u]:
        v2, w = j
        if dist[v2] > dist[u] + w:
          dist[v2] = dist[u] + w
          self.queue.decrease_key(v2, dist[v2]) 
    return [dist[1:], self.queue.getComp()]

  def dijsktra_test(self, s):
    return self.dijsktra(s)[1]

  def queue_init(self, queue):
    """
      Init the queue
    """
    if queue=="FibonacciHeap":
        return FibonacciHeap(self.nvertex)
    if queue=="BinaryHeap":
        return BinaryHeap(self.nvertex)
    else:
      raise Exception("Unknown heap {}".format(queue))

def generator(nnodes, density):
    all_nodes = int((nnodes*(nnodes-1))//2)
    generator = nprand.binomial(n=1, p=density, size=all_nodes)
    total = ""
    edges = []
    i = 0
    for v in range(1,nnodes+1):
      for u in range(v,nnodes+1):
        if v!=u:
          node = [v, u]
          if generator[i] or v+1==u:
            index = random.randint(0, nnodes-1)
            w = random.randint(1, 10**9)
            node.append(w)
            edges.append(node)
          i+=1
    s = random.randint(1, nnodes)
    return [nnodes, edges, s]

def choice_queue():
  if len(sys.argv) > 1:
    return sys.argv[1]
  else: 
    return "BinaryHeap"

def main():
  """
    App Dijkstra
  """
  queue = choice_queue()
  vertices, edges = [int(x) for x in stdin.readline().split()]
  graph = Graph(vertices, edges, queue)
  for i in range(edges):
    v, vn, w = [int(x) for x in stdin.readline().split()]
    graph.add_edge(v, vn, w)
  s = int(input())
  res, _ = graph.dijsktra(s)
  res = " ".join(list(map(lambda x: str(x), res)))
  print(res)

def generate_csv(a, name):
  with open(f"{name}.csv", 'w', newline='', encoding='utf-8') as test:
    file_writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ["vertex", "density", "edges", "comparations", "error", "time"]
    file_writer.writerow(header)
    for i in a:
      file_writer.writerow(i)


def main_test():
  """
    Generate a set test for create graphs
  """
  density = [0, .1, .3, .5, .7, .9, 1] 
  nnodes = [10, 30, 50, 70, 90, 200, 300, 500, 1000]
  number_compare = []
  for i in range(2): 
    array_res = []
    for n in nnodes:
      for rho in density:
        prom = []
        mean_time = []
        prom_edges = []
        for t in range(3):
          c_nodes, edges, s = generator(n, rho)
          queue = FibonacciHeap(n) if i == 0 else BinaryHeap(n)
          graph = Graph(n, len(edges), queue)
          for e in edges:
            v1,v2,w = e
            graph.add_edge(v1,v2,w)
          start = time.perf_counter()
          res = graph.dijsktra_test(s)
          elapsed_time = time.perf_counter() - start
          prom.append(res)
          mean_time.append(elapsed_time)
          prom_edges.append(len(edges))
        res = [n, rho, np.mean(prom_edges), np.mean(prom), np.std(prom)/math.sqrt(3), np.mean(mean_time)]
        array_res.append(res)
    number_compare.append(array_res)
  for i in range(len(number_compare)):
    f = "output_fibonacci" if i==0 else "output_binary"
    generate_csv(number_compare[i], f)


if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1] == "test":
    main_test()
  else:
    main()