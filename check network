#!/bin/sh
nc -z -w 3 180.101.49.11 80 || nc -z -w 3 180.163.122.229 80
if [ $? -eq 0 ]
then
  echo -e $(date) "The script ran ok" >> /var/log/checknet.log
  exit 0
else
  echo -e $(date) "The script failed" >> /var/log/checknet.log
  vim-cmd vmsvc/power.reset 2
  exit 1
fi
