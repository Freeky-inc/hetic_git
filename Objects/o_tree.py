import os
import json
import hashlib

class Tree:
    def setTree(self, root="projet-test"):
        with open("projet-test/.fyt/index", "r", encoding="utf-8") as idx_file:
            index = json.load(idx_file)

        files = []
        subtrees_done = set()

        for rel_path, blob_hash in index.items():
            # On ne prend que les fichiers dans le dossier courant ou ses sous-dossiers
            if ".fyt" in rel_path.split(os.sep):
                continue
            parts = rel_path.split(os.sep)
            # Fichier direct du dossier courant
            if len(parts) == 2 and parts[0] == os.path.basename(root):
                files.append([rel_path, blob_hash])
            # Fichier dans un sous-dossier
            elif len(parts) > 2 and parts[0] == os.path.basename(root):
                subdir = os.path.join(root, parts[1])
                if subdir not in subtrees_done:
                    subtree = Tree()
                    subtree.setTree(subdir)
                    files.append([subdir, subtree.sha1])
                    subtrees_done.add(subdir)

        tree_data = {"files": files}
        tree_json = json.dumps(tree_data).encode("utf-8")
        self.sha1 = hashlib.sha1(tree_json).hexdigest()
        self.files = files


        dir_path = "projet-test/.fyt/objects/tree/"
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, self.sha1)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(tree_json)

    def getFiles(self):
        return self.files