import sys
import os
import json

def find_fyt_dir(path):
    prev = None
    while path != prev:
        dot = os.path.join(path, "projet-test/.fyt")
        if os.path.isdir(dot):
            return dot
        prev, path = path, os.path.dirname(path)
    sys.exit("Erreur : pas de dépôt .fyt ici.")

def ls_tree(tree_sha): 
    fytdir = find_fyt_dir(os.getcwd())
    tree_path = os.path.join(fytdir, "objects", "tree", tree_sha)
    if not os.path.exists(tree_path):
        sys.exit(f"Erreur : tree {tree_sha} introuvable.")
    with open(tree_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            print("Tree vide.")
            return
        
        tree_data = json.loads(content)
    if isinstance(tree_data, dict) and "files" in tree_data:
        for file_path, sha in tree_data["files"]:
            print(f"100644 blob {sha}\t{file_path}")
    else:
        print("Format de tree inattendu :\n" + str(tree_data))

if __name__ == "__main__":
    ls_tree(sys.argv[1])