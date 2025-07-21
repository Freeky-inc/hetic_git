#!/usr/bin/env python3
import argparse
from commands import init, add, commit

def main():
    parser = argparse.ArgumentParser(description="Un clone de Git par le groupe 8 des Web2 de HETIC, écrit avec amour en Python.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # git init
    parser_init = subparsers.add_parser("init", help="Initialise un dépôt")

    # git add <file>
    parser_add = subparsers.add_parser("add", help="Ajoute un ou plusieurs fichiers à l'index")
    parser_add.add_argument("filename", nargs="+", help="Fichier(s) à ajouter")

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


if __name__ == "__main__":
    main()