import hashlib
import datetime
import os

class Commit:
    def setCommit(self, tree_sha1, message, parent_sha1=None):
        
        # Construction du contenu du commit
        commit_content = f"tree {tree_sha1}\n"
        commit_content += f"message {message}\n"
        commit_content += f"date {datetime.datetime.now().isoformat()}\n"
        if parent_sha1:
            commit_content += f"parent {parent_sha1}\n"

        commit_bytes = commit_content.encode("utf-8")

        self.sha1 = hashlib.sha1(commit_bytes).hexdigest()

        # Sauvegarde dans test/objects/
        dir_path = "test/objects/commit"
        file_path = os.path.join(dir_path, self.sha1)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read().decode("utf-8")
                for line in content.splitlines():
                    if line.startswith("tree "):
                        self.ref = line[5:]
                    elif line.startswith("parent "):
                        self.parent = line[7:]
                    elif line.startswith("date "):
                        self.date = datetime.datetime.fromisoformat(line[5:])
                parts = content.split("\n\n", 1)
                
                if len(parts) > 1:
                    self.message = parts[1].strip()
            print("Un commit identique existe déjà. Aucun nouveau commit créé.")
            return
        
        self.ref = tree_sha1
        self.date = datetime.datetime.now()
        self.message = message

        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(commit_bytes)

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