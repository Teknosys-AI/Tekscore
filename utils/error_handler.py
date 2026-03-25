"""
Centralized error handling utility for user-friendly error messages.
"""
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error message handler for user-friendly error messages."""
    
    # HTTP Status Code to User-Friendly Message Mapping
    HTTP_ERROR_MESSAGES = {
        400: "Invalid request. Please check the mobile number format and try again.",
        401: "Authentication failed. Please contact support if this issue persists.",
        403: "Access denied. You don't have permission to perform this action.",
        404: "Credit score service not available. Please try again later.",
        429: "Too many requests. Please wait a moment and try again.",
        500: "Service temporarily unavailable. Please try again later.",
        502: "Service is temporarily down. Please try again in a few moments.",
        503: "Service is currently down for maintenance. Please try again later.",
        504: "Request timeout. The service is taking longer than expected. Please try again.",
    }
    
    # API Error Message Patterns
    API_ERROR_PATTERNS = {
        'invalid': "Invalid mobile number format. Please enter a valid mobile number.",
        'not_found': "Mobile number not found in our system. Please verify the number and try again.",
        'unauthorized': "Authentication failed. Please contact support.",
        'forbidden': "Access denied. Please check your account permissions.",
        'rate_limit': "Too many requests. Please wait a moment before trying again.",
        'server_error': "Service temporarily unavailable. Please try again later.",
        'timeout': "Request timeout. Please try again.",
        'network': "Network error. Please check your internet connection and try again.",
    }
    
    @staticmethod
    def get_http_error_message(status_code, default_message=None):
        """
        Get user-friendly error message for HTTP status code.
        
        Args:
            status_code: HTTP status code
            default_message: Default message if status code not found
            
        Returns:
            User-friendly error message
        """
        message = ErrorHandler.HTTP_ERROR_MESSAGES.get(
            status_code, 
            default_message or "An error occurred. Please try again later."
        )
        logger.info(f"HTTP Error {status_code}: {message}")
        return message
    
    @staticmethod
    def get_api_error_message(error_response, status_code=None):
        """
        Extract user-friendly message from API error response.
        
        Args:
            error_response: API error response (dict or string)
            status_code: HTTP status code if available
            
        Returns:
            User-friendly error message
        """
        # If status code is provided, use HTTP error mapping
        if status_code and status_code in ErrorHandler.HTTP_ERROR_MESSAGES:
            return ErrorHandler.get_http_error_message(status_code)
        
        # Try to extract message from error response
        if isinstance(error_response, dict):
            # Check common error message fields
            message = (
                error_response.get('message') or
                error_response.get('error') or
                error_response.get('error_message') or
                error_response.get('detail')
            )
            
            if message:
                # Check if message matches known patterns
                message_lower = message.lower()
                for pattern, friendly_msg in ErrorHandler.API_ERROR_PATTERNS.items():
                    if pattern in message_lower:
                        return friendly_msg
                
                # Return the message if it's user-friendly, otherwise use generic
                if len(message) < 200 and not any(tech_word in message_lower for tech_word in ['exception', 'traceback', 'stack', 'sql']):
                    return message
        
        # If error_response is a string
        if isinstance(error_response, str):
            error_lower = error_response.lower()
            for pattern, friendly_msg in ErrorHandler.API_ERROR_PATTERNS.items():
                if pattern in error_lower:
                    return friendly_msg
        
        # Default message based on status code
        if status_code:
            return ErrorHandler.get_http_error_message(status_code)
        
        return "An error occurred while processing your request. Please try again later."
    
    @staticmethod
    def validate_mobile_number(mobile_number):
        """
        Validate mobile number format and return error message if invalid.
        
        Args:
            mobile_number: Mobile number string to validate
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not mobile_number:
            return False, "Please enter a mobile number."
        
        # Remove whitespace
        mobile_number = mobile_number.strip()
        
        if not mobile_number:
            return False, "Please enter a mobile number."
        
        # Check for non-numeric characters (allow +, -, spaces for formatting)
        cleaned = re.sub(r'[\s\+\-]', '', mobile_number)
        if not cleaned.isdigit():
            return False, "Mobile number must contain only digits. Please remove any special characters."
        
        # Check if starts with 0 or 92
        if not (cleaned.startswith('0') or cleaned.startswith('92')):
            return False, "Mobile number must start with 0 (for local format) or 92 (for international format)."
        
        # Check length
        if cleaned.startswith('0'):
            if len(cleaned) != 11:
                return False, "Mobile number starting with 0 must be 11 digits long. Example: 03001234567"
        elif cleaned.startswith('92'):
            if len(cleaned) != 12:
                return False, "Mobile number starting with 92 must be 12 digits long. Example: 923001234567"
        
        return True, None
    
    @staticmethod
    def validate_username(username):
        """
        Validate username format.
        
        Args:
            username: Username string to validate
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not username:
            return False, "Please enter your username."
        
        username = username.strip()
        
        if not username:
            return False, "Username cannot be empty."
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long."
        
        if len(username) > 50:
            return False, "Username must be less than 50 characters."
        
        # Allow alphanumeric, underscore, hyphen, dot, @
        if not re.match(r'^[a-zA-Z0-9@._-]+$', username):
            return False, "Username can only contain letters, numbers, and these characters: @ . _ -"
        
        return True, None
    
    @staticmethod
    def validate_password(password):
        """
        Validate password format.
        
        Args:
            password: Password string to validate
            
        Returns:
            Tuple (is_valid, error_message)
        """
        if not password:
            return False, "Please enter your password."
        
        password = password.strip()
        
        if not password:
            return False, "Password cannot be empty."
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        return True, None
    
    @staticmethod
    def format_database_error(error):
        """
        Format database error to user-friendly message.
        
        Args:
            error: Database error exception
            
        Returns:
            User-friendly error message
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Log technical details
        logger.error(f"Database error: {error_type} - {error_message}")
        
        # Return user-friendly message
        if 'connection' in error_message.lower() or 'connect' in error_message.lower():
            return "Unable to connect to the database. Please try again in a few moments. If the problem persists, contact support."
        
        if 'timeout' in error_message.lower():
            return "Request timed out. Please try again."
        
        if 'duplicate' in error_message.lower() or 'unique' in error_message.lower():
            return "This record already exists. Please use a different value."
        
        if 'foreign key' in error_message.lower() or 'constraint' in error_message.lower():
            return "Invalid data. Please check your input and try again."
        
        # Generic database error
        return "A database error occurred. Please try again. If the problem persists, contact support."
    
    @staticmethod
    def format_network_error(error):
        """
        Format network error to user-friendly message.
        
        Args:
            error: Network error exception
            
        Returns:
            User-friendly error message
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        logger.error(f"Network error: {error_type} - {error_message}")
        
        if 'timeout' in error_message.lower() or 'timed out' in error_message.lower():
            return "Request timed out. Please check your internet connection and try again."
        
        if 'connection' in error_message.lower() or 'refused' in error_message.lower():
            return "Unable to connect to the service. Please check your internet connection and try again."
        
        if 'dns' in error_message.lower() or 'resolve' in error_message.lower():
            return "Unable to reach the service. Please check your internet connection and try again."
        
        return "Network error. Please check your internet connection and try again."
    
    @staticmethod
    def get_quota_error_message(quota, max_quota, used_quota, quota_percentage=None):
        """
        Get user-friendly quota error message.
        
        Args:
            quota: Quota object (can be None)
            max_quota: Maximum quota allowed
            used_quota: Currently used quota
            quota_percentage: Percentage of quota used (optional, calculated if not provided)
            
        Returns:
            User-friendly quota error message
        """
        if quota is None:
            current_month = datetime.now().strftime("%B %Y")
            return f"You do not have a quota allocated for {current_month}. Please contact support to set up your monthly quota."
        
        if max_quota is None or max_quota == 0:
            return "Your quota limit is not configured. Please contact support."
        
        if used_quota >= max_quota:
            # Calculate next reset date (first day of next month)
            from datetime import datetime
            now = datetime.now()
            if now.month == 12:
                next_month = datetime(now.year + 1, 1, 1)
            else:
                next_month = datetime(now.year, now.month + 1, 1)
            
            reset_date = next_month.strftime("%B %d, %Y")
            return f"You've used all your monthly requests ({used_quota}/{max_quota}). Your quota will reset on {reset_date}. Consider upgrading your plan for more requests."
        
        # Calculate percentage if not provided
        if quota_percentage is None:
            quota_percentage = round((used_quota / max_quota * 100), 1) if max_quota > 0 else 0
        
        # Warning for approaching limit (80%+)
        if quota_percentage >= 80:
            remaining = max_quota - used_quota
            return f"You've used {quota_percentage}% of your monthly quota ({used_quota}/{max_quota}). Only {remaining} request{'s' if remaining != 1 else ''} remaining this month."
        
        return None  # No error, quota is fine
    
    @staticmethod
    def get_token_error_message(error_type='missing'):
        """
        Get user-friendly token error message.
        
        Args:
            error_type: Type of token error ('missing', 'expired', 'invalid', 'unauthorized')
            
        Returns:
            User-friendly token error message
        """
        token_messages = {
            'missing': "Your authentication token is missing. Please log out and log in again.",
            'expired': "Your session has expired. Please log in again to continue.",
            'invalid': "Your authentication token is invalid. Please log out and log in again.",
            'unauthorized': "You are not authorized to perform this action. Please contact support if you believe this is an error.",
        }
        
        return token_messages.get(error_type.lower(), "Authentication error. Please log in again.")
    
    @staticmethod
    def get_validation_error_message(field, error_type='invalid'):
        """
        Get user-friendly validation error message.
        
        Args:
            field: Field name that failed validation
            error_type: Type of validation error ('empty', 'invalid', 'too_short', 'too_long', 'format')
            
        Returns:
            User-friendly validation error message
        """
        field_names = {
            'mobile_number': 'mobile number',
            'username': 'username',
            'password': 'password',
            'email': 'email',
        }
        
        field_display = field_names.get(field.lower(), field)
        
        validation_messages = {
            'empty': f"Please enter your {field_display}.",
            'invalid': f"Please enter a valid {field_display}.",
            'too_short': f"Your {field_display} is too short. Please check the requirements.",
            'too_long': f"Your {field_display} is too long. Please check the requirements.",
            'format': f"Your {field_display} format is incorrect. Please check and try again.",
        }
        
        return validation_messages.get(error_type.lower(), f"Invalid {field_display}. Please check and try again.")