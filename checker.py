from pprint import pprint

# PASTE THE CHOSEN NUMBERS HERE

numbers = [
  [1, 16, 27, 40, 44, 1],
  [1, 16, 27, 40, 44, 7],
  [1, 16, 27, 40, 44, 15],
  [6, 16, 27, 33, 44, 1],
  [6, 16, 27, 33, 44, 7],
  [6, 16, 27, 33, 44, 15],
  [8, 16, 27, 33, 44, 1],
  [8, 16, 27, 33, 44, 7],
  [8, 16, 27, 33, 44, 15]
]

# PASTE THE WINNING NUMBERS HERE
winners = [
  [1, 16, 27, 40, 44, 1], # PB
  [3, 22, 27, 35, 44, 7]  # PBP
]

scorePB = 0
powerPB = 0
scorePBP = 0
powerPBP = 0

result = []
for row in numbers:
  for num in row:
    if num in winners[0][:-1]:
      scorePB += 1
    if num in winners[1][:-1]:
      scorePBP += 1
  if row[-1] == winners[0][-1]:
    powerPB = 1
  if row[-1] == winners[1][-1]:
    powerPBP = 1
  if (powerPBP + powerPB > 0 or scorePB > 2 or scorePBP > 2):
    result.append({
      'Matched PB Nums': scorePB,
      'Matched PB': powerPB,
      'Matched PBP Nums': scorePBP,
      'Matched PBP': powerPBP
    })
  scorePB = 0
  powerPB = 0
  scorePBP = 0
  powerPBP = 0

for row in result:
  print(' ')
  print(row)