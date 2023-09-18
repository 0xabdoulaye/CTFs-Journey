# . and _ into binary
# Définir le nom du fichier d'entrée et de sortie
fichier_entree = "dot_and_dash.txt"
fichier_sortie = "binaire.txt"

# Définir le dictionnaire de correspondance entre le code Morse et le binaire
correspondance = {'.': '0', '_': '1'}

# Ouvrir le fichier d'entrée en mode lecture
with open(fichier_entree, 'r') as f_entree:
    contenu = f_entree.read()

# Remplacer les caractères selon le dictionnaire de correspondance
binaire = ''.join(correspondance.get(c, c) for c in contenu)

# Ouvrir le fichier de sortie en mode écriture
with open(fichier_sortie, 'w') as f_sortie:
    f_sortie.write(binaire)

print("Conversion terminée. Le résultat a été écrit dans", fichier_sortie)
