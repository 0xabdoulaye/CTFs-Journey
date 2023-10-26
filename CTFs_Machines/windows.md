Windows PwntillDawn
```
└─# nmap -Pn -p- --open --min-rate 5000  10.150.150.219 
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE
21/tcp    open  ftp
25/tcp    open  smtp
79/tcp    open  finger
80/tcp    open  http
105/tcp   open  csnet-ns
106/tcp   open  pop3pw
110/tcp   open  pop3
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
143/tcp   open  imap
443/tcp   open  https
445/tcp   open  microsoft-ds
554/tcp   open  rtsp
1883/tcp  open  mqtt
2224/tcp  open  efi-mg
2869/tcp  open  icslap
3306/tcp  open  mysql
5672/tcp  open  amqp
8009/tcp  open  ajp13
8080/tcp  open  http-proxy
8089/tcp  open  unknown
8161/tcp  open  patrol-snmp
10243/tcp open  unknown
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49157/tcp open  unknown
49251/tcp open  unknown
61613/tcp open  unknown
61614/tcp open  unknown
61616/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 69.76 seconds
```
I will visit port 80, also the port 8080, or i will use `-sV` then visit all web port