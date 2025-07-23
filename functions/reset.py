import os
import time
import ctypes
from moviepy import VideoFileClip
import pygame
import shutil
import cv2
import threading
import time
import numpy




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
    
    elif nuke:
        # shutil.rmtree("projet-test")
        # print("Nuke activé. Tous les fichiers du dépôt sont supprimés.")

        def nuking():
            time.sleep(2)
            
            try:
                clip = VideoFileClip("C:\\Users\\marti\\Documents\\GitHub\\hetic_git\\functions\\nuke.mp4")

                pygame.init()
                screen = pygame.display.set_mode(clip.size, pygame.FULLSCREEN)
                pygame.display.set_caption("Rickroll Time")

                pygame.mixer.init(frequency=44100, size=-16, channels=2)

                audio_path = "temp_audio.wav"
                clip.audio.write_audiofile(audio_path, logger=None)

                sound = pygame.mixer.Sound(audio_path)

                def play_audio():
                    sound.play()

                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()

                clock = pygame.time.Clock()
                for frame in clip.iter_frames(fps=clip.fps, dtype="uint8"):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

                    surface = pygame.surfarray.make_surface(numpy.swapaxes(frame, 0, 1))
                    screen.blit(surface, (0, 0))
                    pygame.display.update()
                    clock.tick(clip.fps)

                pygame.quit()
            
            except Exception as e:
                cap = cv2.VideoCapture("C:\\Users\\marti\\Documents\\GitHub\\hetic_git\\functions\\nuke.mp4")

                cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    cv2.imshow("Video", frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()  # Attente discrète
            time.sleep(10)
            mettre_en_veille()

        def mettre_en_veille():
            # Empêche l’écran de s’éteindre pendant l’exécution
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

            # Met le système en veille (veille S3)
            subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

        # Lancer le piège
        nuking()

    else:
        print("Aucun mode de réinitialisation spécifié. Veuillez utiliser -soft, -mixed ou -hard.")