import os

def exec_ext(nom_fichier):
    extensions_exec = {'.exe', '.bat', '.cmd', '.sh', '.bin', '.py', '.pl', '.rb', '.jar'}
    _, ext = os.path.splitext(nom_fichier.lower())
    return ext in extensions_exec

def cat_file(show_type: bool, pretty: bool, hash_id: str):
    base = "projet-test/.fyt/objects"
    dirs = {
        'blob': os.path.join(base, 'blob'),
        'tree': os.path.join(base, 'tree'),
        'commit': os.path.join(base, 'commit'),
    }

    obj_type = None
    path = None
    for t, d in dirs.items():
        candidate = os.path.join(d, hash_id)
        if os.path.isfile(candidate):
            obj_type = t
            path = candidate
            break

    if obj_type is None:
        print(f"Objet {hash_id} introuvable.")
        return

    if show_type:
        print(obj_type)
        return

    if pretty:
        if obj_type == 'blob':
            with open(path, 'rb') as f:
                try:
                    print(f.read().decode('utf-8', errors='replace'), end='')
                except UnicodeDecodeError:
                    print(f.read().hex())

        elif obj_type == 'tree':
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()

            NAME_COL = 60

            for line in lines:
                # chaque ligne est du type : "100644 chemin hash"
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                mode, chemin, entry_hash = parts
                name = os.path.basename(chemin)

                if os.path.isfile(os.path.join(dirs['tree'], entry_hash)):
                    mode = "040000"
                    typ = "tree"
                else:
                    typ = "blob"
                    mode = "100755" if exec_ext(chemin) else "100644"

                prefix = f"{mode} {typ} {entry_hash}"
                padding = max(1, NAME_COL - len(prefix))
                print(f"{prefix}{' ' * padding}{name}")

        elif obj_type == 'commit':
            with open(path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
                for line in lines:
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        if " " in value:
                            for v in value.split():
                                print(f"{key}: {v}")
                        else:
                            print(f"{key}: {value}")
                    else:
                        print(line)

        return

    print("Il faut choisir -t pour le type ou -p pour afficher le contenu.")