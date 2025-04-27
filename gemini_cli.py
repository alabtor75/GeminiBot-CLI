# Gemini Assistant CLI
# (C) 2025 Soufianne Nassibi
# Licensed under GNU General Public License v3.0
# See LICENSE file for more information.

import google.generativeai as genai
import datetime
import os
import time
import webbrowser
import re
from cryptography.fernet import Fernet


# Fonction d'affichage couleur
def print_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

# === CONFIGURATION ===
CONFIG_FILE = "config.txt"
KEY_FILE = "key.key"
MODEL_NAME = "gemini-2.0-flash-lite"

BASE_DIR = os.path.join(os.getenv('APPDATA'), 'GeminiBot_CLI')
HISTORY_DIR = os.path.join(BASE_DIR, "history")
HISTORY_FILE = os.path.join(HISTORY_DIR, f"gemini_history_{datetime.date.today()}.txt")

os.makedirs(HISTORY_DIR, exist_ok=True)

# === CRYPTAGE CLÉ API ===
def load_encryption_key():
    key_path = os.path.join(BASE_DIR, KEY_FILE)
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
    else:
        with open(key_path, "rb") as f:
            key = f.read()
    return key

fernet = Fernet(load_encryption_key())

# === GESTION CLÉ API ===
def save_api_key(api_key):
    config_path = os.path.join(BASE_DIR, CONFIG_FILE)
    encrypted_api_key = fernet.encrypt(api_key.encode())
    with open(config_path, "wb") as f:
        f.write(encrypted_api_key)

def get_api_key(force_change=False):
    config_path = os.path.join(BASE_DIR, CONFIG_FILE)
    if os.path.exists(config_path) and not force_change:
        with open(config_path, "rb") as f:
            encrypted_api_key = f.read()
        decrypted_api_key = fernet.decrypt(encrypted_api_key).decode()
        return decrypted_api_key
    else:
        while True:
            print_color("\n🔑 Clé API Gemini requise.", "1;33")
            print_color("""
╔═════════════════════════════╗
║        CONFIGURATION        ║
╠═════════════════════════════╣
║ 1. 🔐 Entrer votre clé API  ║
║ 2. 🌐 Créer une clé API     ║
║ 3. 🚪 Quitter               ║
╚═════════════════════════════╝
""", "1;35")
            choix = input("\033[1;34m> Que voulez-vous faire ? (1/2/3) : \033[0m").strip()
            if choix == "1":
                api_key = input("\033[1;33m> Entrez votre clé API Gemini : \033[0m").strip()
                if api_key:
                    save_api_key(api_key)
                    print_color("\n✅ Clé API enregistrée avec succès !", "1;32")
                    time.sleep(1)
                    return api_key
                else:
                    print_color("❌ Clé invalide. Réessayez.", "1;31")
            elif choix == "2":
                print_color("\n🌐 Ouverture du site pour créer une clé API...", "1;32")
                webbrowser.open("https://aistudio.google.com/app/apikey")
            elif choix == "3":
                print_color("\n👋 Sortie du programme.", "1;33")
                input("Appuyez sur Entrée pour quitter...")
                exit()
            else:
                print_color("❌ Choix invalide. Tapez 1, 2 ou 3.", "1;31")

# === CONFIGURATION GEMINI ===
api_key = get_api_key()
genai.configure(api_key=api_key)

# === FONCTIONS ===
def save_history(question, answer):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] Question: {question}\n")
        f.write(f"[{now}] Réponse: {answer}\n\n")

def ask_gemini(question):
    model = genai.GenerativeModel(MODEL_NAME)
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Erreur API : {e}"

def print_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def format_response(response):
    if re.search(r'```', response) or re.search(r'\n', response):
        return f"""
╭────────────────────────────╮
{response.strip()}
╰────────────────────────────╯
"""
    else:
        return f"\n💬 {response.strip()}\n"

def lire_historique():
    if not os.path.exists(HISTORY_FILE):
        print_color("Aucun historique pour aujourd'hui.", "1;33")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        print_color("\n===== HISTORIQUE DU JOUR =====\n", "1;36")
        print(content)
        print_color("===== FIN HISTORIQUE =====\n", "1;36")

def supprimer_historique():
    if os.path.exists(HISTORY_FILE):
        confirm = input("\n⚠️ Êtes-vous sûr de vouloir supprimer l'historique ? (o/n) : ").strip().lower()
        if confirm == "o":
            os.remove(HISTORY_FILE)
            print_color("🧹 Historique supprimé avec succès.\n", "1;32")
        else:
            print_color("❎ Suppression annulée.\n", "1;33")
    else:
        print_color("Aucun historique à supprimer.\n", "1;33")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_header():
    clear_screen()
    loading_text = "Chargement"
    for i in range(4):
        clear_screen()
        print_color(f"{loading_text}{'.' * i}", "1;33")
        time.sleep(0.5)
    clear_screen()
    print_color(r"""
   ____ _____ __  __ ___ _   _ ___    ____ _     ___ 
  / ___| ____|  \/  |_ _| \ | |_ _|  / ___| |   |_ _|
 | |  _|  _| | |\/| || ||  \| || |  | |   | |    | | 
 | |_| | |___| |  | || || |\  || |  | |___| |___ | | 
  \____|_____|_|  |_|___|_| \_|___|  \____|_____|___|

                  GEMINI-CLI  -  2025
""", "1;36")
    time.sleep(1)

# === SCRIPT PRINCIPAL ===
def menu():
    compteur_questions = 0
    afficher_header()
    while True:
        print_color("""
╔═════════════════════════════╗
║         MENU PRINCIPAL      ║
╠═════════════════════════════╣
║ 1. 💬 Poser une question    ║
║ 2. 📜 Lire l'historique     ║
║ 3. 🔑 Changer la clé API    ║
║ 4. 🧹 Effacer l'historique  ║
║ 5. 🚪 Quitter               ║
╚═════════════════════════════╝
""", "1;35")
        choix = input("\033[1;34m> Que veux-tu faire ? (1/2/3/4/5) : \033[0m").strip()
        if choix == "1":
            clear_screen()
            question = input("\033[1;34m> Pose ta question : \033[0m").strip()
            if question:
                answer = ask_gemini(question)
                print_color(format_response(answer), "1;32")
                save_history(question, answer)
                compteur_questions += 1
                print_color(f"\n🧠 Total questions posées aujourd'hui : {compteur_questions}\n", "1;36")
        elif choix == "2":
            clear_screen()
            lire_historique()
        elif choix == "3":
            clear_screen()
            api_key = get_api_key(force_change=True)
            genai.configure(api_key=api_key)
            print_color("\n✅ Nouvelle clé API enregistrée et activée.", "1;32")
            time.sleep(2)
            clear_screen()
        elif choix == "4":
            clear_screen()
            supprimer_historique()
        elif choix == "5":
            print_color("\n👋 Merci d'avoir utilisé GEMINI-CLI.\n", "1;33")
            input("Appuyez sur Entrée pour quitter...")
            break
        else:
            print_color("❌ Choix invalide. Tapez 1, 2, 3, 4 ou 5.", "1;31")

# === PROTECTION D'EXÉCUTION ===
if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        print_color(f"\n❌ Erreur : {e}", "1;31")
        input("\nAppuyez sur Entrée pour fermer...")

