# coding=utf-8
import re
import sys

class BColors:
  def __init__(self):
      pass

  # FOREGROUND
  BLACK = '\033[30m'
  RED = '\033[31m'
  GREEN = '\033[32m'
  YELLOW = '\033[33m'
  BLUE = '\033[34m'
  MAGENTA = '\033[35m'
  CYAN = '\033[36m'
  WHITE = '\033[37m'
  RESET = '\033[39m'


list_of_nodes = []

def entry():

  for  i in sys.stdin:

    entry_split = re.split('\W+', i)

    if entry_split[len(entry_split) - 1] == '':
      del entry_split[len(entry_split) - 1]

#    sys.stdout.write(BColors.MAGENTA)
#    print entry_split
#    sys.stdout.write(BColors.RESET)

    for index in range(len(entry_split)):
      if index <= 1:
        #if entry_split[index] not in list_of_nodes:
        list_of_nodes.append(int(entry_split[index]))
        

entry()
  

class Node:
  
  def __init__(self, key, left=None, right=None):
    self.left = left
    self.right = right
    self.key = key
  
  def __str__(self):
    return str(self.key)

    
class AVLTree:
  
  
  def __init__(self):
    self.node = None
    self.height = -1
    self.balance = 0
  
  
  def __str__(self):
    return str(self.node)
    
  
  # INSERT
  def insert(self, key):
    
    # create new node
    n = Node(key)
    
    # init tree
    if self.node == None:
      self.node = n
      self.node.left = AVLTree()
      self.node.right = AVLTree()
    # insert key to the left subtree
    elif key < self.node.key:
      self.node.left.insert(key)
    # insert key to the right subtree
    elif key >= self.node.key:
      self.node.right.insert(key)
  
    # rebalance tree if needed
    self.rebalance()
  
  
  # REBALANCING
  def rebalance(self):
    # check if need rebalance; update height; balance tree
    self.updateHeights(recursive = False)
    self.updateBalance(False)
    
    # for each node checked, if the balance factor = -1, 0, or 1
    while self.balance < -1 or self.balance > 1:
      # left subtree is larger than right subtree
      if self.balance > 1:
        # left right case - rotate to left
        if self.node.left.balance < 0:
          self.node.left.rotateLeft()
          self.updateHeights()
          self.updateBalance()
          
        # left left case - rotate to right
        self.rotateRight()
        self.updateHeights()
        self.updateBalance()
      
      # right subtree is larger than left subtree
      if self.balance < -1:
        # right left case - rotate to right
        if self.node.right.balance > 0:
          self.node.right.rotateRight()
          self.updateHeights()
          self.updateBalance()
          
        # right right case - rotate to left
        self.rotateLeft()
        self.updateHeights()
        self.updateBalance()
     
  
  def updateHeights(self, recursive = True):
    
    if self.node:
      if recursive:
        if self.node.left:
          self.node.left.updateHeights()
        if self.node.right:
          self.node.right.updateHeights()
          
      self.height = 1 + max(self.node.left.height, self.node.right.height)
    else:
      self.height = -1
  
  
  def updateBalance(self, recursive = True):
    
    if self.node:
      if recursive:
        if self.node.left:
          self.node.left.updateBalance()
        if self.node.right:
          self.node.right.updateBalance()
          
      self.balance = self.node.left.height - self.node.right.height
    else:
      self.balance = 0
  
  
  # ROTATION
  def rotateLeft(self): #set self as the left subtree of right subtree
    
    newRoot = self.node.right.node
    newLeftSubtree = newRoot.left.node
    oldRoot = self.node
    
    self.node = newRoot
    oldRoot.right.node = newLeftSubtree
    newRoot.left.node = oldRoot
  
  
  def rotateRight(self): #set self as the right subtree of left subtree
    
    newRoot = self.node.left.node
    newLeftSubtree = newRoot.right.node
    oldRoot = self.node
    
    self.node = newRoot
    oldRoot.left.node = newLeftSubtree
    newRoot.right.node = oldRoot

        
  def display(self, node = None, level = 0):
    if not node:
      node = self.node
    
    if node.right.node:
      self.display(node.right.node, level + 1)
      print ('   ' * level), ('  /')
    
    print ('   ' * level), node
    
    if node.left.node:
      print ('   ' * level), ('  \\')
      self.display(node.left.node, level + 1)


tree = AVLTree()
data = list_of_nodes

for key in data:
  tree.insert(key)
  sys.stdout.write(BColors.RED)
  print '---- DISPLAY AVL TREE ----'
  sys.stdout.write(BColors.RESET)
  sys.stdout.write(BColors.CYAN)
  print('Insert key: ' + str(key))
  sys.stdout.write(BColors.RESET)
  sys.stdout.write(BColors.GREEN)
  tree.display()
  sys.stdout.write(BColors.RESET)
