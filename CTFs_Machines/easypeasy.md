## Enumeration
**Port**
```
└─# nmap -sV -T5 10.10.227.90 -p1-10000
Not shown: 8097 closed tcp ports (reset), 1901 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx 1.16.1
6498/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
65524/tcp open http syn-ack Apache httpd 2.4.43 ((Ubuntu))
| http-methods:
| Supported Methods: OPTIONS HEAD GET POST
| http-robots.txt: 1 disallowed entry
|/
|_http-server-header: Apache/2.4.43 (Ubuntu)
|_http-title: Apache2 Debian Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
**Directory Bruteforce**
```terminal
└─# ffuf -u "http://easypeasy.thm/FUZZ" -w /usr/share/wordlists/dirb/common.txt                             

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.5.0 Kali Exclusive <3
________________________________________________
                        [Status: 200, Size: 612, Words: 79, Lines: 26, Duration: 2448ms]
hidden                  [Status: 301, Size: 169, Words: 5, Lines: 8, Duration: 1365ms]
index.html              [Status: 200, Size: 612, Words: 79, Lines: 26, Duration: 1645ms]
robots.txt
```
In hidden i found a new other website, i will fuzz on this hidden
```
└─# ffuf -u "http://10.10.252.94/hidden/FUZZ" -w /usr/share/wordlists/dirb/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.5.0 Kali Exclusive <3
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.252.94/hidden/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 390, Words: 47, Lines: 19, Duration: 975ms]
index.html              [Status: 200, Size: 390, Words: 47, Lines: 19, Duration: 969ms]
whatever                [Status: 301, Size: 169, Words: 5, Lines: 8, Duration: 965ms]
```
In the whatever i inspect the source-code and found.
view-source:http://10.10.252.94/hidden/whatever/
`p hidden>ZmxhZ3tmMXJzN19mbDRnfQ==</p>`
```
└─# base=ZmxhZ3tmMXJzN19mbDRnfQ==
                                                                                                                                     
┌──(root㉿1337)-[/home/bloman/CTFs/Boot2root/Tryhackme]
└─# echo $base | base64 -d      
flag{f1rs7_fl4g}  
```