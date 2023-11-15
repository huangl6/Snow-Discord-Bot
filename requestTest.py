import requests
import json

api_key = 'df47b7f47b781635a2176e4c40b62bde'

resorts = {'Mammoth Mountain': (['mammoth', 'mammy'], ['37.628989532560425', '-119.0309197485682']), 'Palisades': (['Squaw', 'Squaw Valley', 'Alpine Meadows', 'Olympic Valley']), 'Whistler Blackcomb': (['Whistler']),
'Alta-Snowbird': (['Alta', 'Snowbird']), 'Park City': (['Park City']), 'Steamboat Springs': (['Steamboat']), 'Big Bear Mountain': (['Big Bear', 'Bear', 'Snow Valley']),
'Niseko United': (['Niseko'])}

lat, long = ['37.628989532560425', '-119.0309197485682']
url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api_key}'
data = json.loads(requests.get(url).content)
dataJson = json.dumps(data)
with open('sample_forecast.json', 'w') as outfile:
    json.dump(data, outfile)
