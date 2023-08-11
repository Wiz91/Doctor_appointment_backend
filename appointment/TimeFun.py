
import datetime


def time_converet_AM_PM(time):
    # Create a time object
    time_str = time
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()

    # Format the time object as a string with the desired format
    formatted_time = time_obj.strftime("%I:%M %p")

    # Print the formatted time
    return formatted_time