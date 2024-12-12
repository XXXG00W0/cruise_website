from datetime import datetime
import re

# NOTE: Remember to add function name here!
__all__ = ['datetime_to_unix', 'unix_to_datetime','sanitize_input','validate_itinerary_times']

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

def sanitize_input(input_str=None, max_len=100):
    """
    Sanitize user input by removing special symbols using regex and limiting its length.

    Args:
        input_str (str): The input string to sanitize. Defaults to None.
        max_len (int): The maximum allowed length for the input string. Defaults to 100.

    Returns:
        str: The sanitized input string.
    """
    if input_str is None:
        return None
    elif type(input_str)!=str:
        return input_str

    # Use regex to remove special symbols
    sanitized_str = re.sub(r'[<>&"\'`;|{}$]', '', input_str)

    # Truncate the string to the maximum allowed length
    sanitized_str = sanitized_str[:max_len]

    return sanitized_str

def validate_itinerary_times(new_itin_start,new_itin_end, trip_start_time, trip_end_time, existing_itineraries):
    """
    Validates the start and end times of a new itinerary against a trip's start and end times,
    and against the existing itineraries for that trip.

    Args:
        new_itinerary: A dictionary containing the new itinerary's start and end times.
        trip_start_time: The start time of the trip.
        trip_end_time: The end time of the trip.
        existing_itineraries: A list of existing itineraries, each represented as a dictionary
                               with 'start_time' and 'end_time' keys.

    Returns:
        True if the new itinerary's times are valid, False otherwise.
    """
    new_itin_start=datetime_to_unix(new_itin_start) if type(new_itin_start)==str else new_itin_start
    new_itin_end=datetime_to_unix(new_itin_end) if type(new_itin_end)==str else new_itin_end

    # Check if the new itinerary's start time is after the trip's start time
    if new_itin_start < trip_start_time:
        print("new_itin_start < trip_start_time")
        return False

    # Check if the new itinerary's end time is before the trip's end time
    if new_itin_end > trip_end_time:
        print("new_itin_end > new_itin_start")
        return False

    # Check if the new itinerary's end time is after its start time
    if new_itin_end <= new_itin_start:
        print("new_itin_end <= new_itin_start")
        return False

    # Check for conflicts with existing itineraries
    for (existing_start_time,existing_end_time) in existing_itineraries:
        if (new_itin_start >= existing_start_time and new_itin_start < existing_end_time) or \
           (new_itin_end > existing_start_time and new_itin_end <= existing_end_time):
            return False

    return True