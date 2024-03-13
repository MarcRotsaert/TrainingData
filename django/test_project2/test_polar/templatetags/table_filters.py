from datetime import datetime
from typing import Union
from django import template


register = template.Library()


@register.filter(name="weekday")
def weekday(datestr: Union[str, datetime]):
    if isinstance(datestr, datetime):
        # garminfit hack
        datestr = str(datestr)[0:10]
    # print(type(datestr))
    weekday = datetime.strptime(datestr, "%Y-%m-%d").strftime("%a")
    return weekday + " " + datestr


@register.filter(name="kmh2minkm")
def kmh2minkm(speed: Union[float, None]) -> str:
    if speed:
        # print(speed)
        temp = 60 * 1 / speed
        minutes = int(temp)
        seconds = round((temp - minutes) * 60)
        if seconds == 60:
            seconds = 0
            minutes += 1

        minkm_str = str(minutes) + ":" + "{:0>2}".format(seconds)
    else:
        minkm_str = "-"
    return minkm_str


@register.filter(name="duration2min")
def duration2min(duration: Union[float, None]) -> str:
    if duration:
        temp = float(duration) / 60
        minutes = int(temp)
        seconds = round((temp - minutes) * 60)
        if seconds == 60:
            seconds = 0
            minutes += 1
        durationmin = str(minutes) + ":" + "{:0>2}".format(seconds)
    else:
        durationmin = "-"
    return durationmin
