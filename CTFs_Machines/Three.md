HacktheBox
tags : web, cloud, aws, Bucket enumeration
`
nmap -sV -Pn -p- --min-rate 5000
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
`
└─# gobuster vhost -u http://thetoppers.htb/ -w /usr/share/wordlists/Seclist/Discovery/DNS/subdomains-top1million-20000.txt --append-domain

Found: s3.thetoppers.htb Status: 404 [Size: 21]
`└─# aws
Command 'aws' not found, but can be installed with:
apt install awscli
Do you want to install it? (N/y)y
apt install awscli
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done`


 aws --endpoint=http://s3.thetoppers.htb/ s3 ls s3://thetoppers.htb
 shell and got flag
 a980d99281a28d638ac68b9bf9453c2b