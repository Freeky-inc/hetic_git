import os
from core import Repository

def status():
    """
    Affiche le statut du dépôt Git.
    """
    repo = Repository()
    
    # Récupérer les fichiers staged
    staged_files = repo.index.get_all_files()
    
    # Récupérer les fichiers modifiés (dans le working directory mais pas dans l'index)
    modified_files = []
    untracked_files = []
    
    # Parcourir le répertoire de travail
    for root, dirs, files in os.walk(repo.path):
        # Ignorer les dossiers .fyt et __pycache__
        if '.fyt' in root.split(os.sep):
            continue
        dirs[:] = [d for d in dirs if d not in ['.fyt', '__pycache__']]
        
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo.path)
            
            # Vérifier si le fichier est dans l'index
            index_entry = repo.index.get_entry(rel_path)
            
            if index_entry:
                # Fichier dans l'index - vérifier s'il a été modifié
                if os.path.exists(file_path):
                    # Calculer le hash du fichier actuel
                    blob = repo.blob_manager.create_blob(file_path)
                    if blob != index_entry.sha:
                        modified_files.append(rel_path)
            else:
                # Fichier non tracké
                untracked_files.append(rel_path)
    
    # Afficher le statut
    print("Statut du dépôt:")
    print()
    
    if staged_files:
        print("Fichiers staged pour commit:")
        for file in staged_files:
            print(f"  {file}")
        print()
    
    if modified_files:
        print("Fichiers modifiés:")
        for file in modified_files:
            print(f"  {file}")
        print()
    
    if untracked_files:
        print("Fichiers non trackés:")
        for file in untracked_files:
            print(f"  {file}")
        print()
    
    if not staged_files and not modified_files and not untracked_files:
        print("Working tree clean")
    
    return {
        'staged': staged_files,
        'modified': modified_files,
        'untracked': untracked_files
    }