#!/usr/bin/python
"Parse bmon to output current incoming/outgoing bandwidth to a file."
import util
import datetime
import sys

CMD_IN = 'curl -o /dev/null --stderr - motespace.com/random_10M'
CMD_OUT = 'scp /home/mote/dev/self_tracking/random_5M motespace.com:/dev/null'


def rescale_to_k(k_str):
  k_str = k_str.upper()
  if k_str.endswith('K'):
    return int(k_str[:-1])
  elif k_str.endswith('M'):
    return int(k_str[:-1]) * 1000
  elif k_str.endswith('G'):
    return int(k_str[:-1]) * 1000 * 1000
  else:
    return int(k_str) / 1000.0


def parse_curl(curl_str):
  try:
    curl_str = curl_str.split('\r')[-1]
    fields = curl_str.split()
    return rescale_to_k(fields[6])
  except Exception, e:
    sys.stderr.write('Problem!: %s' % e)
    return -1


def calc_in():
  curl_txt = util.run(CMD_IN)
  bw_in = parse_curl(curl_txt)
  return bw_in


def calc_out():
  before = datetime.datetime.now()
  util.run(CMD_OUT)
  after = datetime.datetime.now()

  elapsed = after - before
  elapsed = (elapsed.seconds) + (elapsed.microseconds / 1000000.0)
  # took this many seconds to upload 5M, so, in K...
  bw_out = 5000 / elapsed
  return bw_out


now = util.now_datetime()

print '%s\tin\t%.2f' % (now, calc_in())
print '%s\tout\t%.2f' % (now, calc_out())
