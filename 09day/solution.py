import sys
sys.path.append("../aoc")
import tools

def anyAboveZero(row):
  for n in row:
    if n != 0:
      return True
  return False

def createDiffs(array):
  row = [*array]
  diffs = [row]
  while anyAboveZero(row):
    temp = row
    row = []
    i = 1
    while i < len(temp):
      row.append(temp[i]-temp[i-1])
      i += 1
    diffs.append(row)
  return diffs

def calculateNext(array):
  diffs = createDiffs(array)

  j = len(diffs) - 1
  last = 0
  while j >= 0:
    row = diffs[j]
    if j != len(diffs):
      last += row[len(row)-1]
    row.append(last)
    j -= 1

  return last

def calculatePrevious(array):
  diffs = createDiffs(array)

  j = len(diffs) - 1
  first = 0
  while j >= 0:
    row = diffs[j]
    if j != len(diffs):
      first = row[0] - first
    row.insert(0, first)
    j -= 1

  return first
  
lines = tools.getLines("09day/puzzle")
matrix = []

for line in lines:
  nums = line.removeprefix("\n").split(" ")
  array = []
  for num in nums:
    array.append(int(num))
  matrix.append(array)

total = 0
for row in matrix:
  total += calculateNext(row)

print(f"first round solution is {total}")

total = 0
for row in matrix:
  total += calculatePrevious(row)

print(f"second round solution is {total}")
