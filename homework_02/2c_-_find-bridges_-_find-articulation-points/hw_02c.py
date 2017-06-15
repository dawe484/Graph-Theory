import re
import sys
from collections import defaultdict

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

  # SPECIAL
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  
list_of_nodes = []
list_of_start_nodes = []
list_of_end_nodes = []
src_nodes = []
dest_nodes = []
  
class Graph:
  
  def __init__(self,vertices):
    self.V= vertices
    self.graph = defaultdict(list)
    self.Time = 0

  def addEdge(self,u,v):
      self.graph[u].append(v)
      self.graph[v].append(u)
  
  # recursive function that finds bridges in an undirected graph
  # u - vertex to be visited next
  # visited[] - list of visited nodes
  # parent[] - parent vertices in DFS tree
  # disc[] - time of visited nodes
  def findBridgeHelper(self,u, visited, parent, low, disc):

    children = 0 #number of children in current node 

    visited[u] = True #mark current node as visited

    # init discovery time and low value
    disc[u] = self.Time
    low[u] = self.Time
    self.Time += 1

    for v in self.graph[u]:
      # If v is not visited yet, then make it a child of u in DFS tree and recur for it
      if visited[v] == False :
        parent[v] = u
        children += 1
        self.findBridgeHelper(v, visited, parent, low, disc)

        # Check if the subtree rooted with v has a connection to one of the ancestors of u
        low[u] = min(low[u], low[v])

        # If the lowest vertex reachable from subtree under v is below u in DFS tree, then u-v is a bridge
        if low[v] > disc[u]:
          sys.stdout.write(BColors.GREEN)
          print list_of_nodes[u], '-', list_of_nodes[v]
          sys.stdout.write(BColors.RESET)
            
      elif v != parent[u]: #update low value of u for parent
        low[u] = min(low[u], disc[v])

  # DFS based function to find all bridges. It uses recursive function findBridgeHelper()
  def findAllBridges(self):

    # Mark all the vertices as not visited and init parent and visited, and ap (articulation point) arrays
    visited = [False] * (self.V)
    disc = [float("Inf")] * (self.V)
    low = [float("Inf")] * (self.V)
    parent = [-1] * (self.V)

    # Call the recursive helper function to find bridges in DFS tree rooted with vertex 'i'
    for i in range(self.V):
      if visited[i] == False:
        self.findBridgeHelper(i, visited, parent, low, disc)

  # recursive function that finds articulation points (ap) in an undirected graph using DFS traversal
  # u - vertex to be visited next
  # visited[] - list of visited nodes
  # parent[] - parent vertices in DFS tree
  # disc[] - time of visited nodes
  # ap[] - store articulation points
  def findAPHelper(self,u, visited, ap, parent, low, disc):
    
    children = 0 #number of children in current node 

    visited[u] = True #mark current node as visited

    # init discovery time and low value
    disc[u] = self.Time
    low[u] = self.Time
    self.Time += 1

    for v in self.graph[u]:
      # If v is not visited yet, then make it a child of u in DFS tree and recur for it
      if visited[v] == False :
        parent[v] = u
        children += 1
        self.findAPHelper(v, visited, ap, parent, low, disc)

        # Check if the subtree rooted with v has a connection to one of the ancestors of u
        low[u] = min(low[u], low[v])

        # u may be an articulation point if u is root of DFS tree and has two or more chilren
        if parent[u] == -1 and children > 1:
          ap[u] = True

        # If u is not root and low value of one of its child is more than discovery value of u.
        if parent[u] != -1 and low[v] >= disc[u]:
          ap[u] = True

      elif v != parent[u]: # update low value of u for parent
        low[u] = min(low[u], disc[v])
 
  #The function to do DFS traversal. It uses recursive findAPHelper()
  def findAP(self):
    # Mark all the vertices as not visited and init parent and visited, and ap (articulation point) arrays
    visited = [False] * (self.V)
    disc = [float("Inf")] * (self.V)
    low = [float("Inf")] * (self.V)
    parent = [-1] * (self.V)
    ap = [False] * (self.V)

    # Call the recursive helper function to find articulation points in DFS tree rooted with vertex 'i'
    for i in range(self.V):
      if visited[i] == False:
        self.findAPHelper(i, visited, ap, parent, low, disc)

    for index, value in enumerate (ap):
      if value == True:
        sys.stdout.write(BColors.GREEN)
        print list_of_nodes[index]
        sys.stdout.write(BColors.RESET)

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
        if entry_split[index] not in list_of_nodes:
          list_of_nodes.append(entry_split[index])
    
    for index in range(len(entry_split)):
      if index == 0:
        list_of_start_nodes.append(entry_split[index])
      elif index == 1:
        list_of_end_nodes.append(entry_split[index])

  for i in range(len(list_of_start_nodes)):
    if list_of_start_nodes[i] in list_of_nodes:
      src_nodes.append(list_of_nodes.index(list_of_start_nodes[i]))
      dest_nodes.append(list_of_nodes.index(list_of_end_nodes[i]))
      
  g = Graph(len(list_of_nodes))
  for index in range(len(src_nodes)):
    g.addEdge(src_nodes[index], dest_nodes[index])
    
  g.findAllBridges()
  g.findAP()

entry()