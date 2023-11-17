import discord
import requests
import json
from forecast import *
from config import token, api_key
from processJson import processJson
from discord.ext import tasks

# token = 'DISCORD_BOT_TOKEN'
# api_key = 'OPEN_WEATHER_MAP_API_KEY'

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
    loop_forecast.start()

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
                        data = get_data(url)
                        print(data)
                        print('retrieved data')
                        with open('sample_forecast.json', 'w') as outfile:
                            json.dump(data, outfile)
                        print('loaded data!')
                        await message.channel.send(embed=weather_message(data, mtn))
                    except:
                        await message.channel.send(embed=error_message(resort))
                    break
                else:
                    print(resort_input)

def forecast():
    lat, long = resorts['Mammoth Mountain'][1]
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api_key}'
    print('retrieving data')
    data = get_data(url)
    # print(data)
    print('retrieved data')
    snow = processJson(data)
    print(snow)
    print('processed data')
    for i in snow:
        print(snow[i])


@tasks.loop(seconds=20)
async def loop_forecast():
    lat, long = resorts['Mammoth Mountain'][1]
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api_key}'
    print('retrieving data')
    data = get_data(url)
    # print(data)
    print('retrieved data')
    snow = processJson(data)
    print(snow)
    print('processed data')
    totalSnow = 0
    counter = 0
    for i in snow:
        if counter == 3:
            break
        print(i)
        totalSnow += snow[i]
    if totalSnow >= 5:
        #bot sends snow alert
        try:
            await client.wait_until_ready()
            channel = client.get_channel(1172379336620384360)
            await channel.send(totalSnow)
        except discord.errors.Forbidden:
            return




client.run(token)
