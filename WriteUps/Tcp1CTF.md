## Misc
**ZipZIPzip**
```
for ((i = 25000 ; i >= 1 ; i--))
do
  pass=cat password.txt
  rm password.txt
  unzip -P $pass zip-${i}.zip
  rm zip-${i}.zip
done
```
La notation i-- est une opération de décrémentation dans la programmation. Dans le contexte de la ligne for ((i = 25000; i >= 1; i--)), cela signifie que la variable i est réduite d'une unité à chaque itération de la boucle.

## Forensic
**Hide and Split**