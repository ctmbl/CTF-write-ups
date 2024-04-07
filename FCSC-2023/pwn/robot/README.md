## robot
**Points**: 310  
**Difficulty**: 2 stars  
**Category**: pwn  
***Type**: Use After Free (UAF)*

La startup FunWithRobots & Co. souhaite proposer un service interactif, qui tourne sur un serveur distant et qui simule un robot avec beaucoup de réalisme. Mais la veille de l'inauguration, le chef de projet se souvient d'une vague mention concernant des exigences de sécurité...

Comme vous êtes la personne chargée de la sécurité, il a besoin de votre validation. Selon lui, cela n'est qu'une simple formalité car le code a été relu par leurs meilleurs développeurs et le binaire s'exécute avec toutes les protections classiques (canaris, W^X, ASLR, etc.).

Vérifiez s'il est possible de lire le fichier flag.txt qui se trouve sur le serveur distant.

`nc challenges.france-cybersecurity-challenge.fr 2101`

`SHA256(robot) = ef107c2b77ac5c1c4759ae4d4e4c822e8c875d16099d249f420b9401c8643abf`  
`SHA256(robot.c) = c863f1dd19edca20fc5da3f07c75db79681c2ab3778facab525bf582c0c173cf`

[robot](./robot)  
[robot.c](./robot.c)  

## More
[write-up (EN)](./robot_WU.md)  
[exploit](./exploit.py)  
[pwn_utils](./pwn_utils.py)
