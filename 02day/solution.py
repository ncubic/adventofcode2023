import os
import re
from functools import reduce

script_dir = os.path.dirname(__file__) 
rel_path = "puzzle"
abs_file_path = os.path.join(script_dir, rel_path)

puzzle = open(abs_file_path, 'r')
lines = puzzle.readlines()

limits = {
  "red": 12,
  "green": 13,
  "blue": 14
}

validIdSum = 0
powerOfMinCubes = 0

for line in lines:
  sections = line.split(":")
  gameId = int(sections[0].removeprefix("Game "))
  
  rounds = sections[1].split(";")
  isValid = True

  mins = {
    "red": 0,
    "green": 0,
    "blue": 0
  }

  for round in rounds:
    for key in limits.keys():
      match = re.search(rf"(\d+) {key}", round)
      count = int(match.group(1)) if match != None else 0

      if count > mins[key]:
        mins[key] = count

      if count > limits[key]:
        isValid = False

  powerOfMinCubes += reduce(lambda a, b : a * b, mins.values())
  
  if isValid:
    validIdSum += gameId

print(f"Sum of all valid game ids: {validIdSum}")
print(f"Power of all minimal cubes: {powerOfMinCubes}")
