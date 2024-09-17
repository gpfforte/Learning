import pandas as pd
import numpy as np
import holidays
import datetime as dt


today = dt.datetime.now()
# print(today.day)

if today.month < 10:
    mese = "0" + str(today.month)
else:
    mese = str(today.month)
if today.day < 10:
    giorno = "0" + str(today.day)
else:
    giorno = str(today.day)

oggi = str(today.year) + "-" + mese + "-" + giorno

print(today.hour)
print(today.minute)
print(oggi)

list_hol = []
for date, name in sorted(holidays.IT(years=today.year).items()):
    list_hol.append(date)


def add_working_days(x):
    global list_hol

    days_elapsed = 0
    while days_elapsed < x[1]:
        test_date = x[0]+dt.timedelta(days=1)
        # print(type(test_date))
        x[0] = test_date
        if test_date.weekday() > 4 or test_date.to_pydatetime() in list_hol:
            # if a weekend or federal holiday, skip
            continue
        else:
            # if a workday, count as a day
            days_elapsed += 1

    return x[0]


df = {'start': ['2021-01-01', '2021-04-30'],
      'business_days': [1, 4]}
df = pd.DataFrame(df)

df['start'] = pd.to_datetime(df['start'])


df['end'] = df[['start', 'business_days']].apply(add_working_days, axis=1)

print(df.head())
