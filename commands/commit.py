# commands/commit.py

"""
# commands/commit.py
Module pour créer un commit dans le dépôt Git.
Ce module lit l'index, crée un objet Tree à partir des entrées de l'index,
et crée un objet Commit avec les métadonnées appropriées.
"""
from core.index import GitIndex
from core.objects import GitObject
from core.refs import get_head, update_ref, read_ref

def run(message):
    index = GitIndex()
    entries = []

    for path, sha in index.entries.items():
        mode = "100644"
        entries.append(f"{mode} {path}\0".encode() + bytes.fromhex(sha))

    tree = GitObject("tree", b"".join(entries))
    tree_sha = tree.store()

    parent_sha = read_ref(get_head())
    lines = [f"tree {tree_sha}"]
    if parent_sha:
        lines.append(f"parent {parent_sha}")
    lines.append("author You <you@example.com>")
    lines.append("committer You <you@example.com>")
    lines.append("")
    lines.append(message)

    commit = GitObject("commit", "\n".join(lines).encode())
    sha = commit.store()

    update_ref(get_head(), sha)
    print(f"Committed as {sha}")
