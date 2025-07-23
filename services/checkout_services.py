from core import Repository

def checkout(commit_hash):
    """
    Checkout un commit spécifique.
    """
    repo = Repository()
    
    # Vérifier que le commit existe
    if not repo.commit_manager.commit_exists(commit_hash):
        print(f"Commit non trouvé: {commit_hash}")
        return False
    
    # Récupérer le tree du commit
    commit = repo.commit_manager.get_commit(commit_hash)
    tree_hash = commit.tree_hash
    
    # TODO: Implémenter la logique de checkout
    # Pour l'instant, on affiche juste les informations
    print(f"Checkout du commit {commit_hash}")
    print(f"Tree: {tree_hash}")
    print(f"Message: {commit.message}")
    
    return True