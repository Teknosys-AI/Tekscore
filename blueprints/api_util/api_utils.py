import re
import logging
import requests
from flask import request
from config import Config
import urllib3
from utils.error_handler import ErrorHandler
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

    # Check if token exists
    if not user.Token:
        logger.error(f"User {user.UserId} ({user.Username}) has no token in database!")
        return {'error': 'Authentication token is missing. Please contact support.', 'status_code': 401}, 401
    
    # Log token status (masked for security)
    token_preview = user.Token[:30] + "..." if len(user.Token) > 30 else user.Token
    logger.info(f"Token present: Yes, Length: {len(user.Token)}, Preview: {token_preview}")

    headers = {
        'Authorization': f'Bearer {user.Token}'  # Use f-string to include token dynamically
    }
    
    logger.info(f"Making API request to: {url}")
    logger.debug(f"Authorization header: Bearer {token_preview}")

    try:
        # Log the actual request details for debugging
        logger.info(f"API Request Details - URL: {url}")
        logger.info(f"API Request Details - Headers: Authorization: Bearer {token_preview}")
        
        response = requests.get(url, headers=headers, verify=False, timeout=(30, 90))  # (connect timeout: 30s, read timeout: 90s)
        
        # Log response status before raising
        logger.info(f"API Response Status: {response.status_code}")
        if response.status_code != 200:
            try:
                response_text = response.text[:200]  # First 200 chars
                logger.error(f"API Error Response: {response_text}")
            except:
                pass
        
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response (example: returning JSON response from the API)
        api_data = response.json()
        return api_data, 200

    except requests.exceptions.HTTPError as err:
        status_code = response.status_code if hasattr(response, 'status_code') else 500
        logger.error(f"HTTP Error {status_code} for API call: {str(err)}")
        # Try to get error message from response
        try:
            error_data = response.json() if hasattr(response, 'json') else {}
        except:
            error_data = {}
        user_message = ErrorHandler.get_api_error_message(error_data, status_code)
        return {'error': user_message, 'status_code': status_code}, status_code

    except requests.exceptions.Timeout as err:
        logger.error(f"Timeout error for API call: {str(err)}")
        user_message = ErrorHandler.format_network_error(err)
        return {'error': user_message, 'status_code': 504}, 504

    except requests.exceptions.ConnectionError as err:
        logger.error(f"Connection error for API call: {str(err)}")
        user_message = ErrorHandler.format_network_error(err)
        return {'error': user_message, 'status_code': 503}, 503

    except requests.exceptions.RequestException as err:
        logger.error(f"Request exception for API call: {str(err)}")
        user_message = ErrorHandler.format_network_error(err)
        return {'error': user_message, 'status_code': 500}, 500

    except Exception as err:
        logger.error(f"Unexpected error for API call: {str(err)}", exc_info=True)
        user_message = ErrorHandler.get_http_error_message(500)
        return {'error': user_message, 'status_code': 500}, 500



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
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for HTTP errors


        # Process the response (example: returning JSON response from the API)
        history_api_data = response.json()
        return history_api_data, 200

    except requests.exceptions.HTTPError as err:
        status_code = response.status_code if hasattr(response, 'status_code') else 500
        logger.error(f"HTTP Error {status_code} for History API call: {str(err)}")
        # Try to get error message from response
        try:
            error_data = response.json() if hasattr(response, 'json') else {}
        except:
            error_data = {}
        user_message = ErrorHandler.get_api_error_message(error_data, status_code)
        return {'error': user_message, 'status_code': status_code}, status_code

    except requests.exceptions.Timeout as err:
        logger.error(f"Timeout error for History API call: {str(err)}")
        user_message = ErrorHandler.format_network_error(err)
        return {'error': user_message, 'status_code': 504}, 504

    except requests.exceptions.ConnectionError as err:
        logger.error(f"Connection error for History API call: {str(err)}")
        user_message = ErrorHandler.format_network_error(err)
        return {'error': user_message, 'status_code': 503}, 503

    except requests.exceptions.RequestException as err:
        logger.error(f"Request exception for History API call: {str(err)}")
        user_message = ErrorHandler.format_network_error(err)
        return {'error': user_message, 'status_code': 500}, 500

    except Exception as err:
        logger.error(f"Unexpected error for History API call: {str(err)}", exc_info=True)
        user_message = ErrorHandler.get_http_error_message(500)
        return {'error': user_message, 'status_code': 500}, 500






def is_valid_input(input_string):
    return bool(WHITELIST_PATTERN.match(input_string))