# LoveNote - Predictable RSA Key Generation

LoveNote built its reputation on trust. Every message, every action, signed and verified by the system itself. LoveNote claims that no message can be forged, no identity faked. Yet an internal leak suggests the platform may be trusting something it shouldn't.

`Web` `Crypto` `RSA` `Flask` `Deterministic Key Generation`

## Reconnaissance

The application is a Flask-based Valentine's Day messaging platform that uses RSA-2048 digital signatures (PSS + SHA-256) to sign and verify messages.

Available routes discovered:

| Route | Description |
|-------|-------------|
| `/` | Home page with public messages |
| `/register` | User registration |
| `/login` | Authentication |
| `/dashboard` | User dashboard (inbox, sent, public) |
| `/compose` | Compose & sign a message |
| `/messages` | Public message board |
| `/verify` | Verify a message signature |
| `/profile/<user>` | User profile with **public key** |
| `/about` | Tech stack details |
| `/debug` | **Exposed debug logs** |

The session cookie is a simple Flask `itsdangerous` token:

```
session=eyJ1c2VybmFtZSI6ImJsb21hbiJ9.aY_TuA.N_o0bwBh9d1Ginonp3tEnmgRC30
```

```json
{"username":"bloman"}
```

## Identifying the Vulnerability

### 1. Weak RSA Key on Admin Profile

Visiting `/profile/admin` reveals the admin's public key:

```
-----BEGIN PUBLIC KEY-----
MFswDQYJKoZIhvcNAQEBBQADSgAwRwJAAaAWvmsqFsYJ5w1P4MD7NKiuZxsKi2zo
HUjT4uFoKxaN2FV4y+rOMrY07Ab75kNiRoOPxSXMH2diq1jHFa0FKwIDAQAB
-----END PUBLIC KEY-----
```

Extracting the key parameters immediately shows the problem:

```python
from cryptography.hazmat.primitives.serialization import load_pem_public_key

key = load_pem_public_key(pem)
pub = key.public_numbers()
print(f"n = {pub.n}")
print(f"Key size: {pub.n.bit_length()} bits")
```

```
n = 85126331932157837525567854053245460499291064536555820275957255468949993697387108905637573364855242718285589546535798832668842941372737201002956840568107
e = 65537
Key size: 505 bits
```

The platform claims RSA-2048, but the admin key is only **505 bits**.

### 2. Debug Endpoint Leaks Key Generation Algorithm

The `/debug` endpoint exposes the internal key generation process:

```
[2026-02-06 14:23:15] Development mode: ENABLED
[2026-02-06 14:23:15] Using deterministic key generation
[2026-02-06 14:23:15] Seed pattern: {username}_lovenote_2026_valentine

[DEBUG] Seed converted to bytes for cryptographic processing
[DEBUG] Seed hashed using SHA256 to produce large numeric material

[DEBUG] Prime derivation step 1:
[DEBUG] Converting SHA256(seed) into a large integer
[DEBUG] Checking consecutive integers until a valid prime is reached
[DEBUG] Prime p selected

[DEBUG] Prime derivation step 2:
[DEBUG] Modifying seed with PKI-related constant (SHA256(seed + b"pki"))
[DEBUG] Hashing modified seed with SHA256
[DEBUG] Converting hash into a large integer
[DEBUG] Checking consecutive integers until a valid prime is reached
[DEBUG] Prime q selected
```

The key generation is **fully deterministic** based on the username. The algorithm is:

```
seed      = "{username}_lovenote_2026_valentine"
p         = next_prime(int.from_bytes(SHA256(seed)))
q         = next_prime(int.from_bytes(SHA256(seed + b"pki")))
n         = p * q
```

Since SHA-256 produces 256-bit hashes, each prime is ~256 bits, giving a ~512-bit modulus — far from the claimed 2048 bits.

## Exploitation

### Step 1 — Reconstruct the Admin Private Key

With the seed `admin_lovenote_2026_valentine`, we can reproduce the exact same primes the server generated:

```python
import hashlib
from sympy import nextprime, mod_inverse

seed = b"admin_lovenote_2026_valentine"

# Derive p
hash_p = hashlib.sha256(seed).digest()
p = nextprime(int.from_bytes(hash_p, 'big'))

# Derive q
hash_q = hashlib.sha256(seed + b"pki").digest()
q = nextprime(int.from_bytes(hash_q, 'big'))

n = p * q
e = 65537
phi = (p - 1) * (q - 1)
d = int(mod_inverse(e, phi))
```

```
p = 4791618204188744540991837585123847317681060752926508821153931923856376697043
q = 17765675040165337710763422425872010801055738292884264426719252999172010591049
n = 85126331932157837525567854053245460499291064536555820275957255468949993697387108905637573364855242718285589546535798832668842941372737201002956840568107

Match with admin public key: True
```

### Step 2 — Forge a Signature as Admin

Using the reconstructed private key, we sign an arbitrary message with the same scheme the server uses (RSA-PSS + SHA-256):

```python
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers, RSAPublicNumbers

# Build the private key object
dp = d % (p - 1)
dq = d % (q - 1)
iqmp = int(mod_inverse(q, p))

public_numbers = RSAPublicNumbers(e, n)
private_numbers = RSAPrivateNumbers(p, q, d, dp, dq, iqmp, public_numbers)
private_key = private_numbers.private_key()

# Sign
message = b"I am the admin"
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print(signature.hex())
```

### Step 3 — Submit the Forged Signature to /verify

```sh
curl -s -X POST http://10.80.128.113:5000/verify \
  -b 'session=<session_cookie>' \
  -d 'username=admin' \
  --data-urlencode 'message=I am the admin' \
  -d 'signature=<forged_hex_signature>'
```

The server validates the signature against the admin's public key, confirms it's authentic, and reveals the flag:

```
Signature Valid
This message was cryptographically verified and is authentic

You successfully forged an admin signature!
THM{PR3D1CT4BL3_S33D5_BR34K_H34RT5}
```

## Root Cause

The vulnerability is **deterministic key generation from a predictable seed**. The platform derives RSA key pairs using:

```
SHA256("{username}_lovenote_2026_valentine")
```

This has two critical consequences:

1. **Predictable primes** — Anyone who knows the username and the seed pattern can reconstruct the full private key.
2. **Undersized keys** — SHA-256 only produces 256-bit output, so each prime is ~256 bits. The resulting RSA modulus is ~512 bits instead of the claimed 2048 bits.

Cryptographic keys must be generated from a **cryptographically secure random number generator (CSPRNG)**, never from deterministic or guessable seeds.
