def caesar_decrypt(ciphertext, shift):
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext

ciphertext = input("what's your cipher: ")

for shift in range(26):
    plaintext = caesar_decrypt(ciphertext, shift)
    print(f"Shift: {shift:2d} | Plaintext: {plaintext}")
