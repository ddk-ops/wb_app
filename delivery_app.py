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
RETRY_PERIOD = 10


url = 'https://www.wildberries.ru/webapi/lk/myorders/delivery/active'


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
    '''Sending message plug.'''
    print(message)


def check_api_response(response):
    '''Api response checking.'''
    if not isinstance(response, dict):
        raise TypeError('API type not json')
    if bool(response.get('resultState')) is not False:
        raise KeyError('resultState not found')
    if not response.get('value'):
        raise KeyError('value not found')


def get_delivery(last_result, delivery_list):
    '''Delivery list.'''
    delivery_cart = []
    for brand in delivery_list:
        if brand['trackingStatus'] == 'Готов к получению':
            ready_to_recieve = brand['brand'] + ' ' + brand['name']
            delivery_cart.append(ready_to_recieve)

    if delivery_cart != last_result:
        message = f'{delivery_cart} are ready to receive'
        last_result = delivery_cart
    else:
        message = 'nothing happens'
    return message, delivery_cart


def main():
    '''Main logic.'''
    message = ''
    last_result = []
    check_token()
    while True:
        try:
            response_json = get_api_response()
            check_api_response(response_json)
            delivery_list = response_json['value']['positions']
            if len(delivery_list) != 0:
                message, last_result = get_delivery(last_result, delivery_list)
                send_message(message)
            else:
                message = 'your delivery is empty'
                send_message(message)
        except Exception as error:
            message = f'the program is not working {error}'
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
