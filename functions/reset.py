import os

def reset(soft=None, mixed=None, hard=None):
    if soft:
        os.remove(".fyt/HEAD")
        print("Réinitialisation en mode 'soft'. Les commits sont enlevés mais l'index et le répertoire de travail sont conservés.")
        # Logique pour la réinitialisation soft
    elif mixed:
        if os.path.exists(".fyt/HEAD"):
            os.remove(".fyt/HEAD")
        with open(".fyt/index", "w") as f:
            pass 
        print("Réinitialisation en mode 'mixed'. L'index est réinitialisé mais le répertoire de travail est conservé.")
        # Logique pour la réinitialisation mixed
    elif hard:
        if os.path.exists(".fyt/HEAD"):
            os.remove(".fyt/HEAD")
        with open(".fyt/index", "w") as f:
            pass 
        for root, dirs, files in os.walk("test/"):
            for file in files:
                file_path = os.path.join(root, file)
                if ".fyt" not in file_path:
                    os.remove(file_path)
        print("Réinitialisation en mode 'hard'. L'index et le répertoire de travail sont réinitialisés.")
        # Logique pour la réinitialisation hard
    else:
        print("Aucun mode de réinitialisation spécifié. Veuillez utiliser -soft, -mixed ou -hard.")