import os
import re
script_dir = os.path.dirname(__file__)
rel_path = "puzzle.json"
abs_file_path = os.path.join(script_dir, rel_path)

puzzle = open(abs_file_path, 'r')
lines = puzzle.readlines()

regex = r"[^\d]*(\d)(.*(\d)(?![^\d]*\d))*"

result = 0

for line in lines:
  match = re.search(regex, line)
  firstNum = match.group(1)
  secondNum = match.group(3)

  number = firstNum
  if (secondNum != None):
    number += secondNum
  else:
    number += firstNum

  result += int(number)

print(result)
