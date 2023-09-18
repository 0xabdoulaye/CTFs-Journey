morse_code_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-----': '0', '': ' '
}

def decode_morse_code(morse_code):
    words = morse_code.split('   ')
    decoded_message = ''
    for word in words:
        characters = word.split(' ')
        decoded_word = ''.join([morse_code_dict[char] for char in characters])
        decoded_message += decoded_word + ' '
    return decoded_message.strip()

flash_input = input("Enter the flashlight signals (use . for dot and - for dash): ")
flash_input = flash_input.replace(".", ". ").replace("-", "- ")
decoded_message = decode_morse_code(flash_input)
print(decoded_message)
