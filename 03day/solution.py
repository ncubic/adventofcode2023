from functools import reduce
import sys
sys.path.append("../aoc")
import tools

lines = tools.getLines("03day/puzzle")

matrix = []

row = 0
for line in lines:
  matrix.append([])

  for char in line:
    matrix[row].append(char)

  row += 1

numbers = []

linesCount = len(matrix)
columnsCount = len(matrix[0])

def isSymbol(c):
  return not c.isdigit() and c != "." and c != "\n"

def getElement(i, j):
  return matrix[i][j] if i >= 0 and i < linesCount and j >= 0 and j < columnsCount else "0"

def checkSymbolNeighbours(i, j):
  ul = getElement(i-1, j-1)
  if isSymbol(ul):
    return True
  uu = getElement(i-1, j)
  if isSymbol(uu):
    return True
  ur = getElement(i-1,j+1)
  if isSymbol(ur):
    return True
  
  l = getElement(i, j-1)
  if isSymbol(l):
    return True
  r = getElement(i, j+1)
  if isSymbol(r):
    return True

  dl = getElement(i + 1, j - 1)
  if isSymbol(dl):
    return True
  dd = getElement(i + 1, j)
  if isSymbol(dd):
    return True
  dr = getElement(i + 1, j + 1)
  if isSymbol(dr):
    return True
  
  return False


def checkFollowingNumber(i, j):
  return False if j >= columnsCount else matrix[i][j].isdigit()

gearCoordinates = []

i = 0
for row in matrix:
  j = 0
  charBuffer = []
  addToNumbers = False
  for column in row:
    if column.isdigit():
      hasSymbolNeighbour = checkSymbolNeighbours(i, j)
      
      charBuffer.append(column)

      if hasSymbolNeighbour:
        addToNumbers = True
    elif (not addToNumbers) and len(charBuffer) > 0:
      charBuffer = []

    hasFollowingNumber = checkFollowingNumber(i, j)

    if (not hasFollowingNumber) and addToNumbers and len(charBuffer) > 0:
      num = int(reduce(lambda a, b : a + b, charBuffer))
      numbers.append(num)

      charBuffer = []
      addToNumbers = False

    if column == "*":
      gearCoordinates.append((i, j))
  
    j += 1
  
  i += 1

solution = reduce(lambda a, b : a + b, numbers)
print(f"Sum of parts is {solution}")

def getNumber(i, j):
  return matrix[i][j] if i >= 0 and i < linesCount and j >= 0 and j < columnsCount and matrix[i][j].isdigit() else None

def constructNumberLeft(i, j):
  num = getNumber(i,j)

  if num == None:
    return ""
  
  return constructNumberLeft(i,j-1) + num

def constructNumberRight(i, j):
  num = getNumber(i,j)

  if num == None:
    return ""
  
  return num + constructNumberRight(i,j+1)

def constructNumber(i, j):
  num = getNumber(i, j)

  if num == None:
    return ""
  
  return constructNumberLeft(i,j-1) + num + constructNumberRight(i,j+1)

def addToCandidates(candidates, num):
  if num.isdigit():
    candidates.append(int(num))

gearRatioSum = 0

for coord in gearCoordinates:
  (i, j) = coord

  candidates = []

  uln = constructNumber(i-1, j-1)
  addToCandidates(candidates, uln)
  uu = constructNumber(i-1, j) if getNumber(i-1, j-1) == None else ""
  addToCandidates(candidates, uu)
  urn = constructNumber(i-1, j+1) if getNumber(i-1, j) == None else ""
  addToCandidates(candidates, urn)

  l = constructNumberLeft(i, j-1)
  addToCandidates(candidates, l)

  r = constructNumberRight(i, j+1)
  addToCandidates(candidates, r)

  dln = constructNumber(i+1, j-1)
  addToCandidates(candidates, dln)
  dd = constructNumber(i+1, j) if getNumber(i+1, j-1) == None else ""
  addToCandidates(candidates, dd)
  drn = constructNumber(i+1, j+1) if getNumber(i+1, j) == None else ""
  addToCandidates(candidates, drn)

  if i == 138:
    print(candidates)

  if len(candidates) != 2:
    continue

  gearRatio = reduce(lambda a,b: a*b, candidates)

  gearRatioSum += gearRatio

print(f"Gear ratio sum is {gearRatioSum}")
