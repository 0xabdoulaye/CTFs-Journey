num_files = 10  # Nombre de fichiers de sortie souhaité
lines_per_file = 100188  # Nombre de lignes approximatif par fichier

with open('bigdata.txt', 'r') as input_file:
    for file_index in range(1, num_files + 1):
        with open(f'attack{file_index}.txt', 'w') as output_file:
            for line_index, line in enumerate(input_file):
                output_file.write(line)
                if line_index >= lines_per_file - 1:
                    break
