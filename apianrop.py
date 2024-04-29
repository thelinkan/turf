import requests
import json

#url="https://statistik.konj.se:443/PxWeb/api/v1/sv/KonjBar/indikatorer/Indikatorm.px"
#query= "{'query': [{'code': 'Indikator', 'selection': {'filter': 'item', 'values': ['KIFI', 'BTOT']}}, {'code': 'Period', 'selection': {'filter': 'item', 'values': ['2022M11']}}], 'response': {'format': 'json'}}"

url="https://api.turfgame.com/v4/users"
query=[{'name' : 'thelinkan'},{'name' : 'capthaddock'}]

print(url)
print(query)

#response = requests.get(url)
response = requests.post(url,json=query)
print(response.status_code)
#print(response.text)
if (response.status_code == 200):

    print(response.text)
    x=response.text
    y=json.loads(x)

    for z in y:
        print(f"Resultat för {z['name']}")
        print(f"Rank: {z['rank']}")
        print(f"Poäng totalt: {z['totalPoints']}, varav {z['points']} denna månad")
        print(f"Totalt har personen tagit {z['uniqueZonesTaken']} unika zoner")
        print()


elif (response.status_code == 404):
    print("Result not found!")