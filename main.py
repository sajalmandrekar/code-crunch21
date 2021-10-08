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
##########################  CRYPTO  ###############################################

BASE_URL = 'https://api.coinpaprika.com/v1/'

crypto_error = {
        "status": 404,
        "message": "coin/token not found"
    }

@app.get('/crypto/coins', responses={404: {"model": ExceptionModel}})
async def get_all_coins():
    '''
        Get All Coins sends a list of all coins (type = "coin").
        It does so by sending a request to 'https://api.coinpaprika.com/v1/coins' and filtering it to have only objects having type="coin".
        if any exception occurs, raise a HTTP404 Error
    '''
    URL = BASE_URL + 'coins'
    coins_list = requests.get(URL,verify=False)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        response = [{key: coin[key] for key in ['id', 'name', 'symbol', 'type']} for coin in coins_list if coin['type'] == 'coin']
        return response
    else:
        raiseException(crypto_error)


@app.get('/crypto/tokens', responses={404: {"model": ExceptionModel}})
async def get_all_tokens():
    '''
        Get All Tokens sends a list of all coins (type = "token").
        It does so by sending a request to 'https://api.coinpaprika.com/v1/coins' and filtering it to have only objects having type="token".
        if any exception occurs, raise a HTTP404 Error
    '''
    URL = BASE_URL + 'coins'
    coins_list = requests.get(URL,verify=False)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        response = [{key: coin[key] for key in ['id', 'name', 'symbol', 'type']} for coin in coins_list if coin['type'] == 'token']
        return response
    else:
        raiseException(crypto_error)


@app.get('/crypto/quote/{name}', responses={404: {"model": ExceptionModel}})
async def get_coin_ticker(name: str):
    '''
        This route gets all details of a coin by its name.
        Like price, id, symbol, rank, etc.
    '''
    URL = BASE_URL + 'tickers'
    coins_list = requests.get(URL,verify=False)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        try:
            response = list(filter(lambda coin: coin['name'] == name, coins_list))[0]
            response = {key: response[key] for key in ['id', 'name', 'symbol', 'rank', 'circulating_supply', 'total_supply', 'max_supply', 'quotes']}
            response['price'] = response['quotes']['USD']['price']
            del response['quotes']
        except IndexError:
            raiseException(crypto_error)
        return response
    else:
        raiseException(crypto_error)

def get_founder_obj(founder):
    '''
        This function takes a founder object, and formats it properly, for placing it in the founders list, for a particular coin.
    '''
    person_id = founder['id']
    URL = BASE_URL + f'people/{person_id}'
    person_details = requests.get(URL,verify=False)
    if person_details.status_code == 200:
        person_details = person_details.json()
        result = {'name': founder['name']}
        for link_key in ['github', 'linkedin', 'medium', 'twitter', 'additional']:
            try:
                result['links' if link_key == 'additional' else link_key] = person_details['links'][link_key][0]['url']
            except KeyError:
                pass
        return result
    else:
        raiseException(crypto_error)

def get_employee_obj(employee):
    '''
        This function takes a employee object, and formats it properly, for placing it in the team list list, for a particular coin.
    '''
    URL = BASE_URL + f"people/{employee['id']}"
    person_details = requests.get(URL,verify=False)
    if person_details.status_code == 200:
        person_details = person_details.json()
        result = {'name': employee['name'], 'position': employee['position']}
        for link_key in ['github', 'linkedin', 'medium', 'twitter', 'additional']:
            try:
                result['links' if link_key == 'additional' else link_key] = person_details['links'][link_key][0]['url']
            except KeyError:
                result['links' if link_key == 'additional' else link_key] = ""
        return result
    else:
        raiseException(crypto_error)


@app.get('/crypto/team/{name}', responses={404: {"model": ExceptionModel}})
async def get_team_details_by_name(name: str):
    '''
        This route returns the team behind a particular coin/token. This includes founder, authors, developers etc.
    '''
    URL1 = BASE_URL + 'coins'
    coins_list = requests.get(URL1,verify=False)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        try:
            response = list(filter(lambda coin: coin['name'] == name, coins_list))[0]
            coin_id = response['id']
            URL2 = BASE_URL + f'coins/{coin_id}'
            coin_details = requests.get(URL2,verify=False).json()
            response = {key: coin_details[key] for key in ['name', 'symbol', 'rank', 'type', 'team']}
            try:
                founders = [get_founder_obj(person) for person in response['team'] if 'founder' in person['position'].lower()]
                employees = [get_employee_obj(person) for person in response['team'] if 'founder' not in person['position'].lower()]
                response['founders'] = founders
                response['developers'] = employees
            except TypeError:
                response['founders'] = None
                response['developers'] = None
            del response['team']
        except IndexError:
            raiseException(crypto_error)
    else:
        raiseException(crypto_error)
    return response


######################################################################################
########################### section 5   ############################

BASE_URL_git = 'https://api.github.com/'

giterror = { "status": 404,
        "message": "resource not found"}

@app.get('/github/user/{username}', responses={404: {"model": ExceptionModel}})
async def get_profile_by_username(username: str):
    URL = BASE_URL_git + f'users/{username}'
    response = requests.get(URL,verify=False)
    if response.status_code == 200:
        response = response.json()
        response = {key: response[key] for key in ['name', 'avatar_url', 'public_repos', 'followers_url', 'following_url', 'url', 'bio']}

        followers = requests.get(URL + '/followers',verify=False).json()
        following = requests.get(URL + '/following',verify=False).json()

        response['followers'] = [user['login'] for user in followers]
        response['following'] = [user['login'] for user in following]

        del response['followers_url']
        del response['following_url']

        return response
    else:
        raiseException(giterror)

################### task 2,3    ####################
from github import github as gh

@app.get('/github/issues/{author}/{repo}/{label}', responses={404: {"model": ExceptionModel}})
async def get_github_issues(author: str,repo,label):
    output,code = gh.get_issues(repo=repo,creator=author,label=label)
    if code == 200:
        return output
    else:
        raiseException(giterror)

@app.get('/github/commits/{start},{end}/{repo}', responses={404: {"model": ExceptionModel}})
async def get_github_commits(start,end,repo):
    output,code = gh.get_commits(repo=repo,start_date=start,end_date=end)
    if code == 200:
        return output
    else:
        raiseException(giterror)