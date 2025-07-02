import json
import os

def rev_parse(ref):
    # 1. HEAD (fichier spécial)
    if ref == "HEAD" and os.path.exists(".fyt/HEAD"):
        with open(".fyt/HEAD", "r") as f:
            head_content = f.read().strip()
        if head_content.startswith("ref:"):
            # Résout la ref HEAD récursivement
            ref_path = head_content.split(":", 1)[1].strip()
            # Enlève le préfixe "refs/" si présent pour matcher les branches
            if ref_path.startswith("refs/"):
                ref_path = ref_path[5:]
            return rev_parse(ref_path)
        else:
            print(head_content)
            return

    # 2. refs (branche ou tag, y compris sous-dossiers)
    refs_root = ".fyt/refs"
    if os.path.exists(refs_root):
        for root, _, files in os.walk(refs_root):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, refs_root).replace("\\", "/")
                if ref == file or ref == rel_path:
                    with open(abs_path, "r") as f:
                        print(f.read().strip())
                    return

    # 3. objets (commit/tree/blob) et recherche par préfixe
    object_dirs = [
        ".fyt/objects/commit",
        ".fyt/objects/tree",
        ".fyt/objects/blob"
    ]
    possible_matches = []
    for obj_dir in object_dirs:
        if os.path.exists(obj_dir):
            for fname in os.listdir(obj_dir):
                if fname == ref:
                    print(fname)
                    return
                if fname.startswith(ref):
                    possible_matches.append(fname)
    if len(possible_matches) == 1:
        print(possible_matches[0])
        return
    elif len(possible_matches) > 1:
        print(f"Plusieurs objets correspondent au préfixe : {ref}")
        return

    # 4. index (blobs)
    index_path = ".fyt/index"
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
        if ref in index:
            print(index[ref])
            return
        for blob_hash in index.values():
            if ref == blob_hash:
                print(blob_hash)
                return
        matches = [blob_hash for blob_hash in index.values() if blob_hash.startswith(ref)]
        if len(matches) == 1:
            print(matches[0])
            return
        elif len(matches) > 1:
            print(f"Plusieurs objets correspondent au préfixe : {ref}")
            return

    print(f"Référence inconnue : {ref}")