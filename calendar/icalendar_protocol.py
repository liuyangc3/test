import pytz
import datetime
import icalendar
import dateutil.relativedelta as rdelta

tz = pytz.timezone('Asia/Shanghai')

today = datetime.datetime.today()
# 本周一 0点0分
past_monday = today + rdelta.relativedelta(days=-1, weekday=rdelta.MO(-1))
monday = datetime.datetime.combine(past_monday, datetime.time.min).replace(tzinfo=tz)
# 本周日 23点59分
next_sunday = past_monday + rdelta.relativedelta(days=6)
sunday = datetime.datetime.combine(next_sunday, datetime.time.max).replace(tzinfo=tz)


with open('t2.ics', 'rb') as f:
    data = f.read()
    cal = icalendar.Calendar.from_ical(data)

    for e in cal.walk('vevent'):
        dt = e.get("dtstart").dt
        if monday < dt < sunday:
            print(e.get("DESCRIPTION"))
