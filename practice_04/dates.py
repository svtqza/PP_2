#task number 1
from datetime import datetime, timedelta

data = datetime.now()  
new_date = data - timedelta(days=5)

print('Current date:', data.strftime("%Y-%m-%d"))
print('Date 5 days ago:', new_date.strftime("%Y-%m-%d"))


#task number 2
from datetime import datetime, timedelta

data=datetime.now()
yesterday=data-timedelta(days=1)
tomorrow=data+timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:", data.strftime("%Y-%m-%d"))
print("Tomorrow:", tomorrow.strftime("%Y-%m-%d"))


#task number 3
from datetime import datetime

now = datetime.now()

without_microseconds = now.replace(microsecond=0)

print("Original datetime:", now)
print("Without microseconds:", without_microseconds)

#task number 4
from datetime import datetime

date_str1 = input("Enter first date (YYYY-MM-DD HH:MM:SS): ")
date_str2 = input("Enter second date (YYYY-MM-DD HH:MM:SS): ")

date1 = datetime.strptime(date_str1, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date_str2, "%Y-%m-%d %H:%M:%S")

diff = date2 - date1 

seconds = diff.total_seconds()
print("Difference in seconds:", seconds)
