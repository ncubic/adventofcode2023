import sys
sys.path.append("../aoc")
import tools
import re
import math

def calculate(pressedTime, limit):
  return pressedTime * limit - pow(pressedTime, 2)

def calculateTotal(times, distances):
  total = 1
  i = 0

  while i < len(times):
    limit = int(times[i])
    toBeatTime = int(distances[i])
    solutionCount = 0

    j = 1
    while j <= limit:
      solution = calculate(j, limit)
      if solution > toBeatTime:
        solutionCount += 1
      j += 1

    total *= solutionCount
    i += 1
  return total


lines = tools.getLines("06day/puzzle")

times = re.split(r"\s+", lines[0].removeprefix("Time:").strip())
distances = re.split(r"\s+", lines[1].removeprefix("Distance:").strip())

total = calculateTotal(times, distances)
print(f"Initial total is {total}")

correctedTime = "".join(times)
correctedDistance = "".join(distances)

secondTotal = calculateTotal([correctedTime], [correctedDistance])
print(f"Part two total is {secondTotal}")
