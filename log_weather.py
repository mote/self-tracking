#!/usr/bin/python
"Output current weather"

from lib import pywapi
import util


def get_weather(loc='90034'):
  weather = pywapi.get_weather_from_google(loc)
  fields = {}

  try:
    h = weather['current_conditions']['humidity'].split()[-1].rstrip('%')
    fields['humidity'] = h
  except:
    pass
  try:
    wind = weather['current_conditions']['wind_condition']
    wind = wind.split()
    fields['wind_dir'] = wind[1]
    fields['wind_speed'] = wind[-2]
  except:
    pass
  try:
    condition = weather['current_conditions']['condition'].lower()
    fields['condition'] = condition.replace(' ', '_')
  except:
    pass

  try:
    fields['temp'] = weather['current_conditions']['temp_f']
  except:
    pass
  return fields


now = util.now_datetime()

for loc in ['90034', '90401', 'seattle', 'kirkland', 'taipei', 'taichung']:
  for k, v in get_weather(loc).items():
    print '%s\t%s_%s\t%s' % (now, loc, k, v)
