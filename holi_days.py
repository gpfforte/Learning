import holidays
import datetime as dt

today = dt.datetime.now()

list_hol = []
list_year = [today.year, today.year+1]
for year in list_year:
    for date, name in sorted(holidays.IT(years=year).items()):
        list_hol.append([date, name])
        print(date, name)

print(list_hol)
print("###########################")
list_hol = [date for date, name in sorted(
    holidays.IT(years=[today.year, today.year+1]).items())]

print(list_hol)
