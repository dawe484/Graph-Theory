#!/usr/bin/python
import sys
import re

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


list_of_names = []
list_of_start_nodes = []
list_of_end_nodes = []

colors = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

def entry():
  for i in sys.stdin:

    entry_split = re.split('\W+', i)

    if entry_split[len(entry_split) - 1] == '':
      del entry_split[len(entry_split) - 1]

    for index in range(len(entry_split)):
      if entry_split[index] not in list_of_names:
        list_of_names.append(entry_split[index])

    for index in range(len(entry_split)):
      if len(entry_split) == 2:
        if index == 0:
          list_of_start_nodes.append(entry_split[index])
        elif index == 1:
          list_of_end_nodes.append(entry_split[index])


entry()


my_graph = {}
  
for i in range(len(list_of_start_nodes)):
  if list_of_start_nodes[i] in my_graph.keys():
    my_graph[list_of_start_nodes[i]].append(list_of_end_nodes[i])
  else:
    my_graph[list_of_start_nodes[i]] = [list_of_end_nodes[i]]
  
for i in range(len(list_of_end_nodes)):
  if list_of_end_nodes[i] in my_graph.keys():
    my_graph[list_of_end_nodes[i]].append(list_of_start_nodes[i])
  else:
    my_graph[list_of_end_nodes[i]] = [list_of_start_nodes[i]]


def check_valid(graph):
  for node, nexts in graph.iteritems():
    assert (nexts)  # no isolated node
    assert (node not in nexts)  # # no node linked to itself
    for next in nexts:
      assert (next in graph and node in graph[next])  # A linked to B implies B linked to A


class M_Graph:
  def __init__(self, graph):
    self.graph = graph
  
  def vertex_degree(self, vertex):
    """ The degree of a vertex is the number of edges connecting
        it, i.e. the number of adjacent vertices. Loops are counted 
        double, i.e. every occurence of vertex in the list 
        of adjacent vertices. """ 
    adj_vertices = self.graph[vertex]
    degree = len(adj_vertices) + adj_vertices.count(vertex)
    return degree

  def degree_sequence(self):
    """ calculates the degree sequence """
    seq = []
    for vertex in self.graph:
      seq.append(str(self.vertex_degree(vertex))+vertex)
    seq.sort(reverse=True)
    return seq

result = M_Graph(my_graph)

ds = result.degree_sequence()

nodes = []
d = {}
names = list_of_names
name_colors = []
res_names = []
res_colors = []
full_res_names = []
      
class MapColor:
  def __init__(self, graph, colors):
    check_valid(graph)
    self.graph = graph
#    nodes = list(self.graph.keys())
    for i in range(len(ds)):
      nodes.append(ds[i][1:])
    self.node_colors = dict([(node, None) for node in nodes])
    self.domains = dict([(node, set(colors)) for node in nodes])


  def solve(self):
#    uncolored_nodes = [n for n, c in self.node_colors.iteritems() if c is None]
    uncolored_nodes = nodes
    if not uncolored_nodes:
      return True

    node = uncolored_nodes[0]
    
    for color in self.domains[node]:
      if all(color != self.node_colors[n] for n in self.graph[node]):
        self.set_color(node, color)
        self.remove_from_domains(node, color)
        nodes.pop(0)

        if self.solve():
          return True

        self.set_color(node, None)
        self.add_to_domains(node, color)

    return False

  def set_color(self, key, color):
    self.node_colors[key] = color

  def remove_from_domains(self, key, color):
    for node in self.graph[key]:
      if color in self.domains[node]:
        self.domains[node].remove(color)

  def add_to_domains(self, key, color):
    for node in self.graph[key]:
      self.domains[node].add(color)
  
  def print_result(self):
    result = self.node_colors
    values = self.node_colors.values()
    
    for i in range(len(colors)):
      c = 0
      for j in range(len(values)):
        if colors[i] == values[j]:
          c += 1
      if c == 1:
        if colors[i] in values:
          name = self.node_colors.keys()[values.index(colors[i])]
          names.remove(name)
          for node in self.graph[name]:
            names.remove(node)
          if len(names) > 1:
            for ii in range(len(names)):
              if colors[i] in self.domains[names[ii]]:
                result[names[ii]] = colors[i]
                break

    chrom_number = 0
    
    for color in colors:
      if color in result.values():
        chrom_number += 1
    
    for i in range(len(result.values())):
      res_names.append(result.keys()[i])
      res_colors.append(result.values()[i])

    for i in range(chrom_number):
      n = i+1
      full_res_names = []
      for j in range(len(res_colors)):
        if n == int(res_colors[j]):
          full_res_names.append(res_names[j])
      for a in range(len(full_res_names)):
        if a < len(full_res_names)-1:
          sys.stdout.write(BColors.GREEN)
          sys.stdout.write(full_res_names[a] + ', ')
        if a == len(full_res_names)-1:
          sys.stdout.write(full_res_names[a])
          sys.stdout.write(BColors.RESET)
      print


problem = MapColor(my_graph, colors)

problem.solve()
problem.print_result()
