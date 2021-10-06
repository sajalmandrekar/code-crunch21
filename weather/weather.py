import requests
import os

error_output = {
    "status": 404,
    "message": "weather data not found"
}

base_url = "https://api.openweathermap.org/data/2.5/weather"

API_KEY_TEMP = "275e4767a0b6e782b72dbca9457ddfff"           # temporary
#API_KEY = os.environ["OPENWEATHER_KEY"]
'''
Use API Key by setting it as an Environment variable
in terminal: $ export OPENWEATHER_KEY=w233e....
in python: API_KEY = os.environ["OPENWEATHER_KEY"]
'''

################################################################################
def weather_by_city(city):
    
    endpoint = f"{base_url}?q={city}&appid={API_KEY_TEMP}&units=metric"   
    resp = requests.get(endpoint)

    if resp.status_code in (200,203):

        weather_data = resp.json()
        
        return {
        "country": weather_data['sys']['country'],
        "name": weather_data['name'],
        "temp": weather_data['main']['temp']
        }, resp.status_code
    else:
        return error_output,404

##########################################################################
def weather_by_cord(lat,lon):
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    endpoint = f"{base_url}?lat={lat}&lon={lon}&appid={API_KEY_TEMP}&units=metric"
    resp = requests.get(endpoint)

    if resp.status_code in (200,203):
    
        weather_data = resp.json()
        if('country' not in weather_data['sys']):
            country = ""
        else:
            country = weather_data['sys']['country']
    
        return {
            "country": country,
            "name": weather_data['name'],
            "temp": weather_data['main']['temp'],
            "min_temp": weather_data['main']['temp_max'],
            "max_temp": weather_data['main']['temp_min'],
            "latitude": weather_data['coord']['lat'],
            "longitude": weather_data['coord']['lon'],
        }, resp.status_code
    else:
        return error_output,404

#####################################################################
def weather_by_pincode(pincode):
    
    endpoint = f"{base_url}?zip={pincode},IN&appid={API_KEY_TEMP}&units=metric"
    resp = requests.get(endpoint)

    if resp.status_code in (200,203):

        weather_data = resp.json()
        if('country' not in weather_data['sys']):
            country = ""
        else:
            country = weather_data['sys']['country']
        
        return {
            "country": country,
            "name": weather_data['name'],
            "temp": weather_data['main']['temp'],
            "min_temp": weather_data['main']['temp_max'],
            "max_temp": weather_data['main']['temp_min'],
            "latitude": weather_data['coord']['lat'],
            "longitude": weather_data['coord']['lon'],
        },resp.status_code
    else:
        return error_output,404