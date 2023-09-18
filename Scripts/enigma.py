class EnigmaM3:
    def __init__(self):
        self.rotors = {
            'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
            'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
            'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
            'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
            'V': 'VZBRGITYUPSDNHLXAWMJQOFECK'
        }
        self.reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def rotate_rotors(self, positions):
        positions[2] = (positions[2] + 1) % 26
        if positions[2] == self.alphabet.index('R') or positions[1] == self.alphabet.index('F'):
            positions[1] = (positions[1] + 1) % 26
            if positions[1] == self.alphabet.index('E'):
                positions[0] = (positions[0] + 1) % 26

    def encrypt_letter(self, letter, positions):
        letter = letter.upper()
        if letter not in self.alphabet:
            return letter

        positions[0] = (positions[0] + 1) % 26
        if positions[0] == self.alphabet.index('Q'):
            positions[1] = (positions[1] + 1) % 26

        encrypted_letter = letter
        for rotor in reversed(self.rotors.keys()):
            index = (self.alphabet.index(encrypted_letter) + positions[2] - positions[0]) % 26
            encrypted_letter = self.alphabet[(self.alphabet.index(self.rotors[rotor][index]) - positions[2] + positions[0]) % 26]

        index = (self.alphabet.index(encrypted_letter) - positions[2] + positions[0]) % 26
        encrypted_letter = self.alphabet[(self.alphabet.index(self.reflector[index]) + positions[2] - positions[0]) % 26]

        for rotor in self.rotors.keys():
            index = (self.alphabet.index(encrypted_letter) + positions[2] - positions[0]) % 26
            encrypted_letter = self.alphabet[(self.alphabet.index(self.alphabet[(self.alphabet.index(self.rotors[rotor][index]) - positions[2] + positions[0]) % 26]) - positions[2] + positions[0]) % 26]

        return encrypted_letter

    def decrypt_message(self, message, rotor_positions):
        decrypted_message = ''
        for letter in message:
            decrypted_message += self.encrypt_letter(letter, rotor_positions)
            self.rotate_rotors(rotor_positions)
        return decrypted_message

def main():
    enigma = EnigmaM3()
    rotor_positions = [0, 0, 0]  # Rotor positions: [Rotor 1, Rotor 2, Rotor 3]
    encrypted_message = "vyzur vmcla wlgfs z Paramètres"
    decrypted_message = enigma.decrypt_message(encrypted_message, rotor_positions)
    print("Decrypted message:", decrypted_message)

if __name__ == '__main__':
    main()
