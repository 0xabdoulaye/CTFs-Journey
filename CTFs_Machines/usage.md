## Recon


```sh
└─# nmap -sV -Pn -p1-65535 --min-rate 3000 $ip
Not shown: 44797 closed tcp ports (reset), 20736 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


```

le port 80 me retourne sur le `usage.htb`

```sh
# echo "$ip $host" | tee -a /etc/hosts
10.10.11.18 usage.htb


```