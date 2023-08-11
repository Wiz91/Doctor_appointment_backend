from datetime import datetime

def time_calculater(in_time,out_time):
    # Specify the two times
    time1 = datetime.strptime(in_time, '%H:%M:%S')
    time2 = datetime.strptime(out_time, '%H:%M:%S')

    # Calculate the time difference
    time_diff = time2 - time1

    # Extract the hours and minutes from the time difference
    hours = time_diff.seconds / 3600
    minutes = (time_diff.seconds % 3600) // 60

    # Print the time difference
    # print(f'Time difference: {hours} hours and {minutes} minutes')
    return hours

# a=time_calculater('10:00:00','19:00:00')
# print(a)
