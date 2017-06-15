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
cost = []
src_nodes = []
dest_nodes = []
  
class Graph:

  def __init__(self,vertices):
    self.V= vertices
    self.graph = []

  def addEdge(self,u,v,w):
    self.graph.append([u,v,w])

  # A utility function to find set of an element i (uses path compression technique)
  def find(self, parent, i):
    if parent[i] == i:
      return i
    return self.find(parent, parent[i])

  # A function that does union of two sets of x and y (uses union by rank)
  # https://en.wikipedia.org/wiki/Disjoint-set_data_structure
  def union(self, parent, rank, x, y):
    xroot = self.find(parent, x)
    yroot = self.find(parent, y)

    # Attach smaller rank tree under root of high rank tree (union by rank)
    if rank[xroot] < rank[yroot]:
      parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
      parent[yroot] = xroot
    # If ranks are same, then make one as root and increment its rank by one
    else :
      parent[yroot] = xroot
      rank[xroot] += 1

  # The main function to construct MST using Kruskal's algorithm
  def KruskalMST(self):

    result =[] #This will store the resultant MST

    i = 0 # An index variable, used for sorted edges
    e = 0 # An index variable, used for result[]

    # Step 1:  Sort all the edges in non-decreasing order of their weight.
    self.graph = sorted(self.graph, key=lambda item: item[2])

    parent = []
    rank = []

    # Create V subsets with single elements
    for node in range(self.V):
      parent.append(node)
      rank.append(0)

    # Number of edges to be taken is equal to V-1
    while e < self.V-1:
      # Step 2: Pick the smallest edge and increment the index for next iteration
      u, v, w =  self.graph[i]
      i = i + 1
      x = self.find(parent, u)
      y = self.find(parent ,v)

      # If including this edge does't cause cycle, include it in result and increment the index of result for next edge
      if x != y:
        e = e + 1  
        result.append([u,v,w])
        self.union(parent, rank, x, y)          

    result_weight = 0
    # print the contents of result[] to display the built MST
    for u, v, weight in result:
      result_weight += weight
      sys.stdout.write(BColors.GREEN)
      print str(list_of_nodes[u]), "-", str(list_of_nodes[v]) + ": " + str(weight)
    print 'Hodnoceni:', result_weight
    sys.stdout.write(BColors.RESET)

def entry():

  for i in sys.stdin:

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
      elif index == 2:
        cost.append(entry_split[index])

  for i in range(len(list_of_start_nodes)):
    if list_of_start_nodes[i] in list_of_nodes:
      src_nodes.append(list_of_nodes.index(list_of_start_nodes[i]))
      dest_nodes.append(list_of_nodes.index(list_of_end_nodes[i]))

  g = Graph(len(list_of_nodes))
  for index in range(len(cost)):
    g.addEdge(src_nodes[index], dest_nodes[index], int(cost[index]))

  g.KruskalMST()

entry()
