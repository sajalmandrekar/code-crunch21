from fastapi import FastAPI
from datetime import datetime, timedelta
import requests
from calendar import monthrange

'''
    API_KEY = '77Pj5RyutTSatUVfn210VEkvOa3DOk7GDyiCDL1m'
    GET {BASE_URL}planetary/apod
'''
API_KEY = '77Pj5RyutTSatUVfn210VEkvOa3DOk7GDyiCDL1m'
BASE_URL = 'https://api.nasa.gov/'

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]


app = FastAPI()

@app.get('/nasa/image-of-month')
async def get_apod():
    now=datetime.now()
    date = datetime(now.year, now.month, 1).date()
    URL = f'{BASE_URL}planetary/apod/?date={date}&&api_key={API_KEY}'
    response = requests.get(URL,verify=False)
    result = response.json()
    try:
        result = {key: result[key] for key in ['date', 'media_type', 'title', 'url']}
    except:
        result = response.json()
    return result

@app.get('/nasa/images-of-month/{year}/{month}')
async def get_apod(year :int, month: str):
    try:
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = month_names.index(month.lower())+1
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, number_of_days_in_month(year, month)).date()
    except ValueError:
        return {
            'code': 400,
            'title': 'Bad Request',
            'message': 'Invalid Month or year! Did you mispell the month or entered a wrong year?',
            'full_help': 'Currently, the following names are valid inputs for month: ' + ', '.join(month_names) + '. Year has to be a positive integer.'
        }
    
    URL = f'{BASE_URL}planetary/apod/?start_date={start_date}&&end_date={end_date}&&api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        result = response.json()
        result = [i['url'] for i in result if i['media_type'] == 'image']
        return result
    else:
        return response.json()


@app.get('/nasa/videos-of-month/{year}/{month}')
async def get_apod(year :int, month: str):
    try:
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = month_names.index(month.lower())+1
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, number_of_days_in_month(year, month)).date()
    except ValueError:
        return {
            'code': 400,
            'title': 'Bad Request',
            'message': 'Invalid Month or year! Did you mispell the month or entered a wrong year?',
            'full_help': 'Currently, the following names are valid inputs for month: ' + ', '.join(month_names) + '. Year has to be a positive integer.'
        }
    
    URL = f'{BASE_URL}planetary/apod/?start_date={start_date}&&end_date={end_date}&&api_key={API_KEY}'

    response = requests.get(URL,verify=False)
    if(response.status_code == 200):
        result = response.json()
        result = [i['url'] for i in result if i['media_type'] == 'video']
        return result
    else:
        return response.json()


@app.get('/nasa/earth-poly-image/{date}')
async def get_apod(date: str):
    # Work in progress. filter by lat lon error.
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return {
            'code': 400,
            'title': 'Bad Request',
            'message': 'Invalid Date! Did you enter date in the correct format (YYYY-MM-DD)?'
        }
    
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
        return response.json()

