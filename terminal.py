import argparse

from functions.add import add_file, status_all
from functions.commit import commit_changes
from functions.cat_file import cat_file
from functions.checkout import checkout
from functions.commit_tree import commit_tree
from functions.init import init_repo
from functions.log import log
from functions.ls_files import ls_files
from functions.ls_tree import ls_tree
from functions.reset import reset
from functions.rev_parse import rev_parse
from functions.show_ref import show_ref
from functions.write_tree import write_tree


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# git add <file>
parser_add = subparsers.add_parser("add", help="Ajoute un fichier à l'index")
parser_add.add_argument("file", help="Fichier à ajouter")

# git cat-file -t -p <hash>
cat_file_parser = subparsers.add_parser("cat-file", help="Crée un tree à partir de l'index")
cat_file_parser.add_argument("-t", action="store_true", help="Affiche le type de l'objet")
cat_file_parser.add_argument("-p", action="store_true", help="Affiche le contenu de l'objet")
cat_file_parser.add_argument("hash", help="Affiche l'ID de l'objet")

# git checkout -b <branch>
checkout_parser = subparsers.add_parser("checkout", help="Change de branche")
checkout_parser.add_argument("-b", action="store_true", help="Crée une nouvelle branche")
checkout_parser.add_argument("branch", help="Branche à laquelle se déplacer")

# git commit -m "message"
parser_commit = subparsers.add_parser("commit", help="Crée un commit")
parser_commit.add_argument("-m", "--message", required=True, help="Message du commit")

# git commit-tree <tree_sha> -m "message" [-p <parent_sha>]
commit_tree_parser = subparsers.add_parser("commit-tree", help="Crée un commit à partir d'un tree existant")
commit_tree_parser.add_argument("tree_sha", help="SHA1 du tree à committer")
commit_tree_parser.add_argument("-m", required=True, help="message du commit")
commit_tree_parser.add_argument("-p", help="SHA1 du commit parent (optionnel)")

# git init
subparsers.add_parser("init", help="Initialise un dépôt")

# git log
subparsers.add_parser("log", help="Affiche l'historique des commits")

# git ls-files
subparsers.add_parser("ls-files", help="Liste les fichiers dans l'index")

# git ls-tree <tree_sha>
tree_parser = subparsers.add_parser("ls-tree", help="Liste les fichiers dans un tree")
tree_parser.add_argument("tree_sha", help="SHA1 du tree à lister")

# git reset -soft -mixed -hard <sha>
parser_reset = subparsers.add_parser("reset", help="Réinitialise l'index et le répertoire de travail")
parser_reset.add_argument("-soft", action="store_true", help="Enlève les commits mais garde l'index et le répertoire de travail")
parser_reset.add_argument("-mixed", action="store_true", help="Réinitialise l\'index mais pas le répertoire de travail")
parser_reset.add_argument("-hard", action="store_true", help="Réinitialise l'index et le répertoire de travail")
parser_reset.add_argument("-nuke", action="store_true", help="Supprime TOUT (avec une petite surprise)")

# git rev-parse <ref>
parser_rev_parse = subparsers.add_parser("rev-parse", help="Convertit une référence Git en SHA1")
parser_rev_parse.add_argument("ref", help="Référence Git à convertir en SHA1")

# git status-all
status_parser = subparsers.add_parser("status-all", help="Affiche le statut de tous les fichiers")

#git show-ref
subparsers.add_parser("show-ref", help="Affiche les références du dépôt")

# git write-tree
subparsers.add_parser("write-tree", help="Crée un tree à partir de l'index")

args = parser.parse_args()


if args.command == "add":
    add_file(args.file)   
elif args.command == "commit":
    commit_changes(args.message)
elif args.command == "cat-file":
    cat_file(args.t, args.p, args.hash)
elif args.command == "checkout":
    checkout(args.b, args.branch)
elif args.command == "commit-tree":
    commit_tree(args.tree_sha, args.m, args.p)                                    
elif args.command == "init":
    init_repo()
elif args.command == "log":
    log()
elif args.command == "ls-files":
    ls_files()
elif args.command == "ls-tree":
    ls_tree(args.tree_sha)    
elif args.command == "reset":
    reset(args.soft, args.mixed, args.hard, args.nuke)
elif args.command == "rev-parse":
    rev_parse(args.ref)
elif args.command == "status-all":
    status_all()
elif args.command == "show-ref":
    show_ref()
elif args.command == "write-tree":
    write_tree()
else:
    parser.print_help()