#!/bin/bash
echo "Log Parsing"
log_file="/var/log/syslog"
if [ ! -f  "$log_file" ]; then
  echo "Log file not found: $log_file"

exit 1

fi

echo "Top 5 IP addresses in $log_file"
grep -oE "\b([0-9]{1,3}\. 
