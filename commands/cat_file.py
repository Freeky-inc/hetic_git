# commands/cat_file.py
"""
Module pour la commande 'cat-file', qui affiche le contenu d'un objet Git.
"""
from services.cat_file_services import cat_file

def run(args):
    """
    Exécute la commande cat-file.
    Usage: fyt cat-file <sha>
    """
    if not args:
        print("Usage: fyt cat-file <sha>")
        return
    
    sha = args[0]
    cat_file(sha)