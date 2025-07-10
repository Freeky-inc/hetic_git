# **Comment lancer le script**
---
## Cas de script Bash
**Rendre le fichier script exécutable**
```bash
chmod +x my_hash_object.sh  #Rend le script exécutable
```

**Lancer le fichier avec un argument**
```bash
./my_hash_object.sh mon_fichier.txt
```

## Cas de script Python (notre cas)

```bash
python3 --version  # Vérifie que Python 3 est installé

python3 git_hash_object.py mon_fichier.txt
```
---
**ou alors**
## Pour le script Bash
Place-le dans un dossier de ton PATH (par exemple ~/bin/).

Ou utilise un alias dans ton ```.bashrc :```

```bash
alias git-hash-object="$HOME/path/to/my_hash_object.sh"
```
### Pour le script Python
Rends-le exécutable :

```bash
chmod +x git_hash_object.py
```
Ajoute un shebang (première ligne du script) :

```python
#!/usr/bin/env python3
```
Déplace-le dans un dossier du PATH ou utilise un alias :

```bash
alias git-hash-object="python3 $HOME/path/to/git_hash_object.py"
```
### Vérification avec Git
Compare le résultat avec la commande réelle de Git :

```bash
git hash-object test.txt
```

[extrait de deepseek](https://chat.deepseek.com/a/chat/s/00c34d42-1c8e-4fcf-8f1a-a551c10f2804)
Ces étapes peuvent varier entre les utilisateurs de windows et de MacOS