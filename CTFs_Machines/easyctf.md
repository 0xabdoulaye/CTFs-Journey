target : 10.10.78.42
recon : nmap
└─# nmap -sV -p- --open --min-rate 10000 10.10.78.42 

wesite runig on the ip
port 80 apache
Not shown: 65532 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE    VERSION
21/tcp   open  tcpwrapped
80/tcp   open  tcpwrapped
2222/tcp open  tcpwrapped

not shown version then i do this 
└─# nmap -sV -p21,80,2222 -vv --min-rate 10000 10.10.78.42
PORT     STATE SERVICE REASON         VERSION
21/tcp   open  ftp     syn-ack ttl 63 vsftpd 3.0.3
80/tcp   open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))
2222/tcp open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

found website here : http://10.10.188.90/simple/
This site is powered by CMS Made Simple version 2.2.8 
GOOGLE it cms made simple version 2.2.8 exploit and found it
found this https://www.exploit-db.com/exploits/46635

GENERATED WORDS: 4614                                                          

---- Scanning URL: http://10.10.78.42/ ----
+ http://10.10.78.42/index.html (CODE:200|SIZE:11321)                                                    
+ http://10.10.78.42/robots.txt (CODE:200|SIZE:929)                                                      
+ http://10.10.78.42/server-status (CODE:403|SIZE:299)                                                   
==> DIRECTORY: http://10.10.78.42/simple/                                                                
                                                                                                         
---- Entering directory: http://10.10.78.42/simple/ ----
==> DIRECTORY: http://10.10.78.42/simple/admin/                                                          
==> DIRECTORY: http://10.10.78.42/simple/assets/                                                         
==> DIRECTORY: http://10.10.78.42/simple/doc/                                                            
+ http://10.10.78.42/simple/index.php (CODE:200|SIZE:19833)                                              
==> DIRECTORY: http://10.10.78.42/simple/lib/                                                            
==> DIRECTORY: http://10.10.78.42/simple/modules/                                                        
==> DIRECTORY: http://10.10.78.42/simple/tmp/                                                            
==> DIRECTORY: http://10.10.78.42/simple/uploads/                                                        
                                                                                                         
---- Entering directory: http://10.10.78.42/simple/admin/ ----
+ http://10.10.78.42/simple/admin/index.php (CODE:302|SIZE:0)                                            
==> DIRECTORY: http://10.10.78.42/simple/admin/lang/ 

posted by 
Posted by: mitch 
Category: General
