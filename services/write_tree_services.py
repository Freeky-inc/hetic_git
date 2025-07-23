from core import Repository

def write_tree():
    """
    Écrit un tree à partir de l'index et retourne son hash.
    """
    repo = Repository()
    
    # Récupérer tous les fichiers de l'index
    files = repo.index.get_all_files()
    
    if not files:
        print("Aucun fichier dans l'index.")
        return None
    
    # Créer les entrées du tree
    from core.objects import TreeEntry
    entries = []
    
    for filename in files:
        entry = repo.index.get_entry(filename)
        if entry:
            tree_entry = TreeEntry(
                mode=entry.mode,
                name=filename,
                sha=entry.sha
            )
            entries.append(tree_entry)
    
    # Créer et stocker le tree
    tree_hash = repo.tree_manager.create_tree(entries)
    print(tree_hash)
    return tree_hash