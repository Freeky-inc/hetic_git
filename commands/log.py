# commands/log.py
"""
Module pour la commande 'log', qui affiche l'historique des commits.
"""
from services.log_services import log

def run(args):
    """
    Exécute la commande log.
    Usage: fyt log
    """
    log() 