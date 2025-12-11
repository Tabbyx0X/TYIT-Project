"""
Utility functions for the voting system
Contains helper functions for validation, sanitization, and other common operations
"""
import re
from datetime import datetime, timedelta


def sanitize_input(text):
    """
    Sanitize user input to prevent XSS attacks
    
    Args:
        text: Input string to sanitize
        
    Returns:
        Sanitized string
    """
    if not text:
        return text
    # Remove potentially dangerous characters and trim whitespace
    text = text.strip()
    # Additional sanitization can be added here
    return text


def validate_email(email):
    """
    Validate email format using regex
    
    Args:
        email: Email address to validate
        
    Returns:
        Boolean indicating if email is valid
    """
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_voter_id(voter_id):
    """
    Validate voter ID format (alphanumeric, 5-20 characters)
    
    Args:
        voter_id: Voter ID to validate
        
    Returns:
        Boolean indicating if voter ID is valid
    """
    if not voter_id:
        return False
    pattern = r'^[a-zA-Z0-9]{5,20}$'
    return re.match(pattern, voter_id) is not None


def validate_password(password):
    """
    Validate password strength
    - Minimum 8 characters
    - Must contain at least one letter
    - Must contain at least one number
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None


def validate_date_range(start_date, end_date):
    """
    Validate election date range
    
    Args:
        start_date: Election start datetime
        end_date: Election end datetime
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if start_date >= end_date:
        return False, "End date must be after start date"
    
    # Check if start date is not too far in the past
    if start_date < datetime.utcnow() - timedelta(days=1):
        return False, "Start date cannot be in the past"
    
    return True, None


def format_datetime(dt, format_string='%Y-%m-%d %H:%M'):
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
        format_string: Format string for strftime
        
    Returns:
        Formatted datetime string
    """
    if not dt:
        return ""
    return dt.strftime(format_string)


def calculate_percentage(part, whole):
    """
    Calculate percentage with proper handling of division by zero
    
    Args:
        part: Part value
        whole: Whole value
        
    Returns:
        Percentage as float
    """
    if whole == 0:
        return 0.0
    return (part / whole) * 100


def truncate_text(text, max_length=100, suffix='...'):
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_client_ip(request):
    """
    Get client IP address from request
    Handles proxy headers
    
    Args:
        request: Flask request object
        
    Returns:
        Client IP address as string
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or 'unknown'


def is_safe_url(target):
    """
    Check if redirect URL is safe
    Prevents open redirect vulnerabilities
    
    Args:
        target: Target URL to check
        
    Returns:
        Boolean indicating if URL is safe
    """
    if not target:
        return False
    # Only allow relative URLs or same-domain URLs
    return target.startswith('/') and not target.startswith('//')
