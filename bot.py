import discord
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
XRapidAPIKeyGlobalQuotes = os.getenv('XRapidAPIKeyGlobalQuotes')
XRapidAPIKEYStockPrices=os.getenv('XRapidAPIKEYStockPrices')
XRapidAPIKEYWeatherUpdates=os.getenv('XRapidAPIKEYWeatherUpdates')



def update_in_database(data):
    file = open("Data.txt", "a")
    file.write(data + ' \n')
    file.close()


def get_Global_quotes():
    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function": "GLOBAL_QUOTE", "symbol": "MSFT", "datatype": "json"}

    headers = {
        "X-RapidAPI-Key": XRapidAPIKeyGlobalQuotes,
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)
    # quote = json_data["01. Symbol"]
    # print(response)
    # print(type(response))
    print(response.text)
    print(type(json_data))
    # ->dict
    print(type(json_data['Global Quote']))
    print(json_data)
    print(json_data['Global Quote'])
    # -> list

    print(json_data['Global Quote']['01. symbol'])
    for data in json_data["Global Quote"]:
        print(data + " : " + json_data["Global Quote"][data])
    return json_data["Global Quote"]

    # print(json_data["Global Quote"]["01. symbol"])
    # print(quote)
    # return quote


def get_stock_prices():
    url = "https://latest-stock-price.p.rapidapi.com/any"

    headers = {
        "X-RapidAPI-Key": XRapidAPIKEYStockPrices,
        "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    json_data = json.loads(response.text)
    # print(response.text)
    # print(type(response.text))
    # print(type(json_data))
    # for data in json_data[0]:
    #     string = data + " : " + str(json_data[0][data])
    # print(data)
    # print(json_data[0][data])
    # print(string)
    return json_data


def get_weather_updates():
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"

    querystring = {"aggregateHours": "24", "location": "Kanpur,India", "contentType": "json", "unitGroup": "us",
                   "shortColumnNames": "0"}

    headers = {
        "X-RapidAPI-Key": XRapidAPIKEYWeatherUpdates,
        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_data = json.loads(response.text)

    # print(response.text)
    # print(type(response.text))
    # print(json_data)
    # print(type(json_data))
    # print(json_data['locations'])
    return json_data['locations']

    # print(json_data['locations'][data]['values'][subdata])
    # print(type(json_data[0]))
    # return json_data


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$help'):
            string = "$weather-updates - to get updates about weather in Kanpur,India \n $get-stock-prices - to get upadtes about NIFTY stomks \n $add - to add data to the database of the Bot which can be accessed later \n$retrieve_data - to get data from database which has been added through '$add' \n $help-to show all Bot commands"
            await message.channel.send(string)

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        # if message.content.startswith('$inspire'):
        #     quote = get_quote()
        #     await message.channel.send(quote)

        if message.content.startswith('$add'):
            message_to_be_added = message.content.split("$add ", 1)[1]
            update_in_database(message_to_be_added)
            await message.channel.send('Data has been added to the database')

        if message.content.startswith('$retrieve_data'):
            file = open("Data.txt", "r")
            for line in file:
                print(line)
                await message.channel.send(line)
            file.close()

        if message.content.startswith('$getapidata'):
            datas = get_Global_quotes()
            for data in datas:
                string = data + " : " + datas[data]
                await message.channel.send(string)
            # await message.channel.send(data)

        if message.content.startswith('$get-stock-prices'):
            json_data = get_stock_prices()
            for i in range(1):
                for data in json_data[i]:
                    string = data + " : " + str(json_data[i][data])
                    await message.channel.send(string)
                await message.channel.send("---------------------")
            # for data in json_data:
            #     string = data +" : "+json_data[data]
            #     await message.channel.send(string)

        if message.content.startswith('$weather-updates'):
            json_data = get_weather_updates()
            for data in json_data:
                # print(data)
                # print(type(data))
                # print(json_data['locations'][data])
                # print(type(json_data['locations'][data]))
                print(json_data[data]['values'])
                # print(type(json_data['locations'][data]['values']))
                for subdata in json_data[data]['values']:
                    print(subdata)
                    print(type(subdata))
                    # print(subdata[0])
                    # print(type(subdata[0]))
                    for subsubdata in subdata:
                        if subsubdata == 'cloudcover':
                            string = "Cloud Cover" + " : " + str(subdata[subsubdata]) + "%"
                            # print(string)
                            await message.channel.send(string)
                        if subsubdata == 'temp':
                            temperature = 5 * (subdata[subsubdata] - 32) / 9
                            temperature = "{:.2f}".format(temperature)
                            string = "Temp." + " : " + str(temperature) + '\u2070' + "C"
                            await message.channel.send(string)
                        if subsubdata == 'maxt':
                            temperature = 5 * (subdata[subsubdata] - 32) / 9
                            temperature = "{:.2f}".format(temperature)
                            string = "MaxTemp." + " : " + str(temperature) + '\u2070' + "C"
                            await message.channel.send(string)
                        if subsubdata == 'humidity':
                            string = "Humidity" + " : " + str(subdata[subsubdata]) + "%"
                            await message.channel.send(string)
                        if subsubdata == 'visibility':
                            string = "Visibility" + " : " + str(subdata[subsubdata]) + "%"
                            await message.channel.send(string)
                        if subsubdata == 'conditions':
                            string = "Conditions" + " : " + str(subdata[subsubdata])
                            await message.channel.send(string)

                    break
            # for data in json_data[0]:
            # await message.channel.send(data)

    client.run(TOKEN)
