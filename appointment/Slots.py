import datetime


def Slots(from_time,no_of_slots):
    custom_start_time = from_time


    start_time = datetime.datetime.strptime(custom_start_time, "%H:%M:%S")

    time_slot = datetime.timedelta(minutes=15)  # Set the duration of each time slot

    slots = [] 
  
    for i in range(no_of_slots):  # 9 hours = 18 slots (30 minutes each)
        current_slot = start_time + i * time_slot
        slots.append(current_slot.strftime("%I:%M %p"))
    # print(start_time.strftime("%H:%M:%S"))
    return slots






a= Slots("10:00:00",36)
print(a)