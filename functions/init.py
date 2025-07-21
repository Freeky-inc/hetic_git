import os

def init_repo():
    os.makedirs("projet-test/.fyt/objects", exist_ok=True)
    os.makedirs("projet-test/.fyt/refs/heads", exist_ok=True)
    with open("projet-test/.fyt/index", "w", encoding="utf-8") as f:
        f.write("{}")
    with open("projet-test/.fyt/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Dépôt initialisé.\nVous êtes dans la branche 'main'.")