#!/usr/bin/env python3
import os
import sys
import json

def find_fyt_dir(path):
    prev = None
    while path != prev:
        dot = os.path.join(path, ".fyt")
        if os.path.isdir(dot):
            return dot
        prev, path = path, os.path.dirname(path)
    sys.exit("Erreur : pas de dépôt .fyt ici.")

def ls_files():
    fytdir = find_fyt_dir(os.getcwd())
    idx = os.path.join(fytdir, "index")
    if not os.path.exists(idx):
        sys.exit("")  # index inexistant → rien à lister
    with open(idx, "r", encoding="utf-8") as f:
        index_data = json.load(f)
    for file_path in index_data.keys():
        print(file_path)

if __name__ == "__main__":
    ls_files()