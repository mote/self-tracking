#!/usr/bin/python
"Parse bmon to output current incoming/outgoing bandwidth to a file."

import util

CMD = "bmon -p 'eth0' -o 'ascii:noheader;quitafter=20'"

def avg(items):
  if not items:
    return -1
  return float(sum(items)) / len(items)

def rescale_to_kib(unit):
  """Takes string like 52.00GiB, 470KiB, 40B and rescales to KiB units."""
  if unit.endswith('KiB'):
    return float(unit[:-3])
  elif unit.endswith('MiB'):
    return float(unit[:-3])*1000.0
  elif unit.endswith('GiB'):
    return float(unit[:-3])* 1000.0 * 1000.0
  elif unit.endswith('B'):
    return float(unit[:-1])/1000.0

def parse_bmon(bmon_str):
  rxs = []
  txs = []
  for line in bmon_str.split('\n')[2:]:
    fields = line.split()
    rx = fields[1]
    tx = fields[3]
    rx = rescale_to_kib(rx)
    tx = rescale_to_kib(tx)
    rxs.append(rx)
    txs.append(tx)
  return (avg(rxs), avg(txs))


bmon = util.run(CMD)
(bw_in, bw_out) = parse_bmon(bmon)
bw_in = '%.2f' % bw_in
bw_out = '%.2f' % bw_out

now = util.now_datetime()
print '%s\tin\t%s' % (now, bw_in)
print '%s\tout\t%s' % (now, bw_out)
