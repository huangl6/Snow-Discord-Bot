import discord
import json
import requests

color = 0xFF6500
key_features = {
    'temp' : 'Temperature',
    'feels_like' : 'Feels Like',
    'temp_min' : 'Minimum Temperature',
    'temp_max' : 'Maximum Temperature'
}

def parse_data(data):
    if data['humidity']:
        del data['humidity']
    if data['pressure']:
        del data['pressure']
    print(data)
    return data

def weather_message(data, location):
    location = location.title()
    message = discord.Embed(
        title=f'{location} Weather',
        description=f'Here is the weather in {location}.',
        color=color
    )
    for key in data:
        message.add_field(
            name=key_features[key],
            value=str(data[key]),
            inline=False
        )
    return message

def get_data(url):
    r = json.loads(requests.get(url).content)
    return r

def error_message(location):
    location = location.title()
    return discord.Embed(
        title='Error',
        description=f'There was an error retrieving weather data for {location}.',
        color=color
    )
