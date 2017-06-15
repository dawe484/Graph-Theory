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
cost = []
src_nodes = []
dest_nodes = []
matrix = []


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

  graph = {}
  
  for i in range(len(src_nodes)):
    if src_nodes[i] in graph.keys():
      graph[src_nodes[i]].append(dest_nodes[i])
    else:
#      print(str(src_nodes[i]), str(dest_nodes[i]))
      graph[src_nodes[i]] = [dest_nodes[i]]
    
#  print '   graph', graph

  matrix = [[0] * len(list_of_nodes) for i in range(len(list_of_nodes))]
#  print '---- Matrix ----'
#  print matrix of zeros
#  for i in range(len(matrix)):
#    for j in range(len(matrix)):
#      sys.stdout.write(str(matrix[i][j]))
#    print
  
  for i in range(len(src_nodes)):
    #for j in range(len(src_nodes)):
    matrix[src_nodes[i]][dest_nodes[i]] = int(cost[i])
  
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
        # print 'startnode:', startnode, 'endnode', endnode
        newpaths = find_all_paths(graph, startnode, endnode)
        for path in newpaths:
          # print 'path', path
          if (len(path)==len(graph)):                    
            cycles.append(path)
    return cycles

  a = find_paths(graph)

  min_price = 'inf'
  min_price_path = []

  for any in a:
#    print 'any', any
    price = 0
    # sys.stdout.write(str(any) + ' = ')
    for i in range(len(any)-1):
      t = i+1
      price += matrix[any[i]][any[t]]
    # print price
    if price < min_price:
      min_price = price
      min_price_path = []
      min_price_path.append(any)
    elif price == min_price:
      min_price_path.append(any)
#  print min_price_path
#  print min_price
#  print list_of_nodes

  for any in min_price_path:
    for i in range(len(any)):
      if i < (len(any)-1):
        sys.stdout.write(BColors.GREEN)
        sys.stdout.write(list_of_nodes[any[i]] + ' - ')
      if i == (len(any)-1):
        sys.stdout.write(list_of_nodes[any[i]] + ': ')
    print min_price
    sys.stdout.write(BColors.RESET)
  

entry()
