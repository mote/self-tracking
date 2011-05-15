#!/usr/bin/python
"Parse ping to see current latency."

import util

PING = "ping -c 10 %s"

def avg(items):
  if not items:
    return -1
  return float(sum(items)) / len(items)

def parse_ping(ping_str):
  pings = []
  for line in ping_str.strip().split('\n'):
    try:
      fields = line.strip().split()
      pings.append(float(fields[-2][5:]))
    except:
      continue
  if not pings:
    return (-1, -1)
  return avg(pings[1:]), max(pings)

(mote_avg, mote_max) = parse_ping(util.run(PING % 'motespace.com'))
(goog_avg, goog_max) = parse_ping(util.run(PING % 'google.com'))

now = util.now_datetime()

print '%s\tmotespace-avg\t%.2f' % (now, mote_avg)
print '%s\tmotespace-max\t%.2f' % (now, mote_max)
print '%s\tgoogle-avg\t%.2f' % (now, goog_avg)
print '%s\tgoogle-max\t%.2f' % (now, goog_max)
