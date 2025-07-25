import os
import hashlib
import stat

class Tree:
    def setTree(self, root="projet-test"):
        index_path = os.path.join("projet-test", ".fyt", "index")
        with open(index_path, "r", encoding="utf-8") as idx_file:
            index = eval(idx_file.read())  # lecture sans JSON

        files = []
        subtrees_done = set()
        root_parts = os.path.normpath(root).split(os.sep)

        tree_data = ""

        for rel_path, blob_hash in index.items():
            if ".fyt" in rel_path.split(os.sep):
                continue

            parts = rel_path.split(os.sep)
            if parts[:len(root_parts)] != root_parts:
                continue

            # On calcule le chemin relatif au dossier "root"
            relative_to_root = os.path.join(*parts[len(root_parts):])

            # Fichier direct dans le dossier courant
            if len(parts) == len(root_parts) + 1:
                mode = os.stat(rel_path).st_mode
                octal_mode = oct(stat.S_IFMT(mode) | stat.S_IMODE(mode)).replace("0o", "").zfill(6)
                tree_data += f"{octal_mode} {relative_to_root} {blob_hash}\n"
                files.append([relative_to_root, blob_hash])

            # Sous-dossier
            elif len(parts) > len(root_parts) + 1:
                subdir = os.path.join(*parts[:len(root_parts)+1])
                relative_subdir = os.path.join(*parts[len(root_parts):len(root_parts)+1])

                if subdir not in subtrees_done:
                    subtree = Tree()
                    subtree.setTree(subdir)
                    mode = "040000"
                    tree_data += f"{mode} {relative_subdir} {subtree.sha1}\n"
                    files.append([relative_subdir, subtree.sha1])
                    subtrees_done.add(subdir)

        # SHA du contenu
        self.sha1 = hashlib.sha1(tree_data.encode("utf-8")).hexdigest()
        self.files = files

        # Sauvegarde
        dir_path = os.path.join("projet-test", ".fyt", "objects", "tree")
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, self.sha1)

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(tree_data)

    def getFiles(self):
        return self.files
