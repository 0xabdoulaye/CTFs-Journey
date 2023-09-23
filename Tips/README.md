## Hacking Tips
Here you will find all hacking Tips i have taked on my notes

- 1: Always run `nmap ` multiples times, don't do it just 1 times.
- 2: If you run `ffuf` or `gobuster` and still found nothing, run `gobuster` ;`subfinder`; or `wfuzz` to find other domains and do directory fuzzing on them. Just like this `└─# gobuster vhost -u http://thetoppers.htb/ -w /usr/share/wordlists/Seclist/Discovery/DNS/subdomains-top1million-20000.txt --append-domain`
- 3: