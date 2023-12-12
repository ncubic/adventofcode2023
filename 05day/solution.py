import sys
sys.path.append("../aoc")
import tools

lines = tools.getLines("05day/puzzle")

seeds = []
seedNums = lines[0].removeprefix("seeds: ").split(" ")
for seedNum in seedNums:
  if seedNum != "":
    seeds.append(int(seedNum))

def addRange(nums, array):
  startRangeB = int(nums[0])
  startRangeA = int(nums[1])
  length = int(nums[2])
  array.append((startRangeA, startRangeB, length))
  array.sort(key=lambda val: val[0]+val[2])

def addToMap(map, index, lines):
  key = lines[index].removesuffix(" map:\n")
  map[key] = []

  i = index + 1
  while i < len(lines):
    if lines[i] == "\n":
      break

    nums = lines[i].split(" ")
    addRange(nums, map[key])
    i += 1

map = {}
i = 0
for line in lines:
  if "map:" in line:
    addToMap(map, i, lines)

  i += 1

def getJumpFromMap(key, start, map):
  coords = map[key]
  chosen = None
  for coord in coords:
    if start >= coord[0] and start <= coord[0] + coord[2]:
      chosen = coord
      break
  if chosen == None:
    return start
  
  diff = start - chosen[0]
  return chosen[1] + diff

def findIntersection(range, other):
  if other[0] > range[1] or range[0] > other[1]:
    return None
  
  return (max(other[0], range[0]), min(other[1], range[1]))

def getJumpRanges(key, ranges, map):
  nextRanges = []
  candidates = map[key]
  uncoveredRanges = []

  for range in ranges:
    foundAny = False
    i = -1
    for candidate in candidates:
      i += 1
      expanded = (candidate[0], candidate[0] + candidate[2])
      intersection = findIntersection(range, expanded)

      if intersection == None:
        continue

      foundAny = True

      diff = candidate[1] - candidate[0]

      nextRanges.append((intersection[0]+diff, intersection[1]+diff))

      if range[1] > intersection[1]:
        uncovered = [intersection[1]+1, range[1]]
        if i + 1 < len(candidates):
          next = candidates[i+1][0]
          if uncovered[1] >= next:
            uncovered[1] = next - 1
        if uncovered[1] >= uncovered[0]:
          uncoveredRanges.append(uncovered)


    if not foundAny:
      uncoveredRanges.append(range)

  for uncoveredRange in uncoveredRanges:
    nextRanges.append((uncoveredRange[0], uncoveredRange[1]))

  return nextRanges

jumps = [
  "seed-to-soil", 
  "soil-to-fertilizer", 
  "fertilizer-to-water", 
  "water-to-light",
  "light-to-temperature",
  "temperature-to-humidity",
  "humidity-to-location"
]

locations = []
for seed in seeds:
  prev = seed
  for jump in jumps:
    prev = getJumpFromMap(jump, prev, map)
  locations.append(prev)

minLocation = min(locations)

print(f"Closest location is {minLocation}")

def chunk(list, n):
  for i in range(0, len(list), n):
    yield list[i:i+n]

seedRanges = list(chunk(seeds, 2))
for seedRange in seedRanges:
  seedRange[1] = seedRange[0] + seedRange[1] - 1

ranges = seedRanges
for jump in jumps:
  ranges = getJumpRanges(jump, ranges, map)

minLocation = -1
for range in ranges:
  if minLocation == -1 or range[0] < minLocation:
    minLocation = range[0]

print(f"Closest location 2 is {minLocation}")
