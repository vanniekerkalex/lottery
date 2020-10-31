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

# sending post request and saving response as response object 
r_PB = requests.post(url = API, data = DATA_PB) 

# extracting response text  
parsed_PB = json.loads(r_PB.text)
draws_PB = parsed_PB['data']

pbArr = []

for draw in draws_PB:
  if (int(draw['drawNumber']) >= DRAW_CHANGED_FIFTY):
    tempArr = [int(draw['ball1']),int(draw['ball2']),int(draw['ball3']),int(draw['ball4']),int(draw['ball5'])]
    tempArr.sort()
    tempArr.insert(0, int(draw['drawNumber']))
    tempArr.insert(0, draw['drawDate'])
    tempArr.append(int(draw['powerball']))
    pbArr.append(tempArr)

