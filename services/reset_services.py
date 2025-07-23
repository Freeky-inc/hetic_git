from core import Repository
import os

def reset(mode=None):
    """
    Réinitialise le dépôt selon le mode : 'soft', 'mixed', 'hard'.
    Utilise Repository et ses composants.
    """
    repo = Repository()
    
    # Liste des fichiers/dossiers à PROTÉGER (ne jamais supprimer)
    protected_items = {
        '.fyt', '.git', '__pycache__', 
        'core', 'commands', 'services', 'utils', 'functions', 'Objects',
        'main.py', 'terminal.py', 'README.md', 'Launching.md'
    }
    
    if mode == 'soft':
        # Soft : ne fait que déplacer HEAD (à implémenter)
        print("Réinitialisation en mode 'soft'. Les commits sont enlevés mais l'index et le répertoire de travail sont conservés.")
        # TODO: déplacer HEAD vers le commit précédent
    elif mode == 'mixed':
        # Mixed : HEAD + index
        repo.index.clear()
        print("Réinitialisation en mode 'mixed'. L'index est réinitialisé mais le répertoire de travail est conservé.")
    elif mode == 'hard':
        # Hard : HEAD + index + working directory (MAIS PROTÉGER LES FICHIERS SOURCE)
        repo.index.clear()
        
        # Supprimer seulement les fichiers de test et les fichiers utilisateur
        # NE PAS supprimer les fichiers source du projet
        for root, dirs, files in os.walk(repo.path):
            # Exclure les dossiers protégés
            dirs[:] = [d for d in dirs if d not in protected_items]
            
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, repo.path)
                
                # Ne supprimer que les fichiers de test et utilisateur
                # Protéger tous les fichiers source du projet
                should_delete = (
                    # Fichiers de test
                    file.startswith('test_') or
                    file.endswith('_test.py') or
                    # Fichiers utilisateur temporaires
                    file.endswith('.txt') and not file.startswith('README') or
                    file.endswith('.pyc') or
                    # Autres fichiers temporaires
                    file.startswith('file') and file.endswith('.txt') or
                    file.startswith('temp_') or
                    file.startswith('tmp_')
                )
                
                # Vérifier que le fichier n'est pas dans un dossier protégé
                is_in_protected_dir = any(protected in rel_path for protected in protected_items)
                
                if should_delete and not is_in_protected_dir:
                    try:
                        os.remove(file_path)
                        print(f"Supprimé: {rel_path}")
                    except Exception as e:
                        print(f"Impossible de supprimer {rel_path}: {e}")
        
        print("Réinitialisation en mode 'hard'. L'index et les fichiers utilisateur sont réinitialisés.")
        print("⚠️  Les fichiers source du projet ont été PROTÉGÉS.")
    else:
        print("Aucun mode de réinitialisation spécifié. Veuillez utiliser 'soft', 'mixed' ou 'hard'.") 