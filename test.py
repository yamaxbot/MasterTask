import datetime
time_moscow = datetime.timezone(datetime.timedelta(hours=3))
today = str(datetime.datetime.now(time_moscow).time())[:5]
print(today)