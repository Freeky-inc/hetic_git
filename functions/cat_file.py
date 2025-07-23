import os
import json

def exec_ext(nom_fichier):
    extensions_exec = {'.exe', '.bat', '.cmd', '.sh', '.bin', '.py', '.pl', '.rb', '.jar'}
    _, ext = os.path.splitext(nom_fichier.lower())
    return ext in extensions_exec

def cat_file(show_type: bool, pretty: bool, hash_id: str):
    """
    - show_type => option -t
    - pretty    => option -p
    - hash_id   => identifiant SHA1 de l'objet
    """
    base = "projet-test/.fyt/objects"
    dirs = {
        'blob': os.path.join(base, 'blob'),
        'tree': os.path.join(base, 'tree'),
        'commit': os.path.join(base, 'commit'),
    }

    # 1) détecte le dossier qui contient l'objet
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

    # 2) option -t : affiche seulement le type
    if show_type:
        print(obj_type)
        return

    # 3) option -p : pretty-print en fonction du type
    if pretty:
        if obj_type == 'blob':
            # lit le contenu brut et l'affiche
            with open(path, 'rb') as f:
                try:
                    print(f.read().decode('utf-8', errors='replace'), end='')
                except UnicodeDecodeError:
                    # binaire : afficher en hex
                    print(f.read().hex())
        elif obj_type == 'tree':
            # 1) Charge le JSON ; on accepte soit une liste directe, soit un dict {"files": [...]}
            with open(path, 'rb') as f:
                raw = f.read().decode('utf-8', errors='replace')
                data = json.loads(raw)
            entries = data['files'] if isinstance(data, dict) and 'files' in data else data

            # 2) Paramètre la colonne de début du nom (par exemple colonne 60)
            NAME_COL = 60

            for chemin, entry_hash in entries:
                name = os.path.basename(chemin)

                # Détermine mode/type comme avant
                tree_path = os.path.join(dirs['tree'], entry_hash)
                if os.path.isfile(tree_path):
                    mode = '040000'; typ = 'tree'
                else:
                    mode = '100755' if exec_ext(chemin) else '100644'
                    typ  = 'blob'

                # Prépare le préfixe et calcule le nombre d'espaces
                prefix = f"{mode} {typ} {entry_hash}"
                padding = max(1, NAME_COL - len(prefix))
                
                # Affichage final
                print(f"{prefix}{' ' * padding}{name}")

        elif obj_type == 'commit':
            # on suppose que le commit est stocké en JSON
            with open(path, 'rb') as f:
                data = json.loads(f.read().decode('utf-8'))
            # affiche chaque champ "clef: valeur"
            for k, v in data.items():
                # si c'est une liste (e.g. parent multiple), on lève chaque ligne
                if isinstance(v, list):
                    for item in v:
                        print(f"{k}: {item}")
                else:
                    print(f"{k}: {v}")
        return

    # 4) si ni -t ni -p, on avertit l'utilisateur
    print("Il faut choisir -t pour le type ou -p pour afficher le contenu.")
