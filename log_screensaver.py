#!/usr/bin/python
"""Look to see if the screensaver is running.

glslideshow
gnome-screensaver
"""

import util

CMD = "ps aux | grep glslideshow | grep -v grep"


def is_running():
  data = util.run(CMD)
  if data:
    return 1
  return 0

now = util.now_datetime()

print '%s\tscreensaver\t%d' % (now, is_running())
