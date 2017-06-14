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

spolupracujes = []
jespolupracovnikem = []
pracovnici = []
mnozinapracovniku = []

def vstup():
    for i in sys.stdin:

        vstupsplit = re.split('\W+', i)

        if vstupsplit[len(vstupsplit) - 1] == '':
            del vstupsplit[len(vstupsplit) - 1]

        pracovnik1 = vstupsplit[0]
        pracovnik2 = vstupsplit[1]

        spolupracujes.append(pracovnik1)
        jespolupracovnikem.append(pracovnik2)

        for j in range(len(vstupsplit) - 1):
            pracovnici.append(vstupsplit[j])

    mnozinapracovniku = list(set(pracovnici))

    matrix = [[0] * len(mnozinapracovniku) for i in range(len(mnozinapracovniku))]

    for i in range(len(mnozinapracovniku)):
        for j in range(len(jespolupracovnikem)):
            if mnozinapracovniku[i] == jespolupracovnikem[j]:
                for m in range(len(mnozinapracovniku)):
                    if mnozinapracovniku[m] == spolupracujes[j]:
                        matrix[i][m] = 1

    for i in range(len(mnozinapracovniku)):
        for j in range(len(spolupracujes)):
            if mnozinapracovniku[i] == spolupracujes[j]:
                for m in range(len(mnozinapracovniku)):
                    if mnozinapracovniku[m] == jespolupracovnikem[j]:
                        matrix[i][m] = 1

    graph = matrix

    def n(vertex):
        c = 0
        l = []
        for i in graph[vertex]:
            if i == 1:
                l.append(c)
            c += 1
        return l

    # Bron-Kerbosch algoritmus rekurzivně
    # vychází z: http://stackoverflow.com/questions/13904636/implementing-bron-kerbosch-algorithm-in-python
    # upraven pro potřebu zadaní příkladu (modify from homework)

    def bronk(r, p, x, pole):
        vysl = []
        for i in range(len(r)):
            if r[i] not in pole:
                pole.append(r[i])
                if len(p) == 0 and len(x) == 0:
                    for i in range(len(r)):
                        vysl.append(mnozinapracovniku[r[i]])

                    sys.stdout.write(BColors.GREEN)
                    for i in range(len(vysl)):
                        if i != len(vysl)-1:
                            sys.stdout.write(vysl[i] + ', ')
                        else:
                            sys.stdout.write(vysl[i] + '\n')
                    sys.stdout.write(BColors.RESET)
                    return
        for vertex in p[:]:
            r_new = r[::]
            r_new.append(vertex)
            p_new = [val for val in p if val in n(vertex)]  # p intersects n(vertex)
            x_new = [val for val in x if val in n(vertex)]  # x intersects n(vertex)
            bronk(r_new, p_new, x_new, pole)
            p.remove(vertex)
            x.append(vertex)

    bronk([], range(len(mnozinapracovniku)), [], [])

vstup()
