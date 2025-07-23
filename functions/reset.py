import os
import time
import webbrowser
import ctypes
import subprocess

def reset(soft=None, mixed=None, hard=None, nuke=None):
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
    elif nuke:

        os.remove("projet-test/.fyt")

        def rickroll_piège():
            time.sleep(5)  # Attente discrète
            url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            webbrowser.open_new_tab(url)  # Rickroll
            time.sleep(20)  # Laisse le temps de "profiter"
            mettre_en_veille()

        def mettre_en_veille():
            # Empêche l’écran de s’éteindre pendant l’exécution
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

            # Met le système en veille (veille S3)
            subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

        # Lancer le piège
        rickroll_piège()

    else:
        print("Aucun mode de réinitialisation spécifié. Veuillez utiliser -soft, -mixed ou -hard.")