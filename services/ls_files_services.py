from core import Repository

def ls_files(staged_only=False):
    """
    Liste les fichiers dans l'index Git.
    """
    repo = Repository()
    
    files = repo.index.get_all_files()
    
    if staged_only:
        # Afficher seulement les fichiers staged
        for filename in files:
            entry = repo.index.get_entry(filename)
            if entry and entry.stage == 0:
                print(filename)
    else:
        # Afficher tous les fichiers
        for filename in files:
            print(filename)
    
    return files