#!/usr/bin/bash
import datetime
from lib import pywapi

def parse_time(timestr):
  """Parse string like '6:09 am', '5:56 pm' into a 24H string."""
  fields = timestr.split(':')
  hour = int(fields[0])
  minute = fields[1]
  if minute.endswith('pm'):
    hour += 12
  minute = int(minute[0:2])
  if hour < 10:
    hour = '0%d' % hour
  else:
    hour = str(hour)
  if minute < 10:
    minute = '0%d' % minute
  else:
    minute = str(minute)
  return hour + minute


def get_sunrise_sunset(loc):
  weather = pywapi.get_weather_from_yahoo(loc)
  sunrise = parse_time(weather['astronomy']['sunrise'])
  sunset = parse_time(weather['astronomy']['sunset'])
  return sunrise, sunset


locs = {
    '90034': '90034',
    '98101': 'seattle',
    'TWXX0021': 'taipei',
    }
for loc, name in locs.items():
  (sunrise, sunset) = get_sunrise_sunset(loc)
  print '%s-sunrise' % name, sunrise
  print '%s-sunset' % name, sunset
