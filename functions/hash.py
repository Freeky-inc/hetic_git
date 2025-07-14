#!/usr/bin/env python3
import sys
import hashlib

def git_hash_object(file_path):
    try:
        # 1. Vérifier que le fichier existe
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # 2. Construire l'en-tête du blob Git
        header = f"blob {len(content)}\0".encode('utf-8')
        blob_data = header + content
        
        # 3. Calculer le SHA-1
        sha1 = hashlib.sha1(blob_data).hexdigest()
        
        # 4. Afficher le hash
        print(sha1)
    
    except FileNotFoundError:
        print("Error: File does not exist or is a directory", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>", file=sys.stderr)
        sys.exit(1)
    
    git_hash_object(sys.argv[1])
