## Recon
```
└─# nmap -sV -Pn -p1-65535 --min-rate 3000 $ip
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-02-12 17:06 CST
Nmap scan report for 192.168.56.108
Host is up (0.00048s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
MAC Address: 08:00:27:C9:B4:A2 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```


## Fuzz
```
└─# ffuf -u "http://192.168.56.108/FUZZ" -w /usr/share/wordlists/dirb/common.txt

 :: Method           : GET
 :: URL              : http://192.168.56.108/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 1373, Words: 129, Lines: 42, Duration: 4ms]
drupal                  [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 1ms]
index.html              [Status: 200, Size: 1373, Words: 129, Lines: 42, Duration: 0ms]
.hta                    [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 292ms]
.htpasswd               [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 292ms]
Makefile                [Status: 200, Size: 11, Words: 1, Lines: 2, Duration: 2ms]
MANIFEST.MF             [Status: 200, Size: 11, Words: 1, Lines: 2, Duration: 1ms]
.htaccess               [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 382ms]
phpmyadmin              [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 0ms]
privacy                 [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 0ms]
robots.txt              [Status: 200, Size: 37, Words: 3, Lines: 2, Duration: 3ms]
secret                  [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 0ms]
server-status           [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 1ms]
wp-admin                [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 0ms]

```

`User-agent: *
Disallow: /eventadmins`
```
man there's a problem with ssh

john said "it's poisonous!!! stay away!!!"

idk if he's mentally challenged

please find and fix it

also check /littlequeenofspades.html

your buddy, buddyG

Now, she is a little queen of spades, and the men will not let her be
Mmmm, she is the little queen of spades, and the men will not let her be
Everytime she makes a spread, hoo fair brown, cold chill just runs all over me
I'm gon' get me a gamblin' woman, if the last thing that I do
Eee, gon' get me a gamblin' woman, if it's the last thing that I do
Well, a man don't need a woman, ooh fair brown, that he got to give all his money to
Everybody say she got a mojo, now she's been usin' that stuff
Mmmm, mmmm, 'verybody says she got a mojo, 'cause she been usin' that stuff
But she got a way trimmin' down, hoo fair brown, and I mean it's most too tough
Now, little girl, since I am the king, baby, and you is a queen
Ooo eee, since I am the king baby, and you is a queen
Le's us put our heads together, hoo fair brown, then we can make our money green
aW50cnVkZXI/IEwyRmtiV2x1YzJacGVHbDBMbkJvY0E9PQ==
```
user: john
```
└─# echo $base | base64 -d
intruder? L2FkbWluc2ZpeGl0LnBocA==  
└─# base=L2FkbWluc2ZpeGl0LnBocA==

┌──(root㉿xXxX)-[/home/blo/CTFs/CTFs-Journey/CTFs_Machines]
└─# echo $base | base64 -d
/adminsfixit.php  
#######################################################################

ssh auth log

============

i hope some wacky and uncharacteristic thing would not happen

this job is fucking poisonous and im boutta planck length away from quitting this hoe

-abuzer komurcu

#######################################################################

Feb 12 17:04:01 driftingblues CRON[753]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:04:01 driftingblues CRON[753]: pam_unix(cron:session): session closed for user root Feb 12 17:05:01 driftingblues CRON[757]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:05:01 driftingblues CRON[757]: pam_unix(cron:session): session closed for user root Feb 12 17:06:01 driftingblues CRON[763]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:06:01 driftingblues CRON[763]: pam_unix(cron:session): session closed for user root Feb 12 17:06:36 driftingblues sshd[767]: Did not receive identification string from 192.168.56.1 port 46008 Feb 12 17:07:01 driftingblues CRON[768]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:07:01 driftingblues CRON[768]: pam_unix(cron:session): session closed for user root Feb 12 17:08:01 driftingblues CRON[791]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:08:01 driftingblues CRON[791]: pam_unix(cron:session): session closed for user root Feb 12 17:09:01 driftingblues CRON[798]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:09:01 driftingblues CRON[797]: pam_unix(cron:session): session opened for user root by (uid=0) Feb 12 17:09:02 driftingblues CRON[797]: pam_unix(cron:session): session closed for user root Feb 12 17:09:02 driftingblues CRON[798]: pam_unix(cron:session): session closed for user root Feb 12 17:10:01 driftingblues CRON[856]: pam_unix(cron:session): session opened for user root by (uid=0) 
```