# commands/ls_tree.py
"""
Module pour la commande 'ls-tree', qui liste le contenu d'un tree.
"""
from services.ls_tree_services import ls_tree

def run(args):
    """
    Exécute la commande ls-tree.
    Usage: fyt ls-tree <tree-hash> [-r]
    """
    if not args:
        print("Usage: fyt ls-tree <tree-hash> [-r]")
        return
    
    tree_hash = args[0]
    recursive = '-r' in args or '--recursive' in args
    
    ls_tree(tree_hash, recursive)