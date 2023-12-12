import sys
sys.path.append("../aoc")
import tools
import re
import sympy

def getFactors(num, primes):
  chosen = []
  current = num
  found = True
  while found:
    found = False
    for prime in primes:
      if current % prime == 0:
        found = True
        current = int(current / prime)
        chosen.append(prime)
      elif prime > current:
        break

  return chosen


lines = tools.getLines("08day/puzzle")

instructions = [*lines[0].removesuffix("\n")]

paths = {}
i = 2
while i < len(lines):
  parts = lines[i].split("=")
  key = parts[0].strip()

  match = re.search(r"(\w\w\w),\s(\w\w\w)", parts[1])
  left = match.group(1)
  right = match.group(2)
  
  paths[key] = (left, right)

  i += 1

current = "AAA"
step = -1
if current in paths:
  while current != "ZZZ":
    step += 1

    pointer = step % (len(instructions))

    instruction = instructions[pointer]
    options = paths[current]

    if instruction == "L":
      current = options[0]
    else:
      current = options[1]

  print(f"part 1 solution is {step + 1}")

starts = []
ends = []
for key in paths.keys():
  if key[2] == "A":
    starts.append(key)
  if key[2] == "Z":
    ends.append(key)

times = []

for start in starts:
  step = -1
  current = start
  while True:

    step += 1
    pointer = step % (len(instructions))
    instruction = instructions[pointer]
    options = paths[current]

    if instruction == "L":
      current = options[0]
    else:
      current = options[1]

    if current in ends:
      times.append(step+1)
      break

maxTime = max(times)
primes = list(sympy.primerange(0,round(maxTime/2)))  

factorOccurence = {}

for time in times:
  factors = getFactors(time, primes)
  factorOccurenceLocal = {}
  for factor in factors:
    if not factor in factorOccurenceLocal:
      factorOccurenceLocal[factor] = 1
    else:
      factorOccurenceLocal[factor] += 1

  for key in factorOccurenceLocal.keys():
    if not key in factorOccurence:
      factorOccurence[key] = factorOccurenceLocal[key]
    elif factorOccurenceLocal[key] > factorOccurence[key]:
      factorOccurence[key] = factorOccurenceLocal[key]

commonMultiple = 1
for prime in factorOccurence.keys():
  commonMultiple *= prime * factorOccurence[prime]

print(f"part 2 solution is {commonMultiple}")
