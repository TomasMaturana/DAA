import math

class FibonacciNode:
  def __init__(self,x,k):
    self.x = x
    self.k = k
    self.next = self
    self.prev = self
    self.child = None
    self.degree = 0
    self.parent = None
    self.mark = False

def linkNode(nodeMin,nodeMax):
  if (nodeMin.child!=None):
    nodeMinChild = nodeMin.child
    childPrev = nodeMinChild.prev
    childPrev.next = nodeMax
    nodeMinChild.prev = nodeMax
    nodeMax.next = nodeMinChild
    nodeMax.prev = childPrev
    nodeMin.degree = nodeMin.degree + 1
    nodeMax.parent = nodeMin
  else:
    nodeMax.next = nodeMax
    nodeMax.prev= nodeMax
    nodeMin.child = nodeMax
    nodeMax.parent = nodeMin
    nodeMin.degree = nodeMin.degree + 1
  return nodeMin

class FibonacciHeap:

  def __init__(self, n):
    self.currentNodes = 0
    self.rootNodes = 0
    self.maxnodes = n
    self.minPointer = None
    self.P = [None for i in range(n+1)]
    self.comp = 0
  
  def insert(self, x, k):
    node = FibonacciNode(x, k)
    self.currentNodes += 1
    self.addToRoot(node)
  
  def addToRoot(self,node):
    if (self.currentNodes<=self.maxnodes):
      self.comp += 1
      node.parent = None
      if (self.minPointer!=None):
        node.next = self.minPointer
        node.prev = self.minPointer.prev
        self.minPointer.prev.next = node
        self.minPointer.prev = node
        if (node.k<self.minPointer.k):
          self.minPointer = node
        self.rootNodes += 1
      else:
        self.minPointer = node
        self.rootNodes += 1
      self.P[node.x] = node
    else:
      self.currentNodes -=1
      print("Limite de pares ordenados en la cola excedido")
  
  def consolidate(self):
    A = [None for i in range(self.maxnodes+1)]
    node = self.minPointer
    for j in range(self.rootNodes):
      nodeDeg = node.degree
      nextNode = node.next
      while (A[nodeDeg]!=None):
        self.comp +=1
        nodeA = A[nodeDeg]
        if (nodeA.k>node.k):
          node = linkNode(node,nodeA)
        else:
          node = linkNode(nodeA,node)
        A[nodeDeg] = None
        nodeDeg = node.degree
      A[node.degree]=node
      node = nextNode
    self.minPointer = None
    self.rootNodes = 0
    for i in range(len(A)):
      if (A[i]!=None):
        A[i].next = A[i]
        A[i].prev = A[i]
        self.addToRoot(A[i])


  def extract_min(self):
    if (self.minPointer!=None):
      self.comp+=1
      m = self.minPointer
      self.P[self.minPointer.x] = None
      self.currentNodes -= 1
      if (m.child!=None):
        firstChild = m.child
        child = m.child.next
        if (child.next!=child):
          while (child != firstChild):
            nextchild = child.next
            self.addToRoot(child)
            child = nextchild
        self.addToRoot(firstChild)
      nextNode = m.next
      if (m!=nextNode):
        prevNode = m.prev
        nextNode.prev = prevNode
        prevNode.next = nextNode
        self.minPointer = nextNode
        self.rootNodes-=1
        self.consolidate()
      else:
        self.rootNodes-=1
        self.minPointer=None
      return m.x, m.k
    return None

  def empty(self):
    return self.minPointer == None

  def removeChild(self,parent,node):
    firstChild = parent.child
    if (node.next!=node):
      if firstChild==node:
        parent.child = node.next
      node.next.prev = node.prev
      node.prev.next = node.next
    else:
      parent.child=None
    parent.degree -= 1


  def cut(self,parent,node):
    self.removeChild(parent,node)
    self.addToRoot(node)
    node.mark=False
  
  def cascading_cut(self,node):
    parent = node.parent
    if parent!=None:
      if node.mark==False:
        node.mark = True
      else:
        self.cut(parent,node)
        self.cascading_cut(parent)


  def decrease_key(self, x, k):
    node = self.P[x]
    if self.minPointer==None:
      print("cola vacía")
      return
    if node==None:
      print("nodo no existe")
      return
    if node.k<k:
      print("error: llave mas grande que la ya existente")
      return
    node.k = k
    if node.parent==None:
      if node.k<self.minPointer.k:
        self.minPointer=node
    elif node.parent.k>k:
      parent = node.parent
      self.cut(node.parent,node)
      self.cascading_cut(parent)

  def getComp(self):
    return self.comp