#!/bin/bash
#function:cut nginx log files for lnmp
#author: http://lnmp.org
#modified by http://www.juyimeng.com/lnmp-nginx-log-cut-per-day-rotation.html

#set the path to nginx log files
log_files_path="/home/wwwlogs/"
#log_files_dir=${log_files_path}$(date -d "yesterday" +"%Y")/$(date -d "yesterday" +"%m")
log_files_dir=${log_files_path}bak/
#set nginx log files you want to cut
#get log files list,exclude error.log
log_files_name=($(/bin/find $log_files_path -maxdepth 1 -name "*.log" |grep -v error| awk -F/ '{ print $NF }'))
#set the path to nginx.
nginx_sbin="/usr/local/nginx/sbin/nginx"
#Set how long you want to save
save_days=30
############################################
#Please do not modify the following script #
############################################
mkdir -p $log_files_dir
log_files_num=${#log_files_name[@]}

#cut nginx log files
for((i=0;i<$log_files_num;i++));do
       mv ${log_files_path}${log_files_name[i]} ${log_files_dir}$(date -d "yesterday" +"%Y%m%d_%s")_${log_files_name[i]}
done
#delete $save_days ago nginx log files
find $log_files_path -mtime +$save_days -exec rm -rf {} \;
echo "log cuted "$(date -d "yesterday" +"%Y%m%d_%s")
#reload nginx
$nginx_sbin -s reload
du -s /* >/home/wwwlogs/du/$(date -d "yesterday" +"%Y%m%d_%s").du.log
df  >>/home/wwwlogs/du/$(date -d "yesterday" +"%Y%m%d_%s").duall.log
