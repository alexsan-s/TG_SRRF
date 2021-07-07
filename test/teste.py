from datetime import datetime

date_time_str = '1992-06-22 00:00:00'

date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')


print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)

print(datetime.now().date())