#!/usr/bin/python
"Parse bmon to output current incoming/outgoing bandwidth to a file."
import datetime
import subprocess

PS_CMD = "ps aux -U mote -u mote | awk '{print $11}' | sort | uniq -c"

def _run(cmd):
  return subprocess.Popen(cmd, shell=True,
      stdout=subprocess.PIPE, close_fds=True).stdout.read().rstrip()

def avg(items):
  return float(sum(items)) / len(items)

CMD_MAP = {
    '/usr/lib/chromium-browser/chromium-browser' : 'chrome',
    '/opt/google/chrome/chrome' : 'chrome',
    'ssh' : 'ssh',
    'vi' : 'vi',
    'gvim' : 'vi',
    'bash' : 'bash',
    'zsh' : 'zsh',
    }
def parse_ps(ps_str):
  counts = {}
  for line in ps_str.strip().split('\n'):
    try:
      fields = line.strip().split()
      count = int(fields[0])
      cmd = fields[1]
      cmd = cmd.lstrip('-')
      cmd = CMD_MAP.get(cmd, '')
      if not cmd:
        continue
      counts[cmd] = counts.get(cmd, 0) + count
    except:
      continue
  return counts

counts = parse_ps(_run(PS_CMD))

now = datetime.datetime.now()
now = now.strftime('%Y%m%d.%H%M')

for cmd, count in counts.items():
  print 'cmd-%s' % cmd, count
