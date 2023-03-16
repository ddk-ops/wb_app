import os
from http import HTTPStatus
from json.decoder import JSONDecodeError
import time

import requests
from dotenv import load_dotenv

from exceptions import (EnviromentVariableError, ParseJsonError,
                        StatusCodeError, WbAPIError)

load_dotenv()

COOKIES_TOKEN = os.getenv('COOKIES_TOKEN')
COOKIES = {'WILDAUTHNEW_V3': COOKIES_TOKEN}

url = 'https://ru-basket-api.wildberries.ru/lk/basket/items'

RETRY_PERIOD = 5


def check_token():
    ''' WILDAUTHNEW_V3 token check.'''
    if not COOKIES_TOKEN:
        raise EnviromentVariableError(
            'Сheck environment variable WILDAUTHNEW_V3')


def get_api_response():
    '''Api response processing.'''
    try:
        response_status = requests.post(url, cookies=COOKIES)
        if response_status.status_code != HTTPStatus.OK:
            raise StatusCodeError(f'status code {response_status.status_code}')
        return response_status.json()
    except JSONDecodeError:
        raise ParseJsonError('Token expired')
    except requests.RequestException:
        raise WbAPIError('Api access error')


def send_message(message):
    '''snding message plug.'''
    print(message)


def check_api_response(response):
    '''Api response checking.'''
    if not isinstance(response, dict):
        raise TypeError('API type not json')
    if bool(response.get('resultState')) is not False:
        raise KeyError('resultState not found')
    if not response.get('value'):
        raise KeyError('value not found')


def get_backet_list(backet, backet_list):
    '''Compare and generate a new backet.'''
    new_backet_list = []
    for purchase in backet:
        temp = {}
        for key, value in purchase.items():
            if key == 'quantity':
                temp[key] = value
            if key == 'cod1S':
                temp[key] = value
        new_backet_list.append(temp)
    if new_backet_list == backet_list:
        message = 'no changes in backet'
    else:
        message = f'updated backet {new_backet_list}'
    return message, new_backet_list


def main():
    '''Main logic.'''
    message = ''
    backet_list = []
    check_token()
    while True:
        try:
            response_json = get_api_response()
            check_api_response(response_json)
            backet = response_json.get('value')
            if len(backet) != 0:
                message, backet_list = get_backet_list(backet, backet_list)
                send_message(message)
            else:
                message = 'your backet is empty'
                send_message(message)
        except Exception as error:
            message = f'the program is not working {error}'
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
