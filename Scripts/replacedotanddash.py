def morse_to_binary(morse_code):
    binary_code = morse_code.replace('.', '0').replace('-', '1')
    return binary_code

def main():
    input_file_path = "motivation.txt"
    output_file_path = "output_file.txt"

    with open(input_file_path, 'r') as input_file:
        morse_content = input_file.read()

    binary_content = morse_to_binary(morse_content)

    with open(output_file_path, 'w') as output_file:
        output_file.write(binary_content)

    print("Conversion complete. Binary data saved to", output_file_path)

if __name__ == "__main__":
    main()
