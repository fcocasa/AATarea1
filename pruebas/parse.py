# # parsea los pesos wis segun un output y los guarda en res

# import re

# pattern = '\[(-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*\]'
# filename = 'pruebas/4rooms3de60'
# f = open(filename+'.txt', "r")
# res = open(filename+'wi.txt', "w")
# content = f.read()
# i = 0
# for object in re.finditer(pattern, content):
#     if i < 1:
#         for value in object.group(0).strip('][').split(', '):
#             res.write(str(value)+"\n")
#     i = (i + 1) % 2

# ---------------

# parsea winrate segun un output y lo imprime

import re

# indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
#            31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
indexes = []
winrate = []

#pattern = '----------\w'
pattern = 'Game over with reward 0.'
filename = 'testoutput'
f = open(filename+'.txt', "r")
content = f.read()
i = 1
wins = 0
for object in re.finditer(pattern, content):
    if object.group(0)[-1] == '.':
        wins += 1
        winrate.append((wins/i)*100)
        i += 1
    else:
        winrate.append((wins/i)*100)
        i += 1

print(winrate)
