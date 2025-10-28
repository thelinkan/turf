import requests
import json

#url="https://statistik.konj.se:443/PxWeb/api/v1/sv/KonjBar/indikatorer/Indikatorm.px"
#query= "{'query': [{'code': 'Indikator', 'selection': {'filter': 'item', 'values': ['KIFI', 'BTOT']}}, {'code': 'Period', 'selection': {'filter': 'item', 'values': ['2022M11']}}], 'response': {'format': 'json'}}"

url="https://api.turfgame.com/v5/zones/all"

response = requests.get(url)
print(response.status_code)
#print(response.text)

f = open("data/allzonesv5202510.json", "a", encoding='utf-8')
f.write(response.text)
f.close()