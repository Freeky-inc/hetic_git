import os

def log():
    if not os.path.exists('projet-test/.fyt'):
        print("Aucun dépôt Fyt trouvé dans le répertoire actuel.")
        return

    with open('projet-test/.fyt/HEAD', 'r') as head_file:
        ref = head_file.read().strip()
    
    if ref.startswith('ref:'):
        ref = ref.split(' ')[1]
    
    commit_file = os.path.join('projet-test/.fyt', ref)
    
    if not os.path.exists(commit_file):
        print("Aucun commit trouvé.")
        return
    
    with open(commit_file, 'r') as file:
        commits = file.readlines()
    
    for commit in commits:
        print(commit.strip())