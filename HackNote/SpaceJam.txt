target: 10.10.182.91
fastscan :└─# nmap -f -sC -sV -T5 -oN fastscan -v 10.10.182.91
http://10.10.182.91:3000/
i added http://10.10.182.91:3000/?cmd=id
PORT      STATE    SERVICE        VERSION
13/tcp    filtered daytime
22/tcp    open     ssh            OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 1df0d5f2671e5599dec62685b386ea81 (RSA)
|   256 4f5f6298aab1dda28161169ba529cdbd (ECDSA)
|_  256 9b12b0f31ffbb7d8a89c6be6bdf44055 (ED25519)
23/tcp    open     telnet         Linux telnetd
80/tcp    open     http           Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Michael Jordan
212/tcp   filtered anet
544/tcp   filtered kshell
683/tcp   filtered corba-iiop
765/tcp   filtered webster
1034/tcp  filtered zincite-a
1065/tcp  filtered syscomlan
1183/tcp  filtered llsurfup-http
1233/tcp  filtered univ-appserver
1300/tcp  filtered h323hostcallsc
1521/tcp  filtered oracle
1719/tcp  filtered h323gatestat
1840/tcp  filtered netopia-vo2
1863/tcp  filtered msnp
1947/tcp  filtered sentinelsrm
2049/tcp  filtered nfs
2196/tcp  filtered unknown
2920/tcp  filtered roboeda
3000/tcp  open     http           Node.js (Express middleware)
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
3370/tcp  filtered satvid-datalnk
3517/tcp  filtered 802-11-iapp
3800/tcp  filtered pwgpsi
4001/tcp  filtered newoak
4002/tcp  filtered mlchat-proxy
5050/tcp  filtered mmcc
7777/tcp  filtered cbt
9999/tcp  open     http           Golang net/http server
| fingerprint-strings: 

218f5ea7a4d711eef60171e5c92ba9e1
79973eb57d0188ffc6c85a1a4e57a516
79973eb57d0188ffc6c85a1a4e57a516

