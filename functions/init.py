import os

def init_repo():
    os.makedirs(".fyt/objects", exist_ok=True)
    os.makedirs(".fyt/refs/heads", exist_ok=True)
    with open(".fyt/HEAD", "w") as f:
        f.write("ref: refs/heads/main\n")
    print("Dépôt initialisé.\nVous êtes dans la branche 'main'.")