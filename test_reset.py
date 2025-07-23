#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement de reset.
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Exécute une commande et retourne le résultat."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def test_reset():
    """Test de la commande reset."""
    print("=== Test de reset ===")
    
    # 1. Vérifier que nous sommes dans un dépôt
    print("1. Vérification du dépôt...")
    if not os.path.exists(".fyt"):
        print("❌ Pas de dépôt .fyt trouvé. Initialisons-en un...")
        code, out, err = run_command("python3 main.py init")
        if code != 0:
            print(f"❌ Erreur lors de l'initialisation: {err}")
            return False
        print("✅ Dépôt initialisé.")
    
    # 2. Créer des fichiers de test
    print("\n2. Création de fichiers de test...")
    test_files = ["file1.txt", "file2.txt", "file3.txt"]
    
    for file_path in test_files:
        with open(file_path, "w") as f:
            f.write(f"Contenu de {file_path}")
        print(f"✅ Fichier créé: {file_path}")
    
    # 3. Ajouter les fichiers
    print("\n3. Ajout des fichiers...")
    for file_path in test_files:
        code, out, err = run_command(f"python3 main.py add {file_path}")
        if code != 0:
            print(f"❌ Erreur lors de l'ajout de {file_path}: {err}")
            return False
        print(f"✅ Fichier ajouté: {file_path}")
    
    # 4. Vérifier que les fichiers sont dans l'index
    print("\n4. Vérification de l'index avant reset...")
    code, out, err = run_command("python3 main.py ls-files")
    if code != 0:
        print(f"❌ Erreur lors de ls-files: {err}")
        return False
    
    print("✅ Fichiers dans l'index avant reset:")
    print(out)
    
    # 5. Test reset mixed
    print("\n5. Test de reset --mixed...")
    code, out, err = run_command("python3 main.py reset --mixed")
    if code != 0:
        print(f"❌ Erreur lors de reset --mixed: {err}")
        return False
    
    print("✅ Sortie de reset --mixed:")
    print(out)
    
    # 6. Vérifier que l'index est vide
    print("\n6. Vérification de l'index après reset mixed...")
    code, out, err = run_command("python3 main.py ls-files")
    if code != 0:
        print(f"❌ Erreur lors de ls-files: {err}")
        return False
    
    print("✅ Fichiers dans l'index après reset mixed:")
    print(out)
    
    # 7. Vérifier que les fichiers existent toujours dans le répertoire de travail
    print("\n7. Vérification des fichiers dans le répertoire de travail...")
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"✅ Fichier existe toujours: {file_path}")
        else:
            print(f"❌ Fichier manquant: {file_path}")
            return False
    
    # 8. Réajouter les fichiers pour tester reset hard
    print("\n8. Réajout des fichiers pour tester reset hard...")
    for file_path in test_files:
        code, out, err = run_command(f"python3 main.py add {file_path}")
        if code != 0:
            print(f"❌ Erreur lors de l'ajout de {file_path}: {err}")
            return False
        print(f"✅ Fichier réajouté: {file_path}")
    
    # 9. Test reset hard
    print("\n9. Test de reset --hard...")
    code, out, err = run_command("python3 main.py reset --hard")
    if code != 0:
        print(f"❌ Erreur lors de reset --hard: {err}")
        return False
    
    print("✅ Sortie de reset --hard:")
    print(out)
    
    # 10. Vérifier que l'index est vide
    print("\n10. Vérification de l'index après reset hard...")
    code, out, err = run_command("python3 main.py ls-files")
    if code != 0:
        print(f"❌ Erreur lors de ls-files: {err}")
        return False
    
    print("✅ Fichiers dans l'index après reset hard:")
    print(out)
    
    # 11. Vérifier que les fichiers ont été supprimés du répertoire de travail
    print("\n11. Vérification des fichiers dans le répertoire de travail après reset hard...")
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"❌ Fichier existe encore (ne devrait pas): {file_path}")
            return False
        else:
            print(f"✅ Fichier supprimé correctement: {file_path}")
    
    print("\n=== Test terminé avec succès ===")
    return True

if __name__ == "__main__":
    success = test_reset()
    sys.exit(0 if success else 1) 