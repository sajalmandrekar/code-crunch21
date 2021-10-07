from fastapi import FastAPI
import requests

app = FastAPI()
BASE_URL = 'https://api.coinpaprika.com/v1'

@app.get('/crypto/coins')
async def get_all_coins():
    URL = BASE_URL + '/coins'
    coins_list = requests.get(URL)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        response = [{key: coin[key] for key in ['id', 'name', 'symbol', 'type']} for coin in coins_list if coin['type'] == 'coin']
    else:
        response = coins_list.json()
    return response


@app.get('/crypto/tokens')
async def get_all_tokens():
    URL = BASE_URL + '/coins'
    coins_list = requests.get(URL)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        response = [{key: coin[key] for key in ['id', 'name', 'symbol', 'type']} for coin in coins_list if coin['type'] == 'token']
    else:
        response = coins_list.json()
    return response


@app.get('/crypto/quote/{name}')
async def get_coin_ticker(name: str):
    URL = BASE_URL + '/tickers'
    coins_list = requests.get(URL)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        try:
            response = list(filter(lambda coin: coin['name'] == name, coins_list))[0]
            response = {key: response[key] for key in ['id', 'name', 'symbol', 'rank', 'circulating_supply', 'total_supply', 'max_supply', 'quotes']}
            response['price'] = response['quotes']['USD']['price']
            del response['quotes']
        except IndexError:
            response = {
                'code': '404',
                'message': 'Requested Coin could not be found. Did you enter it wrong?',
                'full_help': 'Please check the name of the coin. It is case-sensitive. For a full list of coins, send request to crypto/coins.'
            }
        # response = [{key: coin[key] for key in ['id', 'name', 'symbol', 'type']} for coin in coins_list if coin['type'] == 'token']
    else:
        response = coins_list.json()
    return response

def get_founder_obj(founder):
    person_id = founder['id']
    URL = BASE_URL + f'/people/{person_id}'
    person_details = requests.get(URL)
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
        return person_details.json()

def get_employee_obj(employee):
    URL = BASE_URL + f"/people/{employee['id']}"
    person_details = requests.get(URL)
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
        return person_details.json()


@app.get('/crypto/team/{name}')
async def get_team_details_by_name(name: str):
    URL1 = BASE_URL + '/coins'
    coins_list = requests.get(URL1)
    if(coins_list.status_code == 200):
        coins_list = coins_list.json()
        try:
            response = list(filter(lambda coin: coin['name'] == name, coins_list))[0]
            coin_id = response['id']
            URL2 = BASE_URL + f'/coins/{coin_id}'
            coin_details = requests.get(URL2).json()
            response = {key: coin_details[key] for key in ['name', 'symbol', 'rank', 'type', 'team']}
            print(response)
            try:
                # founders = [get_founder_obj(person) for person in response['team'] if person['position'].lower() in ['founder', 'co-founder', 'author']]
                founders = [get_founder_obj(person) for person in response['team'] if 'founder' in person['position'].lower()]
                # employees = [get_employee_obj(person) for person in response['team'] if person['position'].lower() not in ['founder', 'co-founder', 'author']]
                employees = [get_employee_obj(person) for person in response['team'] if 'founder' not in person['position'].lower()]
                response['founders'] = founders
                response['developers'] = employees
            except TypeError:
                response['founders'] = None
                response['developers'] = None
            del response['team']
        except IndexError:
            response = {
                'code': '404',
                'message': 'Requested Coin could not be found. Did you enter it wrong?',
                'full_help': 'Please check the name of the coin. It is case-sensitive. For a full list of coins, send request to crypto/coins.'
            }
    else:
        response = coins_list.json()
    return response
