file = open("blank.txt", "r").read()
resulat = ""
for ch in file:
	if ord(ch) == 32:
		resulat += "0"
	else:
		resulat += "1"

print(resulat)
