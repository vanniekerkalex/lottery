# importing the requests library 
import requests
import json
from datetime import date
from pprint import pprint

# COLLECT PREVIOUS WINNING NUMBERS

# defining the api-endpoint  
API = "https://www.nationallottery.co.za/index.php?task=results.getHistoricalData&amp;Itemid=273&amp;option=com_weaver&amp;controller=powerball-plus-history"

DATE_TODAY = date.today().strftime('%d/%m/%Y')

# data to be sent to api 

DATA_PB = {'gameName': 'POWERBALL',
        'startDate': '05/10/2003',
        'endDate': DATE_TODAY,
        'offset': 0,
        'limit': 999999999,
        'isAjax': True,
      } 

DATA_PBP = {'gameName': 'POWERBALLPLUS',
        'startDate': '05/10/2003',
        'endDate': DATE_TODAY,
        'offset': 0,
        'limit': 999999999,
        'isAjax': True,
      } 

# sending post request and saving response as response object 
r_PB = requests.post(url = API, data = DATA_PB) 
r_PBP = requests.post(url = API, data = DATA_PBP) 

# extracting response text  
parsed_PB = json.loads(r_PB.text)
parsed_PBP = json.loads(r_PBP.text)

draws_PB = parsed_PB['data']
draws_PBP = parsed_PBP['data']

print('Powerball Entries: ', len(draws_PB))
print('Powerball Plus Entries: ', len(draws_PBP))

pbArr = []

for draw in draws_PB:
  tempArr = [int(draw['ball1']),int(draw['ball2']),int(draw['ball3']),int(draw['ball4']),int(draw['ball5']),int(draw['powerball'])]
  pbArr.append(tempArr)

for draw in draws_PBP:
  tempArr = [int(draw['ball1']),int(draw['ball2']),int(draw['ball3']),int(draw['ball4']),int(draw['ball5']),int(draw['powerball'])]
  pbArr.append(tempArr)

print('Total Entries: ', len(pbArr))

# CALCULATE THE LOTTERY NUMBERS

# Standard values
widthBand = 0.5
midBand = (50+1)/2
minEvenNumbersDiff = 0
# How many numbers are in right distribution: i.e. 1-10, 11-20, 21-30, etc.
distributedAreas = 4
aveTimesNumberDrawnBand = 5

# Create weighted dicts for the lotto numbers (1-50) and the powerballs (1-20)
weightedLotto = {k:0 for k in range(1,51)}
weightedPower = {k:0 for k in range(1,21)}

# Combine the powerball and powerball plus drawn numbers
# comboArr = pbArr + pbpArr

lottoArr = []
powerArr = []

# Separating all the lotto numbers drawn and the powerballs drawn into 1-D arrays.
for row in pbArr:
	row1 = row[:-1]
	lottoArr.append(row1)
	powerArr.append(row[-1])

# Sum the number of times lotto numbers have appeared
for row in lottoArr:
	for val in row:
		weightedLotto[val] = weightedLotto[val] + 1

# Account for the number 46 - 50 that were introduced later.
sumVal = 0
for val in range(1, 46):
  sumVal += weightedLotto[val]
ave = sumVal / 45

sumVal2 = 0
for val in range(46, 51):
  sumVal2 += weightedLotto[val]
ave2 = sumVal2 / 5

aveDiff = int(ave - ave2)

# Adjust values from 45-50 to change of powerball rules
weightedLotto[46] += aveDiff
weightedLotto[47] += aveDiff
weightedLotto[48] += aveDiff
weightedLotto[49] += aveDiff
weightedLotto[50] += aveDiff

# Sum the number of times powerballs have appeared
for val in powerArr:
	weightedPower[val] = weightedPower[val] + 1

# Calculate the average times any number has been drawn
aveTimesNumberDrawn = 0
for num, val in weightedLotto.items():
	aveTimesNumberDrawn += val
aveTimesNumberDrawn /= len(weightedLotto)

leastDrawnLotto = sorted(weightedLotto, key=weightedLotto.get)
leastDrawnPower = sorted(weightedPower, key=weightedPower.get)

# Rules
# no. odd = no. even
# average = total average ie. between 24-26
# split into quadrants ie. 5 x 10 for lotto numbers
# can look at least drawn values... but rather sum the amount of times the chosen numbers have been drawn, the average must equal the average of total numbers drawn.

# Check whether the row of lottery numbers have the minimum ratio of odd / even numbers.
def isEvenOdd(lottoRow, minEvenNumbersDiff):
	even = 0
	for val in lottoRow:
		if val % 2 == 0:
			even += 1
		else:
			even -= 1
	if even <= minEvenNumbersDiff and even >= -minEvenNumbersDiff:
		return True
	return False

# Check whether the row of lottery numbers fit in the average band
def isRowAveInBand(lottoRow, midBand, widthBand):
	ave = sum(lottoRow[:-1])/len(lottoRow[:-1])
	if ave <= (midBand + widthBand) and ave >= (midBand - widthBand):
		return True
	return False

# Check whether the row of lottery numbers values are distributed "nicely"
def isDistributedNicely(lottoRow, distributedAreas):
	distDict = {k:0 for k in (10,20,30,40,50)}

	for val in lottoRow[:-1]:
		if val <= 10:
			distDict[10] = 1
		elif val <= 20:
			distDict[20] = 1
		elif val <= 30:
			distDict[30] = 1
		elif val <= 40:
			distDict[40] = 1
		else:
			distDict[50] = 1
			
	total = sum(distDict.values())
	if total >= distributedAreas:
		return True
	return False

# Check whether the row of lottery numbers fit within an average band
def isAveDrawnAmount(lottoRow, aveTimesNumberDrawn, aveTimesNumberDrawnBand):
	total = 0
	for val in lottoRow[:-1]:
		total += weightedLotto[val]
	# total += weightedLotto[lottoRow[-1]]

	ave = total / (len(lottoRow) - 1)
	# print(ave, aveTimesNumberDrawn)
	if ave <= aveTimesNumberDrawn + aveTimesNumberDrawnBand and ave >= aveTimesNumberDrawn - aveTimesNumberDrawnBand:
		return True
	return False

# TODO: Check least drawn why [1:] and not [0:]

suggestedLotto = leastDrawnLotto[0:20]
suggestedPower = leastDrawnPower[0:5]
print("Lotto:", suggestedLotto)
print("Power:", suggestedPower)
print("***************")
finalArr = []
count = 0
for one in range(min(suggestedLotto),11):
	for two in range(11,21):
		for three in range(21,31):
			for four in range(31,41):
				for five in range(41,max(suggestedLotto)):
					for six in range(min(suggestedPower),max(suggestedPower)):
						count += 1
						arr = [one,two,three,four,five,six]
						if (all(x in suggestedLotto for x in [one,two,three,four,five])) and (six in suggestedPower):
							if isEvenOdd(arr, minEvenNumbersDiff) and isRowAveInBand(arr, midBand, widthBand) and isAveDrawnAmount(arr, aveTimesNumberDrawn, 6):
								print(count, arr)
								finalArr.append(arr)

print(' ')
pprint(finalArr)

print("***************")
print(len(finalArr), "* R7.50 = R ", len(finalArr) * 7.5)

# New features: Have power ball and power ball plus separate
# The final combinations are tested against both criteria
# Build for lotto as well.