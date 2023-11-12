# Description 
Welcome to my personal Capture The Flags (CTFs) repository! This repository is created to track my progress, achievements, and detailed notes regarding cybersecurity challenges, especially on popular platforms like TryHackMe, Hack The Box and Rootme.

## Contents


This repository contains an organized list of CTF Machines that I have successfully exploited. Each entry includes vital information such as difficulty level, key concepts, platforms used, and the status of each machine. Additionally, each box is accompanied by a link to a detailed write-up I've created. These write-ups provide a step-by-step analysis of the exploitation process, tools used, mistakes made, and lessons learned.

Stay Connected:

- **Blog:** Discover in-depth articles and resources for beginners on my blog, [blackcybersec.xyz](https://blackcybersec.xyz), where I share my journey and insights into the realm of cybersecurity.

- **Twitter:** Join the conversation on [@bloman19](https://twitter.com/bloman19) for cybersecurity discussions, tips, and real-time updates on my learning journey.

- **Learning Together:** I'm a strong believer in collaborative learning. Feel free to contribute your thoughts, insights, and alternative approaches to the write-ups. Together, we can expand our knowledge and skills in the ever-evolving field of cybersecurity.

Let's continue learning, adapting, and refining our skills together in the fascinating world of cybersecurity.
Happy hacking!.

## Linux Machines
| Machines | Difficulty |                                                Tags                  | Platform                            | Status | 
|:-------------:|:----------:|:--------------------------------------------------------------------------------------------------:|:---------:|:---------:|
|               |            |                                                                                                    |           |                               | 
| [VulnVersity](./CTFs_Machines/VulnVersity.md)        |    Easy    |                 ssh, DirEnum, Systemctl(PrivEsc)                                                            | Tryhackme |    Completed     |
| [EasyCTF](./CTFs_Machines/easyctf.md)        |    Easy    |                DirEnum, CMS Made Simple, ssh                                                           | Tryhackme |    Completed     |
|  PC       |    Easy    |                   grpcui, go, 50051                                                          | HacktheBox |    Completed     |
| Metasploitable 2         |    Easy    |    FTP, SSH, MySQL, revshells                                                                    | Rootme    |    In Progress     |
|Kenobi         |    Easy    |  SMB, enum4linux, NFS, SSH                                                                       | Tryhackme  |    Completed     |
|[Lian Yu](./CTFs_Machines/LianYu.md)         |    Easy    |     DirEnum, Steg, FTP, polkit(pkexec)                                                                    | Tryhackme  |    Completed     |
| Basic Pentesting 1        |    Easy    |                 Cracking, DirEnum,                                                            | Tryhackme |    Completed     |
| Agent Sudo        |    Easy    |                 ssh, DirEnum, cracking                                                            | Tryhackme |    Completed     |
| [Brooklyn Nine Nine](./CTFs_Machines/brooklyn.md)        |    Easy    |           Steg, FTP, nano(PrivEsc)                                                                 | Tryhackme |    Completed     |
| BullDog        |    Easy    |           DirEnum, Cracking, RCE(id_rsa.pub), Cronjob(PrivEsc)                                                                 | RootMe |    Completed     |
| [Sau](./CTFs_Machines/sau.md)        |    Easy    |           SSRF, CVE-2023-27163, Systemctl(PrivEsc)                                                               | HacktheBox |    Completed     |
| [KeeperHTB](./CTFs_Machines/keeperHTB.md)        |    Easy    |           CVE-2023-32784, keePass, id_rsa(PrivEsc)                                                               | HacktheBox |    Completed     |
| [Blog](./CTFs_Machines/blog.md)        |    Medium    |           Wordpress, CVE-2019-8943, Pkexec(PrivEsc), /usr/sbin/checker                                                              | TryHackMe |    Completed     |
| [StuntMan](https://blackcybersec.xyz/posts/stuntman-mike-on-pwntilldawn/)        |    Easy    |           Ssh, Hydra, Sudo(PrivEsc)                                                              | PwntillDawn |    Completed     |
| [Vega](./CTFs_Machines/vega.md)        |    Medium    |           Ssh, Guessing, Sudo(PrivEsc)                                                              | PwntillDawn |    Completed     |
| [Topology](./CTFs_Machines/Topology.md)        |    Easy    |           Latex Injection, Crack Passwd, Gnuplot(PrivEsc)                                                              | HacktheBox |   Completed    |
| [HiJack](./CTFs_Machines/)        |    Easy    |                                                                         | TryHackMe |   Comming Soon...    |
| [Analytics](./CTFs_Machines/Analytics.md)        |    Easy    |CVE-2023-38646, CVE-2021-3493, OverlayFS(PrivEsc)                                                                         | HacktheBox |   Completed   |
| [Canyon](./CTFs_Machines/Canyon.md)        |    Easy    |SMTP, RCE, sudo(PrivEsc)                                                                         | PwntillDawn |   Completed   |
| [Oopsie](./CTFs_Machines/oopsie.md)        |    Easy    |IDOR, RCE, pkexec,bugtracker,PATH(PrivEsc)                                                                         | HacktheBox |   Completed   |
| [Apache](./CTFs_Machines/apache.md)        |    Easy    |CVE-2021-41773, apache 2.4.49, cpio(PrivEsc)                                                                         | EchoCTF |   Completed   |
| [Grafana](./CTFs_Machines/grafana.md)        |    Advanced    |LFI, default Creds, ansible-playbook(PrivEsc)                                                                         | EchoCTF |   Completed   |
| [DC-1](./CTFs_Machines/Dc1.md)        |    Easy    |Drupal, SQLi, find(PrivEsc)                                                                         | Proving Grounds |   Completed   |
| [Dasherr](./CTFs_Machines/Dasherr.md)        |    Medium    |Instance, Burp, gcc(PrivEsc)                                                                         | EchoCTF |   Completed   |
| [DogCat](./CTFs_Machines/dogcat.md)        |    Medium    |LFI2RCE, Escape Container, env(PrivEsc)                                                                         | TryHackMe |   Completed   |





## Windows Machines
| Machines | Difficulty |                                                Tags                  | Platform                            | Status | 
|:-------------:|:----------:|:--------------------------------------------------------------------------------------------------:|:---------:|:---------:|
|               |            |                                                                                                    |           |                               |
| [Dancing](https://blackcybersec.xyz/posts/Dancing-HacktheBox/)        |    Easy    |           SMB, Anonymous, Share                                                               | HacktheBox |    Completed     |
| [Mr Blue](https://blackcybersec.xyz/posts/Windows-hacking/)        |    Easy    |           EternalBlue, MS17-010, CVE-2017-0144                                                               | PwntillDawn |    Completed     |
| [Blue](./CTFs_Machines/blue.md)        |    Easy    |           EternalBlue, MS17-010, CVE-2017-0144                                                               | HacktheBox |    Completed     |
| [Responder](./CTFs_Machines/responder.md)        |    Easy    |           NTLM, LFI,RFI                                                               | HacktheBox |    Completed     |