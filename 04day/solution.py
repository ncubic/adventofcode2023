import sys
sys.path.append("../aoc")
import tools
from functools import reduce
import re

lines = tools.getLines("04day/puzzle")

def hasNum(nums, num):
  for n in nums:
    if n == num:
      return 1
  return 0

def calculateWorth(count):
  if count == 0:
    return 0
  return pow(2, count-1)

rows = []
total = 0
deck = []

for line in lines:
  firstSplit = line.split(":")
  results = firstSplit[1].split("|")
  winingNums = re.split(r"\s+", results[0])
  elfNums = re.split(r"\s+", results[1])

  map = {}
  for num in winingNums:
    if num == "":
      continue 
    map[num] = hasNum(elfNums, num)

  count = reduce(lambda a,b: a+b, map.values())
  worth = calculateWorth(count)
  total += worth
  deck.append((map, count))

print(f"Worth of cards is {total}")

matrixDeck = []
for card in deck:
  rowCards = [card]
  matrixDeck.append(rowCards)

i = 0
while i < len(matrixDeck):
  j = 0
  row = matrixDeck[i]
  while j < len(row):
    tup = row[j]
    count = tup[1]

    z = i + 1
    while z < i + count + 1:
      if z < len(matrixDeck):
        toCopy = matrixDeck[z][0]
        matrixDeck[z].append(toCopy)

      z += 1

    j += 1

  i += 1

deckSize = 0
for cards in matrixDeck:
  deckSize += len(cards)

print(f"Final deck size is {deckSize}")
