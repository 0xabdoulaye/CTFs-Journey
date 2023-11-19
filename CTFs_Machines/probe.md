## Enum

```
└─# nmap -p- --min-rate 10000 10.10.91.206                                
Not shown: 64031 filtered tcp ports (no-response), 1501 closed tcp ports (reset)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https

└─# nmap -sS -vvv -Pn --min-rate 2000 10.10.91.206
Not shown: 570 closed tcp ports (reset), 426 filtered tcp ports (no-response)
PORT     STATE SERVICE REASON
22/tcp   open  ssh     syn-ack ttl 61
80/tcp   open  http    syn-ack ttl 61
443/tcp  open  https   syn-ack ttl 61
1443/tcp open  ies-lm  syn-ack ttl 61


Host is up (1.0s latency).

└─# nmap -sV -sC -p22,80,1338,1443 10.10.91.206
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 07c0ea0461fe59d6d64c4808c464ee4b (RSA)
|   256 ebd3d5320a6ad886571a067807438f0e (ECDSA)
|_  256 1cb36cbfc5b2fbf513f5518ca8393dd0 (ED25519)
80/tcp   open  http     lighttpd 1.4.55
|_http-title: 403 Forbidden
|_http-server-header: lighttpd/1.4.55
1338/tcp open  ftp      vsftpd 2.0.8 or later
1443/tcp open  ssl/http Apache httpd 2.4.41 ((Ubuntu))
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=dev.probe.thm/organizationName=Tester/stateOrProvinceName=Some-State/countryName=US
| Not valid before: 2023-07-18T10:57:05
|_Not valid after:  2024-07-17T10:57:05
|_http-title: 400 Bad Request
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```