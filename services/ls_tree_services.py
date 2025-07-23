from core import Repository

def ls_tree(tree_hash=None, recursive=False):
    """
    Liste le contenu d'un tree Git.
    """
    repo = Repository()
    
    # Si aucun hash n'est fourni, utiliser le tree du dernier commit
    if not tree_hash:
        head_hash = repo.refs.get_head()
        if not head_hash:
            print("Aucun commit trouvé.")
            return
        
        commit = repo.commit_manager.get_commit(head_hash)
        tree_hash = commit.tree_hash
    
    # Récupérer le tree
    tree = repo.tree_manager.get_tree(tree_hash)
    
    if not tree:
        print(f"Tree non trouvé: {tree_hash}")
        return
    
    # Afficher les entrées
    for entry in tree.entries:
        mode = entry.mode
        name = entry.name
        sha = entry.sha
        
        # Déterminer le type
        if mode.startswith("100"):
            obj_type = "blob"
        elif mode.startswith("040"):
            obj_type = "tree"
        else:
            obj_type = "unknown"
        
        print(f"{mode} {obj_type} {sha}\t{name}")
        
        # Récursion si demandé et que c'est un tree
        if recursive and obj_type == "tree":
            print(f"Tree {sha}:")
            ls_tree(sha, recursive)
            print()