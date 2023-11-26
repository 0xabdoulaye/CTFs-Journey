Bypass authentication and execute commands remotely on Cacti using CVE-2022-46169. TryHackMe

How to Bypass Authentication Checks on This Endpoint

The authentication can be bypassed by manipulating the X-Forwarded-For value to match an entry within the poller table. This will cause the function to return true, authorizing the client.