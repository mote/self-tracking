#!/usr/bin/python
"""Log currect active window to file.
You must have xdotool installed.
"""

import util

CMD = 'xwininfo -display :0 -id "$(xdotool getactivewindow)" | grep xwininfo'

def parse(out_str):
  #return out_str
  fields = out_str.split('"')
  return fields[-2]

val = parse(util.run(CMD))
print util.now_datetime(), val 
