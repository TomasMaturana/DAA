
class BinaryHeap:

  right = lambda self,i: 2*i
  left = lambda self,i: 2*i + 1
  parent = lambda self,i: i//2

  def __init__(self, maxnodes):
    self.tree = [0]
    self.is_empty = True
    self.nodes = [None]*(maxnodes+1)
    self.size = 0
    self.maxsize = maxnodes
    self.count_compare = 0

  def extract_min(self):
    """
      Extract the minimum
    """
    if self.is_empty:
      return
    minimum = self.tree[1]
    self.nodes[minimum[0]] = None
    self.tree[1] = self.tree[self.size]
    self.size -= 1
    max_node = self.tree[-1]
    self.tree.pop()
    if self.size == 0:
      self.is_empty = True
      return minimum
    index = self.swap_down(1)
    self.nodes[max_node[0]] = index
    return minimum
  
  def getComp(self):
    return self.count_compare

  def empty(self):
    """
      Check if a tree is empty
    """
    return self.is_empty

  def swap_down(self, i):
    im = self.min_child(i)
    while self.left(i) <= self.size and self.tree[i][1] > self.tree[im][1]:
      self.count_compare += 1
      tmp = self.tree[i]
      tmp_child = self.tree[im]
      self.tree[i] = self.tree[im]
      self.tree[im] = tmp
      self.nodes[tmp[0]] = im
      self.nodes[tmp_child[0]] = i
      i = im
      im = self.min_child(i)
    return i

  def min_child(self, i):
    """
      Return the index of the minimum child
    """
    if self.right(i) >= self.size:
      self.count_compare += 1
      return self.left(i)
    elif self.tree[self.left(i)][1] < self.tree[self.right(i)][1]:
      self.count_compare += 2
      return self.left(i)
    else:
      self.count_compare += 3
      return self.right(i)

  def swap_up(self, current):
    """
      swap a element if it is less than the parent
    """
    k_curr = self.tree[current][1]
    while(self.parent(current)>0 and k_curr < self.tree[self.parent(current)][1]):
      self.count_compare += 1
      tmp = self.tree[self.parent(current)]
      tmp_child = self.tree[current]
      self.tree[self.parent(current)] = self.tree[current]
      self.tree[current] = tmp
      self.nodes[tmp[0]] = current
      self.nodes[tmp_child[0]] = self.parent(current)
      current = self.parent(current)
      k_curr = self.tree[current][1]
    return current

  def get_node(self, i):
    return self.tree[self.nodes[i]]

  def insert(self, x, k):
    """
      insert a pair (x,k)
    """
    if self.is_empty:
      self.is_empty = False
    if self.size + 1 > self.maxsize:
      return self
    pair = [x, k]
    self.tree.append(pair)
    self.size += 1
    index = self.swap_up(self.size)
    self.nodes[x] = index
    return self

  def decrease_key(self, x, k):
    """
      Change the key of the element x
    """
    if not self.is_empty:
      self.tree[self.nodes[x]] = [x,k]
      current = self.swap_up(self.nodes[x])
      self.nodes[x] = current
      return self
  
  def pp_node(self, i):
    if(i<=self.size):
      node = self.tree[i]
      s1 = f"node: {node[0]}, k: {node[1]} \n"
      return s1
    else:
      return ""

  def pp_tree(self, i):
    s = self.pp_node(i)
    if s!="":
      s+= self.pp_tree(self.left(i))
      s+= self.pp_tree(self.right(i))
    return s
    
  def __str__(self):
    i = 1
    s = ""
    s += self.pp_node(i)
    s += self.pp_tree(self.left(i))
    s += self.pp_tree(self.right(i))
    return s
