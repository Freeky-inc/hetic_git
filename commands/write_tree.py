# commands/write_tree.py
"""
Module pour la commande 'write-tree', qui crée un tree à partir de l'index.
"""
from services.write_tree_services import write_tree

def run(args):
    """
    Exécute la commande write-tree.
    Usage: fyt write-tree
    """
    write_tree() 