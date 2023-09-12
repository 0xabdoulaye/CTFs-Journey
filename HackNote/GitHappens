A tryhackme Rooms 
Links : https://tryhackme.com/room/githappens
tags : git, web, github
target : http://10.10.239.43/
Recon Time :
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# nmap -sC -sV -T4 10.10.239.43
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: Super Awesome Site!
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Web Dirs:
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.10.239.43/FUZZ

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.3.1 Kali Exclusive <3
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.239.43/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

                        [Status: 200, Size: 6890, Words: 541, Lines: 61]
.git/HEAD               [Status: 200, Size: 23, Words: 2, Lines: 2]
css                     [Status: 301, Size: 194, Words: 7, Lines: 8]

I found .git now i need to exploit it 
I use Gitools
I analyzed the git log to find commit 
and i found the pass


+        if (
+          username === "admin" &&
+          password === "Th1s_1s_4_L0ng_4nd_S3cur3_P4ssw0rd!"
+        ) {
+          document.cookie = "login=1";
+          window.location.href = "/dashboard.html";
