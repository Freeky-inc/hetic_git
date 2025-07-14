import os
import json
import hashlib

class Tree:
    def setTree(self):
        # Charge l'index pour obtenir les chemins d'origine et les hashes de blob
        with open(".fyt/index", "r", encoding="utf-8") as idx_file:
            index = json.load(idx_file)

        # Construit la liste des fichiers pour le tree
        files = [[path, blob_hash] for path, blob_hash in index.items()]

        tree_data = {"files": files}
        tree_json = json.dumps(tree_data).encode("utf-8")
        self.sha1 = hashlib.sha1(tree_json).hexdigest()
        self.files = files

        # Sauvegarde dans .fyt/objects/tree/
        dir_path = ".fyt/objects/tree/"
        file_path = os.path.join(dir_path, self.sha1)
        if os.path.exists(file_path):
            print("Un tree identique existe déjà. Aucun nouveau tree créé.")
            return

        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(tree_json)

    def getFiles(self):
        return self.files