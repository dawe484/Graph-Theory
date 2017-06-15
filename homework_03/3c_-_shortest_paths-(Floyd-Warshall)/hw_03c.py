import re
import sys
from itertools import izip


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
matrix = []

#graph = {
#    'a': {'b': -2, 'c': 3},
#    'b': {'c': -4, 'd': 1},
#    'c': {'b': 4, 'd': 3},
#    'd': {'a': 4}
#}

def entry():

  for inp in sys.stdin:

#    sys.stdout.write(BColors.MAGENTA)
#    sys.stdout.write(inp)
#    sys.stdout.write(BColors.RESET)
#    print
    
    c = inp[0]
    
    count_end_nodes = 0
    for i in range(len(inp)):
      if inp[i].isalpha():
        if i == 0:
          if inp[i] not in list_of_nodes:
            list_of_nodes.append(inp[i])
        if i > 0:
          list_of_end_nodes.append(inp[i])
          count_end_nodes += 1
      if inp[i].isdigit():
        if inp[i-1] == '-':
          if inp[1] == '+':
            t = -int(inp[i])
            t += 1
            cost.append(t)
          else:
            t = -int(inp[i])
            cost.append(t)
        else:
          if inp[1] == '+':
            cost.append(int(inp[i])+1)
          else:
            cost.append(int(inp[i]))
#    print 'cost', cost
    
    for i in range(count_end_nodes):
      list_of_start_nodes.append(c)
  
  for i in range(len(list_of_start_nodes)):
    if list_of_start_nodes[i] in list_of_nodes:
      src_nodes.append(list_of_nodes.index(list_of_start_nodes[i]))
      dest_nodes.append(list_of_nodes.index(list_of_end_nodes[i]))

  # matrix
  m = [[0] * len(list_of_nodes) for i in range(len(list_of_nodes))]
  
  for i in range(len(src_nodes)):
    #for j in range(len(src_nodes)):
    m[src_nodes[i]][dest_nodes[i]] = int(cost[i])
 
  # Number of vertices in the graph
  V = len(list_of_nodes)

  INF = 999999

  # Solves all pair shortest path using Floyd Warshall Algrorithm
  def floydWarshall(graph):

    matrix = [[i for i in line] for line in graph]

    for k in range(V):
      for i in range(V):
        for j in range(V):
          if (matrix[i][k] != INF & matrix[k][j] != INF & matrix[i][k] + matrix[k][j] < matrix[i][j]):
            matrix[i][j] = matrix[i][k] + matrix[k][j]
    
    graph = {}
  
    for i in range(len(src_nodes)):
      if src_nodes[i] in graph.keys():
        graph[src_nodes[i]].append(dest_nodes[i])
      else:
  #      print(str(src_nodes[i]), str(dest_nodes[i]))
        graph[src_nodes[i]] = [dest_nodes[i]]

    def find_all_paths(graph, start, end, path=[]):
      #http://www.python.org/doc/essays/graphs/
      path = path + [start]
      if start == end:
        return [path]
      if not graph.has_key(start):
        return []
      paths = []
      for node in graph[start]:
        if node not in path:
          newpaths = find_all_paths(graph, node, end, path)
          for newpath in newpaths:
            paths.append(newpath)
      return paths

    def find_paths(graph):
      cycles=[]
      for startnode in graph:
        for endnode in graph:
          newpaths = find_all_paths(graph, startnode, endnode)
          for path in newpaths:
            if (len(path)==len(graph)):                    
              cycles.append(path)
      return cycles

    a = find_paths(graph)
    
    max_price = -1
    max_price_path = []

    for any in a:
      price = 0
      # sys.stdout.write(str(any) + ' = ')
      for i in range(len(any)-1):
        t = i+1
        price += matrix[any[i]][any[t]]
#      print price
      if price > max_price:
        max_price = price
        max_price_path = []
        max_price_path.append(any)
      elif price == max_price:
        max_price_path.append(any)

    for any in max_price_path:
      for i in range(len(any)):
        if i < (len(any)-1):
          sys.stdout.write(BColors.GREEN)
          sys.stdout.write(list_of_nodes[any[i]] + ' - ')
        if i == (len(any)-1):
          sys.stdout.write(list_of_nodes[any[i]] + ': ')
      print max_price
      sys.stdout.write(BColors.RESET)

  my_graph = []
  
  line = [INF] * len(list_of_nodes)
  
  # zeros on diagonal in my_graph matrix
  for i in range(len(list_of_nodes)):
    line[i] = 0
#    print 'line', line
    my_graph.append(line)
    line = [INF] * len(list_of_nodes)
  
  for i in range(len(list_of_nodes)):
    for j in range(len(list_of_start_nodes)):
      if list_of_nodes[i] == list_of_start_nodes[j]:
        v = list_of_end_nodes[j]
        index = list_of_nodes.index(v)
        my_graph[i][index] = cost[j]

  # Print the solution
  floydWarshall(my_graph);
  
entry()
