import mmh3
import random 
import numpy as np
from BitVector import BitVector

class Bloom:
  def __init__(self, m, k):
    np.random.seed(0)
    self.m = m
    self.k = k
    self.seeds=[]
    for i in range(k):
      self.seeds.append(random.randint(0, 2**10))
    self.bits = BitVector(size=m)

  def insertar(self, p):
    for i in range(self.k):
      hi = mmh3.hash(p, self.seeds[i]) % self.m
      self.bits[hi] = 1

  def revisar(self, p):
    for i in range(self.k):
      hi = mmh3.hash(p, self.seeds[i]) % self.m
      if self.bits[hi] == 0:
        return 0
    return 1

