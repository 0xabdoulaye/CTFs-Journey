import sys

# Lire les deux fichiers en tant que tableaux d'octets (byte arrays)
file1_b = bytearray(open(sys.argv[1], 'rb').read())
file2_b = bytearray(open(sys.argv[2], 'rb').read())

# Déterminer la taille à utiliser, qui correspondra à la taille du fichier le plus petit
size = len(file1_b) if len(file1_b) < len(file2_b) else len(file2_b)

# Créer un tableau d'octets pour stocker le résultat du XOR
xord_byte_array = bytearray(size)

# Effectuer une opération XOR entre les fichiers
for i in range(size):
    xord_byte_array[i] = file1_b[i] ^ file2_b[i]

# Écrire les octets résultants dans le fichier de sortie
open(sys.argv[3], 'wb').write(xord_byte_array)

print("Opération XOR terminée. Résultat enregistré dans", sys.argv[3])
