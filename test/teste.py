from datetime import datetime

date_time_str = '2021-07-01 21:06:16.383707'

date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')


print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)

print(datetime.now())