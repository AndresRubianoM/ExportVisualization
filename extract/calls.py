import requests
from requests.exceptions import HTTPError


TIMELIMIT = 60

def call(url, message=''):
    try:
        response = requests.get(url, timeout=TIMELIMIT)
        #Verifies the request is succesful
        response.raise_for_status()
        print('Succesful Request (HTTP code {}),  {}'.format(response.status_code, message))
        return response

    except HTTPError as e:
        print('HTPP Error has ocurred: {}'.format(e))
        return ''
    except requests.exceptions.ChunkedEncodingError as e:
        print('Connection interruption: {}'.format(e))
