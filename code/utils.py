from datetime import datetime

# NOTE: Remember to add function name here!
__all__ = ['datetime_to_unix', 'unix_to_datetime']

# Function to convert datetime string to Unix time (INTEGER)
def datetime_to_unix(datetime_str):
    """
    Converts a datetime string (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD) to Unix time (INTEGER).
    
    Args:
        datetime_str (str): The datetime string to convert.
        
    Returns:
        int: Unix timestamp.
    """
    # Parse the input string into a datetime object
    dt_format = "%Y-%m-%d %H:%M:%S" if " " in datetime_str else "%Y-%m-%d"
    dt_object = datetime.strptime(datetime_str, dt_format)
    # Convert to Unix time (INTEGER)
    return int(dt_object.timestamp())

# Function to convert Unix time (INTEGER) to datetime string
def unix_to_datetime(unix_time, include_time=False):
    """
    Converts Unix time (INTEGER) to a datetime string (YYYY-MM-DD HH:MM:SS or YYYY-MM-DD).
    
    Args:
        unix_time (int): The Unix timestamp to convert.
        include_time (bool): Whether to include time in the output string.
        
    Returns:
        str: Formatted datetime string.
    """
    # Convert Unix time to a datetime object
    dt_object = datetime.fromtimestamp(unix_time)
    # Format based on include_time flag
    dt_format = "%Y-%m-%d %H:%M:%S" if include_time else "%Y-%m-%d"
    return dt_object.strftime(dt_format)


