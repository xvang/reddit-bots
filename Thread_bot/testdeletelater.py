import time
import datetime
from time import timezone

import calendar



sss = ['Monday', 'March', '16', '22', '30', 'PM']



dt = datetime.datetime(2015, 3, 16, 22, 30, 0)

s = time.mktime(dt.timetuple())

print(s)
