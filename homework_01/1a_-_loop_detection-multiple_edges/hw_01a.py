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

dictSklady = {}

def vstup():

    smycka = 'ne'
    cesta = []

    for i in sys.stdin:

        if re.match('^[A-Z]', i):
            vstupsplit = re.split('\W+', i)

            if vstupsplit[len(vstupsplit) - 1] == '':
                del vstupsplit[len(vstupsplit) - 1]

            for index in range(len(vstupsplit)):
                sklad = vstupsplit[index]
                dictSklady[sklad] = 0

        elif re.match('^[a-z]', i):
            vstupsplit = re.split('\W+', i)

            if vstupsplit[len(vstupsplit) - 1] == '':
                del vstupsplit[len(vstupsplit) - 1]

            del vstupsplit[0]

            for index in range(len(vstupsplit)):
                dictSklady[vstupsplit[index]] += 1

            if vstupsplit[0] == vstupsplit[len(vstupsplit)-1]:
                smycka = 'ano'

            for index in range(len(vstupsplit)):
                if index < len(vstupsplit)-2:
                    cesta.append(str(vstupsplit[index]) + ' ' + str(vstupsplit[index+1]))
                elif index == len(vstupsplit)-1:
                    cesta.append(str(vstupsplit[index-1]) + ' ' + str(vstupsplit[index]))

    m = [key for key, val in dictSklady.iteritems() if val == max(dictSklady.values())]

    sys.stdout.write(BColors.GREEN)
    sys.stdout.write("nejvice navstevovany: ")
    for i in range(len(m)):
        if i != len(m)-1:
            sys.stdout.write(m[i] + ', ')
        else:
            sys.stdout.write(m[i] + ' ')

    print max(dictSklady.values())

    nasobnehrany = [x for x in cesta if cesta.count(x) >= 2]

    if nasobnehrany:
        sys.stdout.write("existuje vice spojeni: ano" + '\n')
    else:
        sys.stdout.write("existuje vice spojeni: ne" + '\n')

    if smycka == 'ano':
        sys.stdout.write("zbozi zpet do skladu: " + smycka + '\n')
    else:
        sys.stdout.write("zbozi zpet do skladu: " + smycka + '\n')
    sys.stdout.write(BColors.RESET)

vstup()
