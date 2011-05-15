#!/bin/bash

LOGDIR=/home/mote/logs/lak_load
export DISPLAY=:0

python /home/mote/dev/self_tracking/log_5m_cpu_load.py >> $LOGDIR/cpu.log
python /home/mote/dev/self_tracking/log_net_load.py >> $LOGDIR/net_usage.log
python /home/mote/dev/self_tracking/log_ping.py >> $LOGDIR/ping.log
python /home/mote/dev/self_tracking/log_screensaver.py >> $LOGDIR/screensaver.log
python /home/mote/dev/self_tracking/log_weather.py >> $LOGDIR/weather.log
python /home/mote/dev/self_tracking/log_active_window.py >> $LOGDIR/active_window.log
