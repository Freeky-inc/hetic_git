import os
import json
import hashlib

class Tree:
    def setTree(self, root="projet-test"):
        with open("projet-test/.fyt/index", "r", encoding="utf-8") as idx_file:
            index = json.load(idx_file)

        files = []
        subtrees_done = set()
        root_parts = os.path.normpath(root).split(os.sep)

        for rel_path, blob_hash in index.items():
            if ".fyt" in rel_path.split(os.sep):
                continue
            parts = rel_path.split(os.sep)
            # Fichier direct du dossier courant
            if parts[:len(root_parts)] == root_parts and len(parts) == len(root_parts) + 1:
                files.append([rel_path, blob_hash])
            # Fichier dans un sous-dossier direct
            elif parts[:len(root_parts)] == root_parts and len(parts) > len(root_parts) + 1:
                subdir = os.path.join(*parts[:len(root_parts)+1])
                subdir_full = os.path.join(*root_parts, parts[len(root_parts)])
                if subdir_full not in subtrees_done:
                    subtree = Tree()
                    subtree.setTree(subdir_full)
                    files.append([subdir_full, subtree.sha1])
                    subtrees_done.add(subdir_full)

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