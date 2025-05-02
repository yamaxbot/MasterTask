import datetime

offset = datetime.timezone(datetime.timedelta(hours=3))

print(datetime.datetime.now(offset).date())