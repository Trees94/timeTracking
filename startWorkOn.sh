#!/usr/bin/env bash
TIME_TRACKING_DIR="/home/local/ANT/tomrees/time_tracking"

current_date_dir=$TIME_TRACKING_DIR/$(date +"%Y/%m")
mkdir -p $current_date_dir
echo "$(date -R) : $@" >> $current_date_dir/timeTracking.md 


