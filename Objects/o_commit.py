import hashlib
import datetime
import os
import json

class Commit:
    def setCommit(self, tree_sha1, message, parent_sha1=None):
        # Construction du contenu du commit pour le hash
        commit_content = f"tree {tree_sha1}\n"
        commit_content += f"message {message}\n"
        if parent_sha1:
            commit_content += f"parent {parent_sha1}\n"

        commit_bytes = commit_content.encode("utf-8")
        self.sha1 = hashlib.sha1(commit_bytes).hexdigest()

        # Préparation des données à sauvegarder au format JSON
        commit_data = {
            "tree": tree_sha1,
            "message": message,
            "date": datetime.datetime.now().isoformat()
        }
        if parent_sha1:
            commit_data["parent"] = parent_sha1

        dir_path = ".fyt/objects/commit"
        file_path = os.path.join(dir_path, self.sha1)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = json.load(f)
                self.ref = content.get("tree")
                self.parent = content.get("parent")
                self.date = datetime.datetime.fromisoformat(content.get("date"))
                self.message = content.get("message")
            print("Un commit identique existe déjà. Aucun nouveau commit créé.")
            return

        self.ref = tree_sha1
        self.parent = parent_sha1
        self.date = datetime.datetime.fromisoformat(commit_data["date"])
        self.message = message

        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(commit_data, f)

    def getCommitHash(self):
        return self.sha1

    def getCommitDate(self):
        return self.date

    def getCommitRef(self):
        return self.ref

    def getCommitMessage(self):
        return self.message

    def getCommitParent(self):
        return self.parent