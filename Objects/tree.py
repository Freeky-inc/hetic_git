import os
import hashlib

class Tree:
    def setTree(self, blobsha1_list):
        contenu_total = b""
        for blob_path in blobsha1_list:
            with open(blob_path, "rb") as f:
                contenu_total += f.read()
        header = f"tree {len(contenu_total)}\0".encode("utf-8")
        tree_data = header + contenu_total

        self.sha1 = hashlib.sha1(tree_data).hexdigest()
        self.blobsha1 = blobsha1_list

        # Sauvegarde dans test/objects/
        dir_path = "test/objects/tree/" 
        file_path = os.path.join(dir_path, self.sha1)
        if os.path.exists(file_path):
            print("Un commit identique existe déjà. Aucun nouveau commit créé.")
            return
        
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(tree_data)

    def getBlob(self):
        return self.blobsha1