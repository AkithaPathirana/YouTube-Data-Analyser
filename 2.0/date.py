from datetime import date

date1=date.fromisoformat('2019-12-24')
date2=date.fromisoformat('2019-11-04')
delta=date1-date2
print(delta.days)