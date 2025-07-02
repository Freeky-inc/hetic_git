import argparse

from functions.add import add_file
from functions.commit import commit_changes
from functions.commit_tree import commit_tree
from functions.init import init_repo
from functions.ls_files import ls_files
from functions.show_ref import show_ref
from functions.write_tree import write_tree


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# git add <file>
parser_add = subparsers.add_parser("add", help="Ajoute un fichier à l'index")
parser_add.add_argument("file", help="Fichier à ajouter")

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

# git ls-files
subparsers.add_parser("ls-files", help="Liste les fichiers dans l'index")

#git show-ref
subparsers.add_parser("show-ref", help="Affiche les références du dépôt")

# git write-tree
subparsers.add_parser("write-tree", help="Crée un tree à partir de l'index")

args = parser.parse_args()


if args.command == "add":
    add_file(args.file) # Revoir la conception du fichier Blob. 
                        # Il faut passer par l'objet Blob pour ajouter le fichier    
elif args.command == "commit":
    commit_changes(args.message)
elif args.command == "commit-tree":             # Faire en sorte que, si le hash du tree n'est 
    commit_tree(args.tree_sha, args.m, args.p)  # pas correct, on lève une erreur                                            
elif args.command == "init":
    init_repo()
elif args.command == "ls-files":
    ls_files()
elif args.command == "show-ref":
    show_ref()
elif args.command == "write-tree":
    write_tree()
else:
    parser.print_help()