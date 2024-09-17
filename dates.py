import datetime
import pytz
import locale
locale.setlocale(locale.LC_TIME, "it_IT")
# Naive
# d = datetime.date(2001, 9, 11)
tday = datetime.date.today()
now = datetime.datetime.now()
print(f"Today is {tday}")
year = now.year

# weekday() - Monday is 0 and Sunday is 6
# print(tday)

# isoweekday() - Monday is 1 and Sunday is 7
# print(tday)


# datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

tdelta = datetime.timedelta(hours=12)
print(tdelta)
# print(tday + tdelta)

# date2 = date1 + timedelta
# timedelta = date1 - date2

bday = datetime.date(year+1, 3, 13)

till_bday = bday - tday


print(f"Days till Birthday {till_bday.days}")

t = datetime.time(9, 30, 45, 100000)

# dt = datetime.datetime.today()
# dtnow = datetime.datetime.now()
# print(dir(datetime.datetime))
# print(dt)
# print(dtnow)

dt = datetime.datetime(2022, 3, 13, 12, 30, 45, tzinfo=pytz.UTC)
print(dt)
print(dt.isoformat())
print(dt.isoweekday())
print(dt.isocalendar())

dt_utcnow = datetime.datetime.now(tz=pytz.UTC)
print("dt_utcnow", dt_utcnow)

dt_utcnow2 = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
print("dt_utcnow2", dt_utcnow2)

# dt_mtn = dt_utcnow.astimezone(pytz.timezone('US/Mountain'))
# print(dt_mtn)

dt_now = datetime.datetime.now()
print("dt_now", dt_now)
ceu_tz = pytz.timezone('Europe/Rome')
print("ceu_tz.localize(dt_now)", ceu_tz.localize(dt_now))
dt_ceu = ceu_tz.normalize(ceu_tz.localize(dt_now))

print("dt_ceu", dt_ceu)

# WRONG BEGIN
dt_now = datetime.datetime.now()
utc_tz = pytz.timezone('UTC')
dt_utc = utc_tz.normalize(utc_tz.localize(dt_now))
# Wrong because it has been localized to the wrong timezone
print("WRONG dt_utc", dt_utc)
# WRONG END

dt_east = dt_ceu.astimezone(pytz.timezone('US/Eastern'))
print("dt_east", dt_east)

print("strftime", dt_ceu.strftime('%B %d, %Y').title())

dt_str = 'Marzo 13, 2022'
dt = datetime.datetime.strptime(dt_str, '%B %d, %Y')
print("strptime", dt)
print("strptime", dt.date())

# strftime - Datetime to String
# strptime - String to Datetime
# print('The supported timezones by the pytz module:',
#       pytz.all_timezones, '\n')

# print('all the supported timezones set:',
#       pytz.all_timezones_set, '\n')

# print('Commonly used time-zones:',
#       pytz.common_timezones, '\n')

# print('Commonly used time-zones-set:',
#       pytz.common_timezones_set, '\n')

# print('country_names =')

for key, val in pytz.country_names.items():
    if key == "IT":
        print(key, '=', val, end=',')

print('\n')
print('equivalent country name to the input code: =',
      pytz.country_names['IT'])

print('\n')
print('Time-zones supported by Italy =', pytz.country_timezones['IT'])
