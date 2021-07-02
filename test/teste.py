from datetime import datetime

date_time_str = '18/09/19 01:55:19.410430'

date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S.%f')


print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)

print(datetime.now())