# When Hearts Collide - MD5 Hash Collision

Matchmaker is a playful, hash-powered experience that pairs you with your ideal dog by comparing MD5 fingerprints. Upload a photo, let the hash chemistry do its thing, and watch the site reveal whether your vibe already matches one of our curated pups.

`Web` `Crypto` `MD5 Collision` `200pts` `Medium`

## Reconnaissance

The application is a Flask-based dog-matching platform served behind Nginx. You upload a JPEG photo and the server computes its MD5 hash, then compares it against every other upload in the database. If two different files share the same MD5, the system declares a "match".

Available routes discovered:

| Route | Description |
|-------|-------------|
| `/` | Home page with upload form |
| `/upload` | POST endpoint for file upload |
| `/upload_success/<uuid>` | Result page after upload |
| `/view/<uuid>` | View a stored profile photo |
| `/static/uploads/<uuid>.jpg` | Direct access to uploaded images |

The home page explicitly describes the matching algorithm:

> Matchmaker keeps up with the universe by comparing your photo's MD5 hash to every doggo snapshot that wanders through the site. If your hash is identical to a pup's, that's our cue.

### Upload Behavior

Three distinct responses were observed:

| Response | Condition |
|----------|-----------|
| **Photo not eligible** | Invalid or empty file |
| **Your photo already lives here** | Exact same file (byte-for-byte duplicate) already exists |
| **Match in progress** (`data-match="false"`) | Valid upload, no MD5 collision found |
| **Match in progress** (`data-match="true"`) | Valid upload, MD5 matches another file — flag revealed |

The "already uploaded" response confirms the server rejects exact duplicates. We need two **different** files that produce the **same** MD5 hash — a classic MD5 collision.

## Exploitation

### Step 1 — Build fastcoll

[fastcoll](https://github.com/cr-marcstevens/hashclash) by Marc Stevens generates identical-prefix MD5 collisions in seconds. The full HashClash project requires Boost and autotools, but the `md5fastcoll` component can be compiled standalone:

```sh
git clone https://github.com/cr-marcstevens/hashclash.git
cd hashclash/src/md5fastcoll
```

A minimal `main.cpp` replacement removes the Boost/hashclash dependencies (program_options, filesystem, timer) and implements basic CLI argument parsing directly. The core collision logic (`block0.cpp`, `block1.cpp`, `md5.cpp`, etc.) compiles without modification:

```sh
g++ -O2 -o fastcoll main.cpp md5.cpp block0.cpp block1.cpp \
    block1wang.cpp block1stevens00.cpp block1stevens01.cpp \
    block1stevens10.cpp block1stevens11.cpp
```

### Step 2 — Create a JPEG Prefix

fastcoll works with an identical-prefix attack: given a common prefix (aligned to 64 bytes — the MD5 block size), it appends two different 128-byte collision blocks that produce the same MD5 hash.

We craft a minimal valid JPEG prefix padded to exactly 64 bytes using a JPEG comment marker (`0xFFFE`):

```python
import struct

data = b'\xff\xd8'                          # SOI
data += b'\xff\xe0\x00\x10'                 # APP0 marker, length 16
data += b'JFIF\x00\x01\x01\x00'            # JFIF header
data += b'\x00\x01\x00\x01\x00\x00'        # density + thumbnail

# Pad to 64 bytes with a JPEG comment
padding_needed = 64 - len(data) - 4         # 4 = comment marker + length field
data += b'\xff\xfe'                         # COM marker
data += struct.pack('>H', padding_needed + 2)
data += b'A' * padding_needed

with open('prefix.jpg', 'wb') as f:
    f.write(data)  # exactly 64 bytes
```

### Step 3 — Generate the Collision Pair

```sh
./fastcoll -p prefix.jpg -o col1.jpg col2.jpg
```

```
Generating first block: ........
Generating second block: S11.............
Done!
```

Verification:

```sh
$ md5sum col1.jpg col2.jpg
7b8198047cee7064dd0de998eb7e1f42  col1.jpg
7b8198047cee7064dd0de998eb7e1f42  col2.jpg

$ diff col1.jpg col2.jpg > /dev/null && echo SAME || echo DIFFERENT
DIFFERENT

$ file col1.jpg
col1.jpg: JPEG image data, JFIF standard 1.01
```

Two distinct 192-byte JPEG files with identical MD5 hashes.

### Step 4 — Upload Both Files

Upload the first file — it gets stored in the database with no match:

```sh
curl -s -X POST -F "file=@col1.jpg;filename=photo1.jpg" \
  http://10.80.155.174/upload
# → data-match="false" — no collision partner yet
```

Upload the second file — same MD5, different bytes — triggers the match:

```sh
curl -s -X POST -F "file=@col2.jpg;filename=photo2.jpg" \
  http://10.80.155.174/upload
# → data-match="true"
```

The server finds that `col2.jpg` has the same MD5 as the previously uploaded `col1.jpg` but is not a byte-for-byte duplicate, and reveals the flag:

```
THM{hash_puppies_4_all}
```

## Root Cause

The application uses MD5 to fingerprint uploads and treats a hash match between two different files as a legitimate "pairing". MD5 has been cryptographically broken since 2004 (Wang et al.), and tools like fastcoll can produce collisions in under a second on modern hardware.

The duplicate check (rejecting identical files) is insufficient — it only compares file contents, not the scenario where two structurally different files share the same MD5. Using a collision-resistant hash function (SHA-256, SHA-3) would prevent this attack entirely.
