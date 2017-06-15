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


# !/usr/bin/env python
#
# http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm
# Ford-Fulkerson algorithm computes max flow in a flow network.
# prevzato z: https://github.com/bigbighd604/Python/blob/master/graph/Ford-Fulkerson.py
# upraveno pro nas priklad, ale princip algoritmu zachovan
#

graph = []
list_of_keys = []
list_of_lastkeys = []
list_of_flowkeys = []
list_of_doors = []
list_of_rooms = []
start = []


def entry():
  for i in sys.stdin:

    entry_split = re.split('\W+', i)

    if entry_split[len(entry_split) - 1] == '':
        del entry_split[len(entry_split) - 1]

    if entry_split[0].startswith('M', 0, 2):
      start.append(entry_split[0])
      start.append(entry_split[1])
      # print 'start', start

    for index in range(len(entry_split)):
      if str(entry_split[index]).startswith('D', 0, 2):
        graph.append(str(entry_split[index + 1]) + ' > ' + str(entry_split[index + 2]) + ' ' + str(
          entry_split[index + 3]))

    for index in range(len(entry_split)):
      if str(entry_split[index]).startswith('D', 0, 2):
        list_of_doors.append(str(entry_split[index]))

    for index in range(len(entry_split)):
      if str(entry_split[index]).startswith('M', 0, 2):
        if str(entry_split[index]) not in list_of_rooms:
          list_of_rooms.append(str(entry_split[index]))

  for index in range(len(entry_split)):
    if str(entry_split[index]).startswith('E', 0, 3):
      if str(entry_split[index]) not in list_of_rooms:
        list_of_rooms.append(str(entry_split[index]))


class Edge(object):
  def __init__(self, u, v, w):
    self.source = u
    self.target = v
    self.capacity = w

  def __repr__(self):
    return "%s > %s %s" % (self.source, self.target, self.capacity)


class FlowNetwork(object):
  def __init__(self):
    self.adj = {}
    self.flow = {}

  def addvertex(self, vertex):
    self.adj[vertex] = []

  def getedges(self, v):
    return self.adj[v]

  def addedge(self, u, v, w=0):
    if u == v:
      raise ValueError("u == v")
    edge = Edge(u, v, w)
    redge = Edge(v, u, 0)
    edge.redge = redge
    redge.redge = edge
    self.adj[u].append(edge)
    self.adj[v].append(redge)
    # Intialize all flows to zero
    self.flow[edge] = 0
    self.flow[redge] = 0

  def findpath(self, source, target, path):
    if source == target:
      return path
    for edge in self.getedges(source):
      residual = edge.capacity - self.flow[edge]
      if residual > 0 and not (edge, residual) in path:
        result = self.findpath(edge.target, target, path + [(edge, residual)])
        if result != None:
          return result

  def maxflow(self, source, target):
      path = self.findpath(source, target, [])
      while path != None:
        flow = min(res for edge, res in path)
        for edge, res in path:
          self.flow[edge] += flow
          self.flow[edge.redge] -= flow
        for key in self.flow:
          continue
        path = self.findpath(source, target, [])
      for key in self.flow:
        if self.flow[key] >= 0:
          list_of_keys.append(str(key))
          list_of_flowkeys.append(str(self.flow[key]))
          if str(key)[len(str(key)) - 2] == ' ':
            list_of_lastkeys.append(str(key)[-1:])
          else:
            list_of_lastkeys.append(str(key)[-2:])

      return sum(self.flow[edge] for edge in self.getedges(source))


if __name__ == "__main__":
  exit_count = 0
  entry()
  g = FlowNetwork()
  for i in range(len(list_of_rooms)):
    g.addvertex(list_of_rooms[i])

  for j in range(len(graph)):
    length = len(graph[j])
    temp = graph[j]
    m1 = temp[:3]
    if temp[6] == 'E':
      m2 = temp[6:10]
      exit_count += 1
    else:
      m2 = temp[6:9]
    if str(temp)[len(temp) - 2] == ' ':
      t = temp[-1:]
    else:
      t = temp[-2:]
    g.addedge(str(m1), str(m2), int(t))

  result = g.maxflow(start[0], 'EXIT')

  sys.stdout.write(BColors.GREEN)
  sys.stdout.write('Group size: ' + str(result) + '\n')

  for i in range(len(graph)):
    if graph[i] in list_of_keys:
      if list_of_lastkeys[list_of_keys.index(graph[i])] == list_of_flowkeys[list_of_keys.index(graph[i])]:
        sys.stdout.write(
          str(list_of_doors[i]) + ': ' + str(list_of_flowkeys[list_of_keys.index(graph[i])]) + ' !\n')
      else:
        sys.stdout.write(
          str(list_of_doors[i]) + ': ' + str(list_of_flowkeys[list_of_keys.index(graph[i])]) + '\n')

  time = int(start[1]) / result * exit_count

  sys.stdout.write('Time: ' + str(time) + '\n')
  sys.stdout.write(BColors.RESET)
