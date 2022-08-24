import re

# FUNCION 1 - parsea los pesos wis segun un output y los guarda en res

# pattern = '\[(-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*, (-)*\d\.(\d)*\]'
# f = open('empty3.txt', "r")
# res = open('res.txt', "w")
# content = f.read()
# i = 0
# for object in re.finditer(pattern, content):
#   if i<1:
#     for value in object.group(0).strip('][').split(', '):
#       res.write(str(value)+"\n")
#   i = (i + 1) % 2

# FIN FUNCION 1 ------------------------------

# FUNCION 2 - parsea winrate segun un output y lo imprime

# indexes = []
# winrate = []

# pattern = '----------\w'
# f = open('empty5.txt', "r")
# content = f.read()
# i = 1
# wins = 0
# for object in re.finditer(pattern, content):
#   indexes.append(i)
#   if object.group(0)[-1] == 'L':
#     wins+=1
#     winrate.append((wins/i)*100)
#     i+=1
#   else:
#     winrate.append((wins/i)*100)
#     i+=1

# print(winrate)

# FIN FUNCION 2 ------------------------------

# FUNCION 3 - imprime arreglo de winrates segun un performance resultado de test.py

indexes = []
winrate = []

pattern = 'Game over with reward 0.'
f = open('perfnovis2.txt', "r")
content = f.read()
i = 1
wins = 0
for object in re.finditer(pattern, content):
  indexes.append(i)
  if object.group(0)[-1] == '.':
    wins+=1
    winrate.append((wins/i)*100)
    i+=1
  else:
    winrate.append((wins/i)*100)
    i+=1

print(winrate)