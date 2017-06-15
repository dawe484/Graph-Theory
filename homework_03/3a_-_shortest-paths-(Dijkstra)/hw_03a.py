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
my_list = []

for i in sys.stdin:

  entry_split = re.split('\W+', i)

  if entry_split[len(entry_split) - 1] == '':
    del entry_split[len(entry_split) - 1]

  # sys.stdout.write(BColors.MAGENTA)
  # print entry_split
  # sys.stdout.write(BColors.RESET)

  my_list.append(entry_split)
  for index in range(len(entry_split)):
    if (index <= 1) & (entry_split[index] not in list_of_nodes):
        list_of_nodes.append(entry_split[index])

def make_link(G, node1, node2, dist):
  if node1 not in G:
    G[node1] = {}
  (G[node1])[node2] = dist
  if node2 not in G:
    G[node2] = {}
  (G[node2])[node1] = dist
  return G

G = {}

for (i, j, k) in my_list:
  make_link(G, i, j, k)

def shortest_dist_node(dist):
  best_node = 'undefined'
  best_value = 100000
  for v in dist:
    if dist[v] < best_value:
      (best_node, best_value) = (v, dist[v])
  return best_node


def dijkstra(G, v):
  dist_so_far = {v: 0}
  final_dist = {}
  while len(final_dist) < len(G):
    w = shortest_dist_node(dist_so_far)
    final_dist[w] = dist_so_far[w]
    del dist_so_far[w]
    for x in G[w]:
      if x not in final_dist:
        if x not in dist_so_far:
          dist_so_far[x] = final_dist[w] + int(G[w][x])
        elif final_dist[w] + int(G[w][x]) < dist_so_far[x]:
          dist_so_far[x] = final_dist[w] + int(G[w][x])
  return final_dist

a = list_of_nodes[0]

dijkstr = dijkstra(G, a)

for i in range(len(dijkstra(G, a))):
  vysl = min(dijkstr.items(), key=lambda x: x[1])
  sys.stdout.write(BColors.GREEN)
  print vysl[0] + ':', vysl[1]
  sys.stdout.write(BColors.RESET)
  del dijkstr[vysl[0]]
