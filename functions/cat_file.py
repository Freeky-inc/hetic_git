import os
import json

def cat_file(t, prettier, hash_id):
    # Recherche dans les dossiers d'objets possibles
    object_dirs = [
        "projet-test/.fyt/objects/blob",
        "projet-test/.fyt/objects/tree",
        "projet-test/.fyt/objects/commit"
    ]
    found = False
    for obj_dir in object_dirs:
        file_path = os.path.join(obj_dir, hash_id)
        if os.path.exists(file_path):
            found = True
            # Affiche le type si demandé
            if t:
                if "blob" in obj_dir:
                    print("blob")
                elif "tree" in obj_dir:
                    print("tree")
                elif "commit" in obj_dir:
                    print("commit")
                else:
                    print("unknown")
            # Affiche le contenu si demandé
            if prettier:
                with open(file_path, "rb") as f:
                    try:
                        content = f.read().decode("utf-8")
                        # Si c'est du JSON, affiche joliment
                        try:
                            data = json.loads(content)
                            print(json.dumps(data, indent=2, ensure_ascii=False))
                        except Exception:
                            print(content)
                    except Exception:
                        print(f"[binaire] {hash_id}")
            # Affiche le hash si demandé
            if not t and not prettier:
                print("Il faut choisir une option pour afficher le contenu ou le type de l'objet.")
            break
    if not found:
        print(f"Objet {hash_id} introuvable.")