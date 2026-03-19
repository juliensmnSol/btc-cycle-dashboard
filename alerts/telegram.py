import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from scoring import calculate_score
from data.fetch_onchain import load_cache
from data.fetch_rsi import fetch_rsi

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200

def interpret_nupl(v):
    if v < 0: return "Capitulation — zone de bottom historique"
    elif v < 0.25: return "Espoir — debut de recovery"
    elif v < 0.5: return "Optimisme"
    elif v < 0.75: return "Confiance/anxiete"
    else: return "Euphorie — zone de top"

def interpret_mvrv(v):
    if v < 0: return "Marche sous-evalue — opportunite historique"
    elif v < 2: return "Zone neutre — marche sain"
    elif v < 5: return "Zone de chaleur — prudence"
    else: return "Zone de top — danger"

def interpret_puell(v):
    if v < 0.5: return "Mineurs sous pression — zone de bottom"
    elif v < 1: return "Mineurs en legere pression"
    elif v < 2: return "Mineurs profitables — normal"
    elif v < 4: return "Mineurs tres profitables — prudence"
    else: return "Mineurs en euphorie — zone de top"

def interpret_rsi(v):
    if v < 30: return "Survente — potentiel bottom"
    elif v > 70: return "Surachat — potentiel top"
    else: return "Neutre"

def interpret_funding(v):
    if v < -0.001: return "Marche majoritairement short — potentiel reversal"
    elif v < 0.0001: return "Marche equilibre"
    elif v < 0.001: return "Legere pression haussiere"
    else: return "Marche suracheté — risque correction"

def check_and_alert():
    print("Verification du score BTC...")
    score = calculate_score()
    
    if score is None:
        return
    
    cache = load_cache()
    rsi = fetch_rsi()
    
    nupl    = cache.get("nupl")
    mvrv    = cache.get("mvrv")
    puell   = cache.get("puell")
    funding = cache.get("funding")

    # Zone globale
    if score < 25:
        zone = "SIGNAL D'ACCUMULATION — Entree justifiee sur BTC/SOL/ETH"
    elif score < 45:
        zone = "ZONE DE RECOVERY — Accumulation progressive possible"
    elif score < 65:
        zone = "ZONE NEUTRE — Pas de signal fort"
    elif score < 80:
        zone = "ZONE DE CHALEUR — Prudence recommandee"
    else:
        zone = "ZONE DE TOP — Reduire les positions"

    message = (
        f"<b>BTC Cycle Bottom Detector</b>\n"
        f"Mis a jour le : {cache.get('last_updated')}\n"
        f"{'='*30}\n\n"
        
        f"<b>SCORE FINAL : {score}/100</b>\n"
        f"{zone}\n\n"
        
        f"{'='*30}\n"
        f"<b>Detail des indicateurs</b>\n\n"
        
        f"<b>NUPL</b> ({round(nupl, 3)}) — poids 30%\n"
        f"{interpret_nupl(nupl)}\n\n"
        
        f"<b>MVRV Z-Score</b> ({round(mvrv, 3)}) — poids 25%\n"
        f"{interpret_mvrv(mvrv)}\n\n"
        
        f"<b>Puell Multiple</b> ({round(puell, 3)}) — poids 20%\n"
        f"{interpret_puell(puell)}\n\n"
        
        f"<b>RSI 1W</b> ({round(rsi, 2)}) — poids 15%\n"
        f"{interpret_rsi(rsi)}\n\n"
        
        f"<b>Funding Rate</b> ({round(funding, 6)}) — poids 10%\n"
        f"{interpret_funding(funding)}"
    )
    
    if send_message(message):
        print("Message Telegram envoye !")
    else:
        print("Erreur envoi Telegram")

if __name__ == "__main__":
    check_and_alert()