import re
import logging
import requests
from flask import request
from config import Config
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logger = logging.getLogger(__name__)

def call_Jscore_api_function(user, mobile_number):
    """
    Function to call Jscore API and return the response.
    """

    # Extract user's IP address
    user_ip = request.remote_addr

    # Log user information
    logger.info(f"API call by UserId: {user.UserId}, Username: {user.Username}, IP: {user_ip}, for MobileNumber: {mobile_number}")


    api =  Config.API_ENDPOINT
    url = f"{api}?msisdn={mobile_number}"


    headers = {
        'Authorization': f'Bearer {user.Token}'  # Use f-string to include token dynamically
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response (example: returning JSON response from the API)
        api_data = response.json()
        return api_data, 200

    except requests.exceptions.HTTPError as err:
        # print( str(err))
        return {'error': str(err)}, response.status_code

    except Exception as err:
        # print( str(err))
        return {'error': 'An error occurred: ' + str(err)}, 500



def call_JscoreHistory_api_function(user, mobile_number):
    """
    Function to call Jscore History API and return the response.
    """

    # Extract user's IP address
    user_ip = request.remote_addr

    # Log user information
    logger.info(f"History API call by UserId: {user.UserId}, Username: {user.Username}, IP: {user_ip}, for MobileNumber: {mobile_number}")


    api =  Config.HISTORYAPI_ENDPOINT
    url = f"{api}?msisdn={mobile_number}"


    headers = {
        'Authorization': f'Bearer {user.Token}'  # Use f-string to include token dynamically
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors


        # Process the response (example: returning JSON response from the API)
        history_api_data = response.json()
        return history_api_data, 200

    except requests.exceptions.HTTPError as err:
        # print( str(err))
        return {'error': str(err)}, response.status_code

    except Exception as err:
        # print( str(err))
        return {'error': 'An error occurred: ' + str(err)}, 500






def is_valid_input(input_string):
    return bool(WHITELIST_PATTERN.match(input_string))