#!/bin/sh
#延迟30秒，避免拨号没有成功之前，造成反复重启。
sleep 30
nc -z -w 3 180.101.49.11 80 || nc -z -w 3 180.163.122.229 80
if [ $? -eq 0 ]; then
  echo -e $(date) "The script ran ok" >> /vmfs/volumes/datastore1/log/checknet.log
  #exit 0
else
  echo -e $(date) "The script failed" >> /vmfs/volumes/datastore1/log/checknet.log
  vim-cmd vmsvc/power.reset 2
  #exit 1
fi
