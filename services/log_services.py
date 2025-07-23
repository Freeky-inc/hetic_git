from core import Repository

def log():
    """
    Affiche l'historique des commits.
    """
    repo = Repository()
    
    # Récupérer le hash du dernier commit
    head_hash = repo.refs.get_head()
    
    if not head_hash:
        print("Aucun commit trouvé.")
        return
    
    # Parcourir l'historique
    current_hash = head_hash
    while current_hash:
        commit = repo.commit_manager.get_commit(current_hash)
        if not commit:
            break
        
        print(f"commit {current_hash}")
        print(f"Author: {commit.author}")
        print(f"Date: {commit.timestamp}")
        print()
        print(f"    {commit.message}")
        print()
        
        # Passer au parent
        current_hash = commit.parent_hash