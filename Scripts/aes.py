from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

# Ciphertext, password, and salt
ciphertext = base64.b64decode("FOqxc90aMQZydCQb2MUm5tj4kRIxxVeCDWzAANfOrr8JItHYneUHhSV0awvQIo/8E1LtfYm/+VVWz0PDK6MXp38BWHoFDorhdS44DzYj9CQ=")
password = "aesiseasy"
salt = "saltval"

# Derive the encryption key using PBKDF2
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,  # 256-bit key for AES-256
    salt=salt.encode(),
    iterations=10000,
    backend=default_backend()
)
key = kdf.derive(password.encode())

# Create a cipher object using AES-256 in ECB mode (assuming no IV is used)
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

# Create a decryptor object
decryptor = cipher.decryptor()

# Perform the decryption
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Create an unpadder for the plaintext
unpadder = padding.PKCS7(128).unpadder()

# Unpad the plaintext
unpadded_plaintext = unpadder.update(plaintext) + unpadder.finalize()

# Print the decrypted plaintext
print("Decrypted plaintext:", unpadded_plaintext.decode())

