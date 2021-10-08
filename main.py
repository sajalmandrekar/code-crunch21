from fastapi import FastAPI, Response, status, HTTPException
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import requests
from calendar import monthrange
from pydantic import BaseModel
import os

from starlette.exceptions import HTTPException as StarletteHTTPException

API_KEY = os.environ.get('NASA_KEY')
BASE_URL = 'https://api.nasa.gov/'

def number_of_days_in_month(year, month):
    '''
        This function returns the number of days of a given month in an year.
        eg. (2021, 10) returns 31 because Oct 2021 has 31 days.
    '''
    return monthrange(year, month)[1]

nasa_error = {
        "status": 404,
        "message": "image/video not found"
    }


class ExceptionModel(BaseModel):
    status: int
    message: str

def raiseException(error_message=nasa_error):
    raise HTTPException(status_code=404, detail=error_message)


app = FastAPI()     # the base app


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(exc.detail, status_code=exc.status_code)


@app.get('/nasa/image-of-month', responses={404: {"model": ExceptionModel}})
async def get_apod(response: Response):
    now=datetime.now()
    date = datetime(now.year, now.month, 1).date()
    URL = f'{BASE_URL}planetary/apod/?date={date}&&api_key={API_KEY}'
    response = requests.get(URL,verify=False)
    result = response.json()
    try:
        result = {key: result[key] for key in ['date', 'media_type', 'title', 'url']}
    except:
        raiseException()
    return result

@app.get('/nasa/images-of-month/{year}/{month}', responses={404: {"model": ExceptionModel}})
async def get_apod(year :int, month: str, response: Response):
    try:
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = month_names.index(month.lower())+1
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, number_of_days_in_month(year, month)).date()
    except ValueError:
        raiseException()
    
    URL = f'{BASE_URL}planetary/apod/?start_date={start_date}&&end_date={end_date}&&api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        result = response.json()
        result = [i['url'] for i in result if i['media_type'] == 'image']
        return result
    else:
        raiseException()


@app.get('/nasa/videos-of-month/{year}/{month}', responses={404: {"model": ExceptionModel}})
async def get_apod(year :int, month: str, response: Response):
    try:
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = month_names.index(month.lower())+1
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, number_of_days_in_month(year, month)).date()
    except ValueError:
        raiseException()
    
    URL = f'{BASE_URL}planetary/apod/?start_date={start_date}&&end_date={end_date}&&api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        result = response.json()
        result = [i['url'] for i in result if i['media_type'] == 'video']
        return result
    else:
        raiseException()


@app.get('/nasa/earth-poly-image/{date}', responses={404: {"model": ExceptionModel}})
async def get_apod(date: str, response: Response):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raiseException()
    
    URL = f'{BASE_URL}EPIC/api/natural/date/{date}?api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        results = response.json()
        results_list = []
        for result in results:
            result_dict = {key: result[key] for key in ['identifier', 'caption', 'image', 'date']}
            result_dict.update({ key: result['centroid_coordinates'][key] for key in ['lat', 'lon'] })
            results_list.append(result_dict)
        results_list = [i for i in results_list if (i['lat'] >= 10 and i['lat'] <= 40 and i['lon'] >= 120 and i['lon'] <= 160)]
        return results_list
    else:
        raiseException()

####################################    SECTION 2  ##############################################
####################################    WEATHER API     ######################################

from weather import weather

#####################   TASK 2  ############################################

@app.get('/weather/search',responses={404: {"model": ExceptionModel}})
def weather_by_location(lat:float=-1,lon:float=-1,pincode:int=-1):
    output = {}
    if lat == -1 or lon == -1:
        ## search by pincode
        output,code = weather.weather_by_pincode(pincode)
    else:
        ## search by coordinates
        output,code = weather.weather_by_cord(lat=lat,lon=lon)

    if code == 200:
        return output
    else:
        raiseException(output)


################### TASK 1  ##############################################

@app.get('/weather/{city}',responses={404: {"model": ExceptionModel}})
def weather_by_city(city:str):
    output,code = weather.weather_by_city(city)

    if code == 200:
        return output
    else:
        raiseException(output)

#####################################################################################
########################    SECTION 3       #########################################
########################    TWITTER API     #########################################

from twitter import twitter  

#############################   TASK 1  ###########################################
@app.get('/twitter/user/{username}',responses={404: {"model": ExceptionModel}})
def get_user_tweet(username:str):

    output,code = twitter.get_tweets_by_username(username)
    if code == 200:
        return output
    else:
        raiseException(output)

#############################   TASK 2  ###########################################
@app.get('/twitter/hashtag/{hashtag}',responses={404: {"model": ExceptionModel}})
def get_hashtag(hashtag:str):

    output,code = twitter.tweets_hashtag(hashtag)
    if code == 200:
        return output
    else:
        raiseException(output)

#############################   TASK 3  ###########################################
@app.get('/twitter/location',responses={404: {"model": ExceptionModel}})
def get_tweet_location(latitude:float,longitude:float,radius:str):

    output,code = twitter.geoloc(lat=latitude,lon=longitude,radius=radius)
    if code == 200:
        return output
    else:
        raiseException(output)

#####################################################################################
###########################     SECTION 4       #####################################

