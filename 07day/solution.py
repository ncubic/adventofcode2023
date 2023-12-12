import sys
sys.path.append("../aoc")
import tools

cards = {
  "2": 2,
  "3": 3,
  "4": 4,
  "5": 5,
  "6": 6,
  "7": 7,
  "8": 8,
  "9": 9,
  "T": 10,
  "J": 11,
  "Q": 12,
  "K": 13,
  "A": 14
}

hands = {
  "five": 7,
  "four": 6,
  "full": 5,
  "three": 4,
  "two": 3,
  "one": 2,
  "high": 1
}

def countJokers(hand):
  count = 0
  for c in hand:
    if c == "J":
      count += 1
  return count

def jokerHand(hand):
  value = getHand(hand)

  jokerCount = countJokers(hand)
  if jokerCount == 0 or jokerCount == 5:
    return value
  
  if jokerCount == 1:
    if value == "four":
      return "five"
    if value == "three":
      return "four"
    if value == "two":
      return "full"
    if value == "one":
      return "three"
    if value == "high":
      return "one"
  elif jokerCount == 2:
    if value == "full":
      return "five"
    if value == "two":
      return "four"
    if value == "one":
      return "three"
  elif jokerCount == 3:
    if value == "full":
      return "five"
    if value == "three":
      return "four"
  elif jokerCount == 4:
    return "five"

def getHand(hand):
  values = {}
  for card in hand:
    if not card in values:
      values[card] = 1
    else:
      values[card] += 1

  if 5 in values.values():
    return "five"
  elif 4 in values.values():
    return "four"
  elif 3 in values.values() and 2 in values.values():
    return "full"
  elif 3 in values.values() and 1 in values.values():
    return "three"
  elif len(values.keys()) == 3 and 2 in values.values() and 1 in values.values():
    return "two"
  elif len(values.keys()) == 4 and 2 in values.values():
    return "one"
  else:
    return "high"
  
def compareDecks(a, b, useJokers):
  ah = getHand(a) if not useJokers else jokerHand(a)
  bh = getHand(b) if not useJokers else jokerHand(b)

  if hands[ah] < hands[bh]:
    return -1
  elif hands[ah] > hands[bh]:
    return 1
  
  i = 0
  while i < len(a):
    ca = a[i]
    cb = b[i]
    if cards[ca] < cards[cb]:
      return -1
    elif cards[ca] > cards[cb]:
      return 1
    i += 1

  return 0

def quicksort(l, useJokers=False):
  if len(l) <= 1:
    return l
  
  pivotNum = round(len(l) / 2) - 1

  lower = []
  higher = []

  pivot = l[pivotNum]
  i = 0
  while i < len(l):
    e = l[i]

    if i == pivotNum:
      i += 1
      continue
    elif compareDecks(e[0], pivot[0], useJokers) <= 0:
      lower.append(e)
    else:
      higher.append(e)
    
    i += 1

  next = quicksort(lower, useJokers)
  next.append(pivot)
  next.extend(quicksort(higher, useJokers))
  return next

  
lines = tools.getLines("07day/puzzle")

decks = []
for line in lines:
  parts = line.split(" ")
  deck = [*parts[0]]
  bid = int(parts[1].removesuffix("\n"))

  decks.append((deck, bid))

sortedDecks = quicksort(decks)

result = 0
j = len(sortedDecks) - 1
while j >= 0:
  result += (j+1)*sortedDecks[j][1]
  j -= 1

print(f"first round result is {result}")

cards["J"] = 0

sortedDecks = quicksort(decks, True)

result = 0
j = len(sortedDecks) - 1
while j >= 0:
  result += (j+1)*sortedDecks[j][1]
  j -= 1

print(f"second round result is {result}")
