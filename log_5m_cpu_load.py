#!/usr/bin/python
"Parse `uptime` to output current 5m CPU load to a file."

import util

def parse_uptime(uptime_str):
  fields = uptime_str.split()
  fields = [f.rstrip(',') for f in fields]
  vals = {
        'time'    : fields[0],
        'users'   : fields[-7],
        'load_1m' : fields[-3],
        'load_5m' : fields[-2],
        'load_15m': fields[-1],
        }
  if fields[3].startswith('day'):
    vals['updays'] = fields[2]
  else:
    vals['updays'] = 0
  return vals


uptime = util.run('uptime')
fields = parse_uptime(uptime)

print util.now_datetime(), fields['load_5m']

