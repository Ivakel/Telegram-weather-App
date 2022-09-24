import datetime as dt
import telebot
import requests
import os
from dotenv import load_dotenv

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

load_dotenv()
API_KEY = os.getenv("API_KEY")
TELE_KEY = os.getenv("TELE_KEY")

bot = telebot.TeleBot(TELE_KEY)

@bot.message_handler(commands=["weather"])
def weather(message):

    CITY = message.text
    response = weather("Bizana")
    
    data = main_weather(response)
    compiled_data = compile(data)
    bot.send_message(message.chat.id, compiled_data)



def compile(data: dict) ->str:
    str_data = ""

    for key, value in data.items():
        if not (type(str_data) == str):
            value = str(value)
        str_data += f"{key}: {value}\n"
    return str_data

def main_weather(response):
    if "message" in response:
        return {"Error": "Place not found!"}
    
    main_weather_info = response["main"]
    weather = response["weather"][0]
    description = weather["description"]
    name = response["name"]

    min_temp = round(main_weather_info["temp_min"] - 273.15)
    max_temp = round(main_weather_info["temp_max"] - 273.15)

    data = {"Name": name, "minimum_emperature": min_temp, "maximum_emperature": max_temp, "Condition": description}
    return data

def weather(place):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + place
    response = requests.get(url).json()
    return response

def request_weather(message):
    request = message.text.split(" ")
    if len(request) < 2:
        return False
    return request[0].lower() == "weather"



@bot.message_handler(func=request_weather)
def get_weather(message):
    place = " ".join(message.text.split()[1:])
    
    response = weather(place)
    
    data = main_weather(response)
    compiled_data = compile(data)
    bot.send_message(message.chat.id, compiled_data)
  

bot.polling()
    
    
