import os
import json
import hashlib
import datetime

def init_repo():
    os.makedirs("projet-test/.fyt/objects/blob", exist_ok=True)
    os.makedirs("projet-test/.fyt/objects/tree", exist_ok=True)
    os.makedirs("projet-test/.fyt/objects/commit", exist_ok=True)
    os.makedirs("projet-test/.fyt/refs/heads", exist_ok=True)

    # Créer un tree vide
    tree_data = {"files": []}
    tree_json = json.dumps(tree_data).encode()
    tree_hash = hashlib.sha1(tree_json).hexdigest()
    with open(f"projet-test/.fyt/objects/tree/{tree_hash}", "wb") as f:
        f.write(tree_json)

    # Créer le commit initial
    commit_data = {
        "tree": tree_hash,
        "message": "Initial commit",
        "date": datetime.datetime.now().isoformat(),
        "parents": []
    }
    commit_json = json.dumps(commit_data).encode()
    commit_hash = hashlib.sha1(commit_json).hexdigest()
    with open(f"projet-test/.fyt/objects/commit/{commit_hash}", "wb") as f:
        f.write(commit_json)

    # Crée la branche main et écrit le SHA du commit initial
    main_ref = "projet-test/.fyt/refs/heads/main"
    with open(main_ref, "w") as f:
        f.write(commit_hash)

    # Met HEAD sur main
    with open("projet-test/.fyt/HEAD", "w") as f:
        f.write("ref: refs/heads/main")
    print("Dépôt initialisé avec commit initial.")