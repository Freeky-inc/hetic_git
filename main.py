 #!/usr/bin/env python3
import argparse
from commands import init, add, commit, ls_files, ls_tree, cat_file, write_tree, reset, log, checkout, status


# description du projet
parser = argparse.ArgumentParser(description="Un clone de Git par le groupe 8 des Web2 de HETIC, écrit avec amour en Python.")
subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

# fyt init
parser_init = subparsers.add_parser("init", help="Initialise un dépôt")

# fyt add <file>
parser_add = subparsers.add_parser("add", help="Ajoute un ou plusieurs fichiers à l'index")
parser_add.add_argument("filename", nargs="+", help="Fichier(s) à ajouter")

# fyt commit -m "message"
parser_commit = subparsers.add_parser("commit", help="Crée un commit")
parser_commit.add_argument("-m", "--message", required=True, help="Message du commit")

# fyt log
parser_log = subparsers.add_parser("log", help="Affiche l'historique des commits")

# fyt checkout <branch>
parser_checkout = subparsers.add_parser("checkout", help="Change de branche ou restaure un commit")
parser_checkout.add_argument("-b", action="store_true", help="Créer une nouvelle branche")
parser_checkout.add_argument("branch_or_sha", help="Nom de la branche ou SHA du commit à checkout")

# fyt ls-files
parser_ls_files = subparsers.add_parser("ls-files", help="Affiche les fichiers dans l'index")
parser_ls_files.add_argument("--staged", action="store_true", help="Affiche les fichiers dans l'index (staged)")

# fyt ls-tree
parser_ls_tree = subparsers.add_parser("ls-tree", help="Affiche le contenu d'un objet tree")
parser_ls_tree.add_argument("tree_hash", help="Hash du tree à afficher")

# fyt cat-file
parser_cat_file = subparsers.add_parser("cat-file", help="Affiche le contenu d'un objet Git")
parser_cat_file.add_argument("-t", action="store_true", help="Affiche le type de l'objet")
parser_cat_file.add_argument("-p", action="store_true", help="Affiche le contenu de l'objet")
parser_cat_file.add_argument("hash", help="Hash de l'objet à afficher")

# fyt write-tree
parser_write_tree = subparsers.add_parser("write-tree", help="Crée un objet tree à partir de l'index")

# fyt reset
parser_reset = subparsers.add_parser("reset", help="Réinitialise l'index ou HEAD")
parser_reset.add_argument("-mixed", action="store_true", help="Réinitialise l\'index mais pas le répertoire de travail")
parser_reset.add_argument("-soft", action="store_true", help="Enlève les commits mais garde l'index et le répertoire de travail")
parser_reset.add_argument("-hard", action="store_true", help="Réinitialise l'index et le répertoire de travail")
parser_reset.add_argument("commit_hash", nargs="?", help="Hash du commit à réinitialiser")

# fyt status
parser_status = subparsers.add_parser("status", help="Affiche l'état des fichiers")

args = parser.parse_args()

if args.command == "init":
    init.run()
elif args.command == "add":
    add.run(args.filename)
elif args.command == "commit":
    commit.run(args.message)
elif args.command == "ls-files":
    arglist = []
    if args.staged:
        arglist.append('--staged')
    ls_files.run(arglist)
elif args.command == "ls-tree":
    ls_tree.run([args.tree_hash])
elif args.command == "cat-file":
    arglist = []
    if args.t:
        arglist.append('-t')
    arglist.append(args.hash)
    cat_file.run(arglist)
elif args.command == "write-tree":
    write_tree.run([])
elif args.command == "reset":
    arglist = []
    if args.soft:
        arglist.append('-soft')
    elif args.hard:
        arglist.append('-hard')
    elif args.mixed:
        arglist.append('-mixed')
    reset.run(arglist)
elif args.command == "log":
    log.run([])
elif args.command == "checkout":
    checkout.run(args.branch_or_sha, create_branch=args.b)
elif args.command == "status":
    status.run([])
else:
    parser.print_help()