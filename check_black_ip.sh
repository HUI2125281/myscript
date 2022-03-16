#!/bin/bash
#function:ban ip for nginx
#modified by http://www.juyimeng.com/

filename=/usr/local/nginx/conf/blacklist.conf
cat  /home/wwwlogs/*.log |grep "POST.*/wp-login"  | awk '{print $1,$7}' | awk '{print $1}' | sort | uniq -c | sort -rn | awk '{if($1>6)print "deny "$2";"}' > $filename
cat  /home/wwwlogs/*.log | awk '{print $1,$7}'|grep -v "/lixxxe" | awk '{print $1}' | sort | uniq -c | sort -rn  | awk '{if($1>5999) print "deny "$2";"}' >> $filename
filesize=$(stat -c%s "$filename")
echo "Size of $filename = $filesize bytes."
if (( filesize > 0 )); then
        /usr/bin/lnmp nginx reload
        echo "reload nginx"
else
        echo "fine"
fi
