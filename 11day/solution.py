import sys
sys.path.append("../aoc")
import tools

def addSteps(jumps, x1, y1):
  if len(jumps) == 0:
    jumps.append((x1, y1))
    return

  last = jumps[-1]
  if last == (x1, y1):
    return

  x0 = last[0]
  y0 = last[1]
  if x1 == x0 or y1 == y0:
    jumps.append((x1, y1))
  else:
    jumps.extend([(x0, y1), (x1, y1)])

# source https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
def getJumps(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy
    
    jumps = []
    while True:
        addSteps(jumps, x0, y0)
        if x0 == x1 and y0 == y1:
          break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
              break
            error = error + dy
            x0 = x0 + sx
        
        if e2 <= dx:
            if y0 == y1:
              break
            error = error + dx
            y0 = y0 + sy
        
    return jumps

def calculateDistance(first, second, rowsWithGalaxies, columnsWithGalaxies, expansionFactor):
  jumps = getJumps(first[0], first[1], second[0], second[1])
  distance = 0
  lastExpandedX = 0
  lastExpandedY = 0
  for i in range(1, len(jumps)):
    distance += 1
    x = jumps[i][0]
    y = jumps[i][1]
    if x != lastExpandedX and not x in rowsWithGalaxies:
      lastExpandedX = x
      distance += expansionFactor
    if y != lastExpandedY and not y in columnsWithGalaxies:
      lastExpandedY = y
      distance += expansionFactor
  return distance
    

matrix = tools.getStringMatrix("11day/puzzle")

rowsWithGalaxies = []
columnsWithGalaxies = []
for i in tools.arrayRange(matrix):
  row = matrix[i]
  for j in tools.arrayRange(row):
    elem = row[j]
    if elem == "#":
      if i not in rowsWithGalaxies:
        rowsWithGalaxies.append(i)
      if j not in columnsWithGalaxies:
        columnsWithGalaxies.append(j)

galaxies = []
for i in tools.arrayRange(matrix):
  for j in tools.arrayRange(matrix[i]):
    if matrix[i][j] == "#":
      galaxies.append((i, j))

sumLen = 0
for i in tools.arrayRange(galaxies):
  firstLocation = galaxies[i]
  for j in range(i+1, len(galaxies)):
    secondLocation = galaxies[j]
    length = calculateDistance(firstLocation, secondLocation, rowsWithGalaxies, columnsWithGalaxies, 1)
    sumLen += length

print(f"First solution is {sumLen}")

sumLen = 0
for i in tools.arrayRange(galaxies):
  firstLocation = galaxies[i]
  for j in range(i+1, len(galaxies)):
    secondLocation = galaxies[j]
    length = calculateDistance(firstLocation, secondLocation, rowsWithGalaxies, columnsWithGalaxies, 999999)
    sumLen += length

print(f"Second solution is {sumLen}")
