"Utility functions"

import datetime
import subprocess

def run(cmd):
  return subprocess.Popen(cmd, shell=True,
      stdout=subprocess.PIPE, close_fds=True).stdout.read().rstrip()

def now_date():
  return datetime.datetime.now().strftime('%Y%m%d')

def now_datetime():
  return datetime.datetime.now().strftime('%Y%m%d.%H%M')

