#!/bin/bash
LOGDIR=/home/mote/logs/lak_load
python /home/mote/dev/self_tracking/log_bandwidth.py >> $LOGDIR/net_bandwidth.log
