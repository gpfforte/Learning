import pandas as pd
import numpy as np
import holidays


holidays_country = holidays.CountryHoliday("IT")
for date, name in sorted(holidays.IT(years=2021).items()):
    print(date, name)
print(type(holidays_country))

list_hol = []

print(sorted(holidays.IT(years=2021).items()))
for date, name in sorted(holidays.IT(years=2021).items()):
    list_hol.append(date)

print(list_hol)

df = {'start': ['2021-01-01', '2021-04-01'],
      'end': ['2021-01-02', '2021-04-07']}
df = pd.DataFrame(df)


def f(x):
    return np.busday_count(x[0], x[1], holidays=holidays_country[x[0]:x[1]])


df['business_days'] = df[['start', 'end']].apply(f, axis=1)

print(df.head())
