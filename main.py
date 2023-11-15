import discord
import requests
import json
from forecast import *

# token = 'DISCORD_BOT_TOKEN'
token = 'MTE3MjM3OTU3MDI3MjQ3NzI1NQ.GyZMBk.axDrZacsYKNBZyDArHkzb9XIqS1cHIKMAHUCYw'
# api_key = 'OPEN_WEATHER_MAP_API_KEY'
api_key = 'df47b7f47b781635a2176e4c40b62bde'

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)


command_prefix = 'w.'
forecast_prefix = 'forecast.'
resorts = {'Mammoth Mountain': (['mammoth', 'mammy'], ['37.628989532560425', '-119.0309197485682']), 'Palisades': (['Squaw', 'Squaw Valley', 'Alpine Meadows', 'Olympic Valley']), 'Whistler Blackcomb': (['Whistler']),
'Alta-Snowbird': (['Alta', 'Snowbird']), 'Park City': (['Park City']), 'Steamboat Springs': (['Steamboat']), 'Big Bear Mountain': (['Big Bear', 'Bear', 'Snow Valley']),
'Niseko United': (['Niseko'])}

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='w.[location]'))

@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(command_prefix):
        if len(message.content.replace(command_prefix, '')) >= 1:
            location = message.content.replace(command_prefix, '').lower()
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
            print(url)
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))
    elif message.author != client.user and message.content.startswith(forecast_prefix):
        if len(message.content.replace(forecast_prefix, '')) >= 1:
            resort_input = message.content.replace(forecast_prefix, '').lower()
            for mtn, details in resorts.items():
                if resort_input.lower() in details[0] or resort_input.lower() == mtn:
                    print(details)
                    print(details[1])
                    lat, long = details[1]
                    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api_key}'
                    resort = mtn
                    print(url)
                    try:
                        print('retrieving data')
                        data = get_forecast(url)
                        print(data)
                        print('retrieved data')
                        with open('sample_forecast.json', 'w') as outfile:
                            json.dump(data, outfile)
                        print('loaded data!')
                        await message.channel.send(embed=weather_message(data, location))
                    except:
                        await message.channel.send(embed=error_message(resort))
                    break
                else:
                    print(resort_input)


client.run(token)
