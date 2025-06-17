#!/usr/bin/env python3
import argparse
import os
import hashlib
import json
import datetime

def main():
    parser = argparse.ArgumentParser(description="Un mini-Git (Fyt) en Python.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # git init
    parser_init = subparsers.add_parser("init", help="Initialise un dépôt")

    # git add <file>
    parser_add = subparsers.add_parser("add", help="Ajoute un fichier à l'index")
    parser_add.add_argument("file", help="Fichier à ajouter")

    # git commit -m "message"
    parser_commit = subparsers.add_parser("commit", help="Crée un commit")
    parser_commit.add_argument("-m", "--message", required=True, help="Message du commit")

    args = parser.parse_args()

    if args.command == "init":
        init_repo()
    elif args.command == "add":
        add_file(args.file)
    elif args.command == "commit":
        commit_changes(args.message)
    else:
        parser.print_help()

def init_repo():
    os.makedirs(".fyt/objects", exist_ok=True)
    os.makedirs(".fyt/refs/heads", exist_ok=True)
    with open(".fyt/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Dépôt initialisé.\nVous êtes dans la branche 'main'.")

def update_index(file_path, blob_hash):
    print("hello")
    if not os.path.isfile(file_path):
        print("le fichier n'existe pas")

    # si le fichier existe, je vais sortir le h du fichier pour le comparer

def add_file(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    blob_hash = hashlib.sha1(content).hexdigest()
    blob_path = f".fyt/objects/{blob_hash}"

    with open(blob_path, "wb") as f:
        f.write(content)

    update_index(file_path, blob_hash)
    print(f"Fichier '{file_path}' ajouté (Blob: {blob_hash})")



def commit_changes(message):
    # Créer un Tree (simplifié)
    tree_data = {"files": []}  # En vrai, on stocke une structure de dossiers/fichiers
    tree_json = json.dumps(tree_data).encode()
    tree_hash = hashlib.sha1(tree_json).hexdigest()

    with open(f".fyt/objects/{tree_hash}", "wb") as f:
        f.write(tree_json)

    # Créer un Commit
    commit_data = {
        "tree": tree_hash,
        "message": message,
        "date": datetime.datetime.now().isoformat(),
    }
    commit_json = json.dumps(commit_data).encode()
    commit_hash = hashlib.sha1(commit_json).hexdigest()

    with open(f".fyt/objects/{commit_hash}", "wb") as f:
        f.write(commit_json)

    # Mettre à jour la référence (branche)
    with open(".fyt/refs/heads/main", "w") as f:
        f.write(commit_hash)

    print(f"Commit [{commit_hash[:6]}]: {message}")

if __name__ == "__main__":
    main()