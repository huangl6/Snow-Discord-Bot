import json
from config import api_key
from datetime import datetime
import pandas

with open('sample_forecast.json') as json_file:
    data = json.load(json_file)

def processJson(data):
    times = data['list']
    snowfall = {}

    for i in times:
        dt_txt = i['dt_txt']
        date = str(datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S').date())
        snow = 0
        # print(i['weather'])
        # print(i)
        # weather formatted as 1 item list containing dictionary with keys: id, main, description, icon
        # print(i['weather'][0]['main'])
        if date not in snowfall:
            snowfall[date] = 0
        if i['weather'][0]['main'] == 'Snow':
            snow = i['snow']['3h']
            # print(date, snow)
            snowfall[date] += snow
        else:
            snowfall[date] += snow

    # print(snowfall)
    return snowfall
