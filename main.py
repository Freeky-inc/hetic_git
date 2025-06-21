#!/usr/bin/env python3
import argparse
# import os
# import hashlib
# import json
# import datetime
# from core.objects import GitObject
from commands import init, add, commit

def main():
    parser = argparse.ArgumentParser(description="Un clone de Git par le groupe 8 des Web2 de HETIC, écrit avec amour en Python.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # git init
    parser_init = subparsers.add_parser("init", help="Initialise un dépôt")

    # git add <file>
    parser_add = subparsers.add_parser("add", help="Ajoute un ou plusieurs fichiers à l'index")
    parser_add.add_argument("filename", help="Fichier(s) à ajouter")

    # git commit -m "message"
    parser_commit = subparsers.add_parser("commit", help="Crée un commit")
    parser_commit.add_argument("-m", "--message", required=True, help="Message du commit")

    args = parser.parse_args()

    if args.command == "init":
        init.run()
    elif args.command == "add":
        add.run(args.filename)
    elif args.command == "commit":
        commit.run(args.message)
    else:
        parser.print_help()

# def init_repo():
#     os.makedirs(".fyt/objects", exist_ok=True)
#     os.makedirs(".fyt/refs/heads", exist_ok=True)
#     with open(".fyt/HEAD", "w") as f:
#         f.write("ref: refs/heads/main\n")
#     print("Dépôt initialisé.\nVous êtes dans la branche 'main'.")


# def commit_changes(message):
#     # Créer un Tree (simplifié)
#     tree_data = {"files": []}  # En vrai, on stocke une structure de dossiers/fichiers
#     tree_json = json.dumps(tree_data).encode()
#     tree_hash = hashlib.sha1(tree_json).hexdigest()

#     with open(f".fyt/objects/{tree_hash}", "wb") as f:
#         f.write(tree_json)

#     # Créer un Commit
#     commit_data = {
#         "tree": tree_hash,
#         "message": message,
#         "date": datetime.datetime.now().isoformat(),
#     }
#     commit_json = json.dumps(commit_data).encode()
#     commit_hash = hashlib.sha1(commit_json).hexdigest()

#     with open(f".fyt/objects/{commit_hash}", "wb") as f:
#         f.write(commit_json)

#     # Mettre à jour la référence (branche)
#     with open(".fyt/refs/heads/main", "w") as f:
#         f.write(commit_hash)

#     print(f"Commit [{commit_hash[:6]}]: {message}")

    # def write_object(git_object: GitObject):
    #     import zlib, os
    #     sha = git_object.sha1()
    #     path = f".git/objects/{sha[:2]}/{sha[2:]}"
    #     os.makedirs(os.path.dirname(path), exist_ok=True)
    #     with open(path, "wb") as f:
    #         f.write(zlib.compress(git_object.serialize()))
    #     return sha


if __name__ == "__main__":
    main()