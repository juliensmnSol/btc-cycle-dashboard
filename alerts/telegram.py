import requests
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scoring import calculate_score

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message):
    """Envoie un message sur Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def check_and_alert():
    """
    Calcule le score et envoie une alerte si nécessaire
    Cette fonction sera appelée automatiquement toutes les 24h
    """
    print("Vérification du score BTC...")
    score = calculate_score()
    
    if score is None:
        return
    
    if score < 25:
        message = (
            "🟢 <b>SIGNAL D'ACCUMULATION BTC</b>\n\n"
            f"Score cycle : <b>{score}/100</b>\n\n"
            "Les indicateurs on-chain signalent une zone de bottom.\n"
            "→ Entrée long terme sur BTC/SOL/ETH justifiée.\n\n"
            "<i>Dashboard : http://127.0.0.1:8050</i>"
        )
        if send_message(message):
            print("✅ Alerte Telegram envoyée !")
        else:
            print("❌ Erreur envoi Telegram")
    elif score > 75:
        message = (
            "🔴 <b>ALERTE TOP DE CYCLE BTC</b>\n\n"
            f"Score cycle : <b>{score}/100</b>\n\n"
            "Les indicateurs signalent une zone de danger.\n"
            "→ Réduire ou sortir les positions.\n\n"
            "<i>Dashboard : http://127.0.0.1:8050</i>"
        )
        if send_message(message):
            print("✅ Alerte Telegram envoyée !")
    else:
        print(f"Score {score}/100 — pas d'alerte nécessaire")

if __name__ == "__main__":
    check_and_alert()