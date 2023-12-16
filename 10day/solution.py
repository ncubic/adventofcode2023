import sys
sys.path.append("../aoc")
import tools
import random

sys.setrecursionlimit(100000)
lines = tools.getLines("10day/puzzle")

rules = {
  "|": {
    "n": ["|", "F", "7", "S"],
    "s": ["|", "L", "J", "S"]
  },
  "-": {
    "w": ["-", "F", "L", "S"],
    "e": ["-", "J", "7", "S"]
  },
  "F": {
    "e": ["-", "J", "7", "S"],
    "s": ["|", "L", "J", "S"]
  },
  "L": {
    "n": ["|", "F", "7", "S"],
    "e": ["-", "J", "7", "S"]
  },
  "7": {
    "w": ["-", "F", "L", "S"],
    "s": ["|", "L", "J", "S"]
  },
  "J": {
    "n": ["|", "F", "7", "S"],
    "w": ["-", "F", "L", "S"]
  },
  "S": {
    "n": ["|", "F", "7", "S"],
    "s": ["|", "L", "J", "S"],
    "w": ["-", "F", "L", "S"],
    "e": ["-", "J", "7", "S"]
  }
}

start = "S"
ground = "."

directions = ["n", "w", "e", "s"]

def randomElem(array):
  index = random.randint(0, len(array)-1)
  return array[index]

def getCoords(direction, x, y):
  if direction == "n":
    return (x-1, y)
  elif direction == "w":
    return (x, y-1)
  elif direction == "e":
    return (x, y+1)
  else:
    return (x + 1, y)

def getElem(matrix, x, y):
  if x >= len(matrix) or x < 0:
    return "B"
  
  row = matrix[x]
  if y < 0 or y >= len(row):
    return "B"
  
  return matrix[x][y]

def retrace(direction, prevDirection):
  if direction == "s" and prevDirection == "n":
    return True
  elif direction == "n" and prevDirection == "s":
    return True
  elif direction == "w" and prevDirection == "e":
    return True
  elif direction == "e" and prevDirection == "w":
    return True
  return False 

def worker(matrix, startX, startY):

  x = startX
  y = startY
  current = matrix[x][y]
  path = []
  guide = []
  prevDirection = ""

  while True:
    options = []

    for direction in directions:
      if retrace(direction, prevDirection):
        continue

      if not direction in rules[current]:
        continue

      nextCoords = getCoords(direction, x, y)
      nextElem = getElem(matrix, nextCoords[0], nextCoords[1])

      if nextElem in rules[current][direction]:
        options.append((direction, nextCoords))

    if len(options) == 0:
      break

    option = randomElem(options)
    prevDirection = option[0]
    x = option[1][0]
    y = option[1][1]
    current = matrix[x][y]
    path.append(current)
    guide.append(option[1])

    if current == "S":
      break
  
  return guide if current == "S" else []

start = (0, 0)
matrix = []
for i in range(len(lines)):
  line = lines[i]
  row = [*line.removesuffix("\n")]
  matrix.append(row)

  for j in range(len(row)):
    if row[j] == "S":
      start = (i, j)

solution = []
while True:
  solution = worker(matrix, start[0], start[1])
  if len(solution) > 0:
    break

print(f"part 1 solution is {int(len(solution)/2)}")

def inSolution(coord):
  for c in solution:
    if c[0] == coord[0] and c[1] == coord[1]:
      return True
  return False

def findBorderStart(matrix):
  for i in range(len(matrix)):
    row = matrix[i]
    if row[0] == ".":
      return (i, 0)
    elif row[-1] == ".":
      return (i, len(row)-1)
    elif i == 0 or i == len(matrix)-1:
      for j in range(len(row)):
        if row[j] == ".":
          return (i,j)
  return None

def trimWorker(matrix, current):
  x = current[0]
  y = current[1]

  matrix[x][y] = ""

  print(current)
  for direction in directions:
    nextCoord = getCoords(direction, x, y)
    nextElem = getElem(matrix, nextCoord[0], nextCoord[1])
    if nextElem not in [".", "G"]:
      continue
    
    trimWorker(matrix, nextCoord)

def expandRow(row):
  newRow = []
  for j in range(len(row)):
    elem = row[j]
    newRow.append(elem)
    if elem in ["-", "F", "L"]:
      newRow.append("-")
    elif elem == "S" and j < len(row) - 1 and row[j+1] in ["-", "J", "7"]:
      newRow.append("-")
    else:
      newRow.append("G")
  return newRow

def constructRow(row, nextRow):
  newRow = []
  for j in range(len(row)):
    elem = row[j]
    if elem in ["F", "7", "|"]:
      newRow.append("|")
    elif elem == "S" and nextRow != None and nextRow[j] in ["J", "L", "|"]:
      newRow.append("|")
    else:
      newRow.append("G")
  return newRow

def visualise(matrix):
  print("------------------")
  for i in range(len(matrix)):
    row = matrix[i]
    print(row)

  print("------------------")

visualise(matrix)

# cleanup rouge pipes
for i in range(len(matrix)):
  row = matrix[i]
  for j in range(len(row)):
    coord = (i, j)
    if not inSolution(coord):
      row[j] = "."

expandedMatrix = []
for row in matrix:
  expandedMatrix.append(expandRow(row))

matrix = []
for i in range(len(expandedMatrix)):
  row = expandedMatrix[i]
  nextRow = expandedMatrix[i+1] if i < len(expandedMatrix) - 1 else None
  matrix.append(row)
  matrix.append(constructRow(row, nextRow))

while True:
  start = findBorderStart(matrix)
  if start == None:
    break

  trimWorker(matrix, start)

visualise(matrix)

enclosed = 0
for row in matrix:
  for column in row:
    if column == ".":
      enclosed += 1

print(f"part 2 solution is {enclosed}")
