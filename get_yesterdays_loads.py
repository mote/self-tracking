#!/usr/bin/python
"Get average loads from yesterday."
import datetime
import sys


def avg(items):
  if not items:
    return 0.0
  items = [float(f) for f in items]
  return sum(items)/len(items)

def get_avg(logpath, daystr):
  items = []
  for line in open(logpath):
    if not line.startswith(daystr):
      continue
    fields = line.split()
    items.append(fields[-1])
  return avg(items)

def get_keyed_avg(logpath, daystr):
  keyed = {}
  for line in open(logpath):
    if not line.startswith(daystr):
      continue
    fields = line.strip().split()
    try:
      key = fields[1].strip()
      val = float(fields[2])
      vals = keyed.get(key, [])
      vals.append(val)
      keyed[key] = vals
    except:
      continue
  keyed = dict((k, avg(v)) for k, v in keyed.items())
  return keyed

def count_keys(logpath, daystr):
  counts = {}
  for line in open(logpath):
    if not line.startswith(daystr):
      continue
    fields = line.strip().split()
    val = fields[2]
    counts[val] = counts.get(val, 0) + 1
  return counts

def is_day(yyyymmdd_hhmm):
  hour = int(yyyymmdd_hhmm[-4:-1])
  return hour > 6 and hour < 8

def get_keyed_min_max_avg(logpath, daystr):
  keyed = {}
  for line in open(logpath):
    if not line.startswith(daystr):
      continue
    fields = line.strip().split()
    try:
      key = fields[1].strip()
      val = float(fields[2])
      vals = keyed.get(key, [])
      vals.append(val)
      keyed[key] = vals
    except:
      continue
  avgs = dict((k, avg(v)) for k, v in keyed.items())
  mins = dict((k, min(v)) for k, v in keyed.items())
  maxs = dict((k, max(v)) for k, v in keyed.items())
  return mins, maxs, avgs

  
def print_float_dict(prefix, d):
  for k, v in d.items():
    print '%s-%s\t%.2f' % (prefix, k, v)


def main():
  NET_USAGE_LOAD  = '/home/mote/logs/lak_load/net_usage.log'
  BW_LOAD  = '/home/mote/logs/lak_load/net_bandwidth.log'
  CPU_LOAD  = '/home/mote/logs/lak_load/cpu.log'
  PING_LOAD = '/home/mote/logs/lak_load/ping.log'
  SCREENSAVER = '/home/mote/logs/lak_load/screensaver.log'
  WEATHER = '/home/mote/logs/weather.log'

  yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
  yesterday = yesterday.strftime('%Y%m%d')

  # CPU
  cpu = get_avg(CPU_LOAD, yesterday)
  print 'cpu\t%.2f' % cpu

  # Net Usage
  (u_min, u_max, u_avg) = get_keyed_min_max_avg(NET_USAGE_LOAD, yesterday)
  print_float_dict('net', u_avg)
  print_float_dict('net-min', u_min)
  print_float_dict('net-max', u_max)

  # Bandwidth
  bw_min, bw_max, bw_avg = get_keyed_min_max_avg(BW_LOAD, yesterday)
  print_float_dict('bw', bw_avg)
  print_float_dict('bw-min', bw_min)
  print_float_dict('bw-max', bw_max)

  # Ping
  p_min, p_max, p_avg = get_keyed_min_max_avg(PING_LOAD, yesterday)
  print_float_dict('ping', p_avg)
  print_float_dict('ping-min', p_min)
  print_float_dict('ping-max', p_max)

  # Screensaver
  screenkeys = count_keys(SCREENSAVER, yesterday)
  print 'screensaver-hours_on\t%.2f' % (screenkeys.get('1', 0) / 12.0)
  print 'screensaver-hours_off\t%.2f' % (screenkeys.get('0', 0) / 12.0)

  # Weather
  w_min, w_max, w_avg = get_keyed_min_max_avg(WEATHER, yesterday)
  print_float_dict('weather', w_avg)
  print_float_dict('weather-min', w_min)
  print_float_dict('weather-max', w_max)


  # TODO: aggregate wind direction
  # TODO: better aggregation of averages (daytime and nighttime)
  # TODO: see how often stats change, and change polling frequency
  # TODO: fix parsing library so that it returns results for Taiwan


if __name__ == '__main__':
  main()
