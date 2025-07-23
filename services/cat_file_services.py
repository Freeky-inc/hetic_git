from core import Repository

def cat_file(sha):
    """
    Affiche le contenu d'un objet Git.
    """
    repo = Repository()
    
    # Essayer de lire comme un blob
    try:
        blob = repo.blob_manager.get_blob(sha)
        print(blob.content.decode('utf-8', errors='ignore'))
        return
    except:
        pass
    
    # Essayer de lire comme un tree
    try:
        tree = repo.tree_manager.get_tree(sha)
        for entry in tree.entries:
            print(f"{entry.mode} {entry.sha}\t{entry.name}")
        return
    except:
        pass
    
    # Essayer de lire comme un commit
    try:
        commit = repo.commit_manager.get_commit(sha)
        print(f"tree {commit.tree_hash}")
        if commit.parent_hash:
            print(f"parent {commit.parent_hash}")
        print(f"author {commit.author}")
        print(f"committer {commit.author}")
        print()
        print(commit.message)
        return
    except:
        pass
    
    print(f"Objet non trouvé: {sha}") 