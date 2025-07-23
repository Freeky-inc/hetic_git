from core import Repository

def commit(message):
    """
    Crée un commit avec les fichiers staged.
    """
    repo = Repository()
    commit_hash = repo.create_commit(message)
    
    if commit_hash:
        print(f"Commit créé: {commit_hash}")
        return commit_hash
    else:
        print("Erreur lors de la création du commit.")
        return None 