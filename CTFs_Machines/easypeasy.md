## Enumeration
**Port**
```
└─# nmap -sV -T5 10.10.227.90 -p1-10000
Not shown: 8097 closed tcp ports (reset), 1901 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx 1.16.1
6498/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
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
In hidden i found a new other website