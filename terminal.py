import argparse
from ls_files import ls_files
from write_tree import write_tree
from commit_tree import commit_tree

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

# Sous-commande ls-files
subparsers.add_parser("ls-files")

# Sous-commande write-tree
subparsers.add_parser("write-tree")

commit_tree_parser = subparsers.add_parser("commit-tree")
commit_tree_parser.add_argument("tree_sha", help="SHA1 du tree à committer")
commit_tree_parser.add_argument("-m", required=True, help="message du commit")
commit_tree_parser.add_argument("-p", help="SHA1 du commit parent (optionnel)")

args = parser.parse_args()

if args.command == "ls-files":
    ls_files()
elif args.command == "write-tree":
    write_tree()
elif args.command == "commit-tree":
    commit_tree(args.tree_sha, args.m, args.p)