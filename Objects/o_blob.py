class Blob:
    def setBlob(self, sha1, donnees):
        self.sha1 = sha1
        self.donnees = donnees

    def getBlobHash(self):
        return self.sha1