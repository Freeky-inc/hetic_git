# commands/reset.py
"""
Module pour la commande 'reset', qui réinitialise l'état de l'index.
"""
from services.reset_services import reset

def run(args):
    """
    Exécute la commande reset.
    Usage: fyt reset [-soft|-mixed|-hard]
    """
    if not args:
        print("Usage: fyt reset [-soft|-mixed|-hard]")
        return

    mode = 'mixed'  # Mode par défaut
    if '--soft' in args or '-soft' in args:
        mode = 'soft'
    elif '--hard' in args or '-hard' in args:
        mode = 'hard'
    elif '--mixed' in args or '-mixed' in args:
        mode = 'mixed'
    
    # Appeler le service
    reset(mode)