# importing the requests library 
import requests
import json
from datetime import date
from pprint import pprint

# COLLECT PREVIOUS WINNING NUMBERS

# defining the api-endpoint  
API = "https://www.nationallottery.co.za/index.php?task=results.getHistoricalData&amp;Itemid=273&amp;option=com_weaver&amp;controller=powerball-plus-history"

DATE_TODAY = date.today().strftime('%d/%m/%Y')

DRAW_CHANGED_FIFTY = 895
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

# print('Powerball Entries: ', len(draws_PB))
# print('Powerball Plus Entries: ', len(draws_PBP))

# pprint(draws_PB)

pbArr = []

# for draw in draws_PB:
#   if (int(draw['drawNumber']) >= DRAW_CHANGED_FIFTY):
#     tempArr = [int(draw['ball1']),int(draw['ball2']),int(draw['ball3']),int(draw['ball4']),int(draw['ball5'])]
#     tempArr.sort()
#     tempArr.insert(0, int(draw['drawNumber']))
#     tempArr.insert(0, draw['drawDate'])
#     tempArr.append(int(draw['powerball']))
#     pbArr.append(tempArr)

for draw in draws_PBP:
  if (int(draw['drawNumber']) >= DRAW_CHANGED_FIFTY):
    tempArr = [int(draw['ball1']),int(draw['ball2']),int(draw['ball3']),int(draw['ball4']),int(draw['ball5'])]
    tempArr.sort()
    tempArr.insert(0, int(draw['drawNumber']))
    tempArr.insert(0, draw['drawDate'])
    tempArr.append(int(draw['powerball']))
    pbArr.append(tempArr)

print('Date,Draw,1,2,3,4,5,PB')
for row in pbArr:
  print(str(row[0]) + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]))
