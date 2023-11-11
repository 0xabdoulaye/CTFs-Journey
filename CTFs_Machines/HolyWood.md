## Recon

```
└─# nmap -sS -vvv -Pn --min-rate 2000 $ip
Host is up, received user-set (0.50s latency).
Scanned at 2023-11-11 11:04:16 GMT for 8s
Not shown: 976 closed tcp ports (reset)
PORT      STATE SERVICE      REASON
21/tcp    open  ftp          syn-ack ttl 127
25/tcp    open  smtp         syn-ack ttl 127
79/tcp    open  finger       syn-ack ttl 127
80/tcp    open  http         syn-ack ttl 127
106/tcp   open  pop3pw       syn-ack ttl 127
110/tcp   open  pop3         syn-ack ttl 127
135/tcp   open  msrpc        syn-ack ttl 127
139/tcp   open  netbios-ssn  syn-ack ttl 127
143/tcp   open  imap         syn-ack ttl 127
443/tcp   open  https        syn-ack ttl 127
445/tcp   open  microsoft-ds syn-ack ttl 127
554/tcp   open  rtsp         syn-ack ttl 127
2869/tcp  open  icslap       syn-ack ttl 127
3306/tcp  open  mysql        syn-ack ttl 127
8009/tcp  open  ajp13        syn-ack ttl 127
8080/tcp  open  http-proxy   syn-ack ttl 127
8089/tcp  open  unknown      syn-ack ttl 127
10243/tcp open  unknown      syn-ack ttl 127
49152/tcp open  unknown      syn-ack ttl 127
49153/tcp open  unknown      syn-ack ttl 127
49154/tcp open  unknown      syn-ack ttl 127
49155/tcp open  unknown      syn-ack ttl 127
49156/tcp open  unknown      syn-ack ttl 127
49157/tcp open  unknown      syn-ack ttl 127
```
`flag30=eb1b768800000e1d2fe1c3100005d2dc8dd10000`
```
└─# nmap -sC -sV -p21,80,25,79,106,110,135,139,143,445,554,2869,3306,8009,8080,8089,10243,49152,49153-49157 $ip
NSE Timing: About 99.46% done; ETC: 11:23 (0:00:02 remaining)
Nmap scan report for 10.150.150.219
Host is up (0.67s latency).

PORT      STATE SERVICE      VERSION
21/tcp    open  ftp          FileZilla ftpd 0.9.41 beta
| ftp-syst: 
|_  SYST: UNIX emulated by FileZilla
25/tcp    open  smtp         Mercury/32 smtpd (Mail server account Maiser)
|_smtp-commands: localhost Hello nmap.scanme.org; ESMTPs are:, TIME
79/tcp    open  finger       Mercury/32 fingerd
| finger: Login: Admin         Name: Mail System Administrator\x0D
| \x0D
|_[No profile information]\x0D
80/tcp    open  http         Apache httpd 2.4.34 ((Win32) OpenSSL/1.0.2o PHP/5.6.38)
| http-title: Welcome to XAMPP
|_Requested resource was http://10.150.150.219/dashboard/
106/tcp   open  pop3pw       Mercury/32 poppass service
110/tcp   open  pop3         Mercury/32 pop3d
|_pop3-capabilities: USER TOP APOP UIDL EXPIRE(NEVER)
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
143/tcp   open  imap         Mercury/32 imapd 4.62
|_imap-capabilities: AUTH=PLAIN IMAP4rev1 OK X-MERCURY-1A0001 complete CAPABILITY
445/tcp   open  microsoft-ds Windows 7 Ultimate 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
554/tcp   open  rtsp?
2869/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
3306/tcp  open  mysql        MariaDB (unauthorized)
8009/tcp  open  ajp13        Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
8080/tcp  open  http         Apache Tomcat/Coyote JSP engine 1.1
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/7.0.56
8089/tcp  open  ssl/http     Splunkd httpd
| http-robots.txt: 1 disallowed entry 
|_/
| ssl-cert: Subject: commonName=SplunkServerDefaultCert/organizationName=SplunkUser
| Not valid before: 2019-10-28T09:17:32
|_Not valid after:  2022-10-27T09:17:32
|_http-title: splunkd
10243/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
Service Info: Hosts: localhost, HOLLYWOOD; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-os-discovery: 
|   OS: Windows 7 Ultimate 7601 Service Pack 1 (Windows 7 Ultimate 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1
|   NetBIOS computer name: HOLLYWOOD\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2023-11-11T19:49:32+08:00
| smb2-security-mode: 
|   210: 
|_    Message signing enabled but not required
|_clock-skew: mean: -2h06m23s, deviation: 4h37m07s, median: 33m36s
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2023-11-11T11:49:42
|_  start_date: 2020-04-02T14:13:04
```
Exploit the activeMQ on port 8161
```
meterpreter > sysinfo 
Computer        : Hollywood
OS              : Windows 7 6.1 (x86)
Architecture    : x86
System Language : en_US
Meterpreter     : java/windows
meterpreter > 



 Directory of C:\Users\User\Documents

03/22/2019  04:12 PM    <DIR>          .
03/22/2019  04:12 PM    <DIR>          ..
03/22/2019  04:12 PM                43 FLAG9.txt
               1 File(s)             43 bytes
               2 Dir(s)  44,543,647,744 bytes free

C:\Users\User\Documents>type FLAG9.txt
type FLAG9.txt
b017cd11a8def6b4bae78b0a96a698deda09f033 

C:\Users\User\Documents>
```