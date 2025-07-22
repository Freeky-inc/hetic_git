import os

def reset(soft=None, mixed=None, hard=None):
    if soft:
        os.remove("projet-test/.fyt/HEAD")
        print("Réinitialisation en mode 'soft'. Les commits sont enlevés mais l'index et le répertoire de travail sont conservés.")
        # Logique pour la réinitialisation soft
    elif mixed:
        if os.path.exists("projet-test/.fyt/HEAD"):
            os.remove("projet-test/.fyt/HEAD")
        with open("projet-test/.fyt/index", "w") as f:
            pass 
        print("Réinitialisation en mode 'mixed'. L'index est réinitialisé mais le répertoire de travail est conservé.")
        # Logique pour la réinitialisation mixed
    elif hard:
        if os.path.exists("projet-test/.fyt/HEAD"):
            os.remove("projet-test/.fyt/HEAD")
        with open("projet-test/.fyt/index", "w") as f:
            pass 
        for root, dirs, files in os.walk("test/"):
            for file in files:
                file_path = os.path.join(root, file)
                if "projet-test/.fyt" not in file_path:
                    os.remove(file_path)
        print("Réinitialisation en mode 'hard'. L'index et le répertoire de travail sont réinitialisés.")
        # Logique pour la réinitialisation hard
    else:
        print("Aucun mode de réinitialisation spécifié. Veuillez utiliser -soft, -mixed ou -hard.")