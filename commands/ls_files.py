# commands/ls_files.py
"""
Module pour la commande 'ls-files', qui liste les fichiers dans l'index.
"""
from services.ls_files_services import ls_files

def run(args):
    """
    Exécute la commande ls-files.
    Usage: fyt ls-files [--staged]
    """
    staged_only = '--staged' in args
    
    ls_files(staged_only)