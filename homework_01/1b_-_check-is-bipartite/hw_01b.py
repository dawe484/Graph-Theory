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

  # BACKGROUND
  BBLACK = '\033[40m'
  BRED = '\033[41m'
  BGREEN = '\033[42m'
  BYELLOW = '\033[43m'
  BBLUE = '\033[44m'
  BMAGENTA = '\033[45m'
  BCYAN = '\033[46m'
  BWHITE = '\033[47m'
  BRESET = '\033[49m'

  # SPECIAL
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

queue = []
skupina1 = []
skupina2 = []
p = []
colorArr = []

ne = 'Nelze rozdelit.'

def vstup():

  for i in sys.stdin:

    vstupsplit = re.split('\W+', i)

    if vstupsplit[len(vstupsplit) - 1] == '':
      del vstupsplit[len(vstupsplit) - 1]
    
    if len(vstupsplit) == 1:
      sys.stdout.write(BColors.RED)
      print ne
      sys.stdout.write(BColors.RESET)
      #sys.exit() #will terminate all python scripts
      quit() #only terminates the script which spawned it
    
    if len(vstupsplit) > 2:
      for index in range(len(vstupsplit)):
        firstline = vstupsplit
        p.append(index)
        w = len(p)
        graph = [[0 for x in range(w)] for y in range(w)]

    if len(vstupsplit) == 2:
      for index in range(len(vstupsplit)):
        if vstupsplit[index] in firstline:
          if index == 0:
            x = firstline.index(vstupsplit[index])
          elif index == 1:
            y = firstline.index(vstupsplit[index])
            graph[x][y] = 1
            graph[y][x] = 1
    
  numberOfVertices = len(graph[0])
  
  def isBipartite(graph, indexOfFirstVertex):
    
    colorArr = [-1 for x in range(numberOfVertices)];
    
    # Assing first color to the firstVertex
    colorArr[indexOfFirstVertex] = 1
    
    # For every vertex in graph test color (Similar to BFS)
    for index in range(len(colorArr)):
      u = index
      # Find all non-colored adjacent vertices
      for v in range(numberOfVertices):
        # An edge from u to v exists and destination v is not colored
        if (graph[u][v] == 1 and colorArr[v] == -1):
          # Assign alternate color to this adjacent v of u
          colorArr[v] = 1-abs(colorArr[u])
          queue.append(v)
        # An edge from u to v exists and destination v is colored with same color as u
        elif (graph[u][v] == 1 and colorArr[v] == colorArr[u]):
          return False

    # If we reach here, then all adjacent vertices can be colored with alternate color
    for index in range(len(colorArr)):
      #print colorArr[index]
      if colorArr[index] == 1:
        skupina1.append(firstline[index])
      if colorArr[index] == 0:
        skupina2.append(firstline[index])
        
    for index in range(len(skupina1)):
      if index < len(skupina1)-1:
        sys.stdout.write(BColors.GREEN)
        sys.stdout.write(skupina1[index]+', ')
      elif index == len(skupina1)-1:
        print skupina1[index]
        sys.stdout.write(BColors.RESET)
        
    for index in range(len(skupina2)):
      if index < len(skupina2)-1:
        sys.stdout.write(BColors.GREEN)
        sys.stdout.write(skupina2[index]+', ')
      elif index == len(skupina2)-1:
        print skupina2[index]
        sys.stdout.write(BColors.RESET)
    
    return True
  # end function isBipartite
  
  b = isBipartite(graph, graph[0][0])
  
  if (b):
    sys.stdout.write('')
  else:
    sys.stdout.write(BColors.RED)
    print ne
    sys.stdout.write(BColors.RESET)

vstup()
