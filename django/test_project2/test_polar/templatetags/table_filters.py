from datetime import datetime
from typing import Union
from django import template


register = template.Library()


@register.filter(name="weekday")
def weekday(datestr: str):
    # print(datestr)
    weekday = datetime.strptime(datestr, "%Y-%m-%d").strftime("%a")
    return weekday + " " + datestr


@register.filter(name="kmh2minkm")
def kmh2minkm(speed: Union[float, None]) -> str:
    if speed:
        # print(speed)
        temp = 60 * 1 / speed
        minutes = int(temp)
        seconds = round((temp - minutes) * 60)
        minkm_str = str(minutes) + ":" + "{:0>2}".format(seconds)
    else:
        minkm_str = "-"
    return minkm_str
