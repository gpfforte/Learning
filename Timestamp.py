import datetime as dt
now = dt.datetime.now()
date_time = now.strftime("%Y-%m-%d-%H%M%S")
print("date and time:", date_time)
other_date = now + dt.timedelta(days=1)
print (other_date)
print (dt.timedelta(days=1))