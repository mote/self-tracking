#!/usr/bin/python
"Get stats about yesterdays commands from bash log."
import datetime
import operator
import sys


yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
yesterday = yesterday.strftime('%Y%m%d')

def parse_logfile(logfile, daystr):
  cmds = {}
  for line in open(logfile):
    if not line.startswith(daystr):
      continue
    fields = line.strip().split()
    try:
      cmd = fields[3]
      cmds[cmd] = cmds.get(cmd, 0) + 1
    except:
      continue
  return cmds


def yield_inorder(mydict, min):
  inorder = sorted(mydict.iteritems(), key=operator.itemgetter(1),
      reverse=True)
  for k, c in inorder:
    if c > min:
      yield k, c


logfile = '/home/mote/logs/vim_history.log'
cmds = parse_logfile(logfile, yesterday)
print 'saved-total', sum(cmds.values())

