from os import error
from fastapi import FastAPI
from datetime import datetime, timedelta
import requests
from calendar import monthrange
import json

'''
    API_KEY = '77Pj5RyutTSatUVfn210VEkvOa3DOk7GDyiCDL1m'
    GET {BASE_URL}planetary/apod
'''
API_KEY = '77Pj5RyutTSatUVfn210VEkvOa3DOk7GDyiCDL1m'
BASE_URL = 'https://api.nasa.gov/'

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

error_output = {
  "status": 404,
  "message": "image/video not found"
}

app = FastAPI()

@app.get('/nasa/image-of-month')
async def get_apod():
    now=datetime.now()
    date = datetime(now.year, now.month, 1).date()
    URL = f'{BASE_URL}planetary/apod/?date={date}&&api_key={API_KEY}'
    response = requests.get(URL,verify=False)
    result = response.json()
    try:
        result = {key: result[key] for key in ['date', 'media_type', 'title', 'url']},200
    except:
        result = error_output
    return json.dumps(result)

@app.get('/nasa/images-of-month/{year}/{month}')
async def get_apod(year :int, month: str):
    try:
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = month_names.index(month.lower())+1
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, number_of_days_in_month(year, month)).date()
    except ValueError:
        return json.dumps(error_output)
    
    URL = f'{BASE_URL}planetary/apod/?start_date={start_date}&&end_date={end_date}&&api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        result = response.json()
        result = [i['url'] for i in result if i['media_type'] == 'image']
        return json.dumps(result)
    else:
        return json.dumps(error_output),404


@app.get('/nasa/videos-of-month/{year}/{month}')
async def get_apod(year :int, month: str):
    try:
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = month_names.index(month.lower())+1
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, number_of_days_in_month(year, month)).date()
    except ValueError:
        return json.dumps(error_output)
    
    URL = f'{BASE_URL}planetary/apod/?start_date={start_date}&&end_date={end_date}&&api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        result = response.json()
        result = [i['url'] for i in result if i['media_type'] == 'video']
        return json.dumps(result)
    else:
        return json.output(error_output),404


@app.get('/nasa/earth-poly-image/{date}')
async def get_apod(date: str):
    # Work in progress. filter by lat lon error.
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return json.output(error_output),404
    
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
        return json.dumps(results_list)
    else:
        return json.output(error_output),404

