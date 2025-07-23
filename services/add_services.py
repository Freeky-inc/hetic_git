import os
from core import Repository

def add(paths):
    """
    Ajoute des fichiers ou répertoires à l'index.
    """
    repo = Repository()
    results = []
    
    for path in paths:
        if not os.path.exists(path):
            print(f"Erreur: Le chemin '{path}' n'existe pas.")
            results.append((path, None))
            continue
        
        if os.path.isdir(path):
            # Traitement récursif pour les répertoires
            for root, dirs, files in os.walk(path):
                # Ignorer les dossiers .git et __pycache__
                if '.git' in root.split(os.sep):
                    continue
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    blob_hash = repo.add_file(file_path)
                    results.append((file_path, blob_hash))
        else:
            # Traitement d'un fichier simple
            blob_hash = repo.add_file(path)
            results.append((path, blob_hash))
    
    return results