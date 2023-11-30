## Hacking Tips
Here you will find all hacking Tips i have taked on my notes

- 1: Always run `nmap ` multiples times, don't do it just 1 times.
- 2: If you run `ffuf` or `gobuster` and still found nothing, run `gobuster` ;`subfinder`; or `wfuzz` to find other domains and do directory fuzzing on them. Just like this `└─# gobuster vhost -u http://thetoppers.htb/ -w /usr/share/wordlists/Seclist/Discovery/DNS/subdomains-top1million-20000.txt --append-domain`
- 3: If you are exploiting `DirtyCow` and then the exploit is not compiling correctly. use this `PATH=PATH$:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/gcc/x86_64-linux-gnu/4.8/;export PATH `
- 4: If you're fuzzing on a domain and found like `https://domain/file`, Fuzz also on that file like `https://domain/file/FUZZ`.
