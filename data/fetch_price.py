import requests
import json
import os

def fetch_btc_price():
    """
    Récupère l'historique du prix BTC sur 365 jours via CoinGecko
    CoinGecko est gratuit et ne nécessite pas de clé API
    """
    
    print("Récupération du prix BTC...")
    
    # L'URL de l'API CoinGecko
    # coin_id = bitcoin, vs_currency = usd, days = 365
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    
    # Les paramètres qu'on envoie à l'API
    params = {
        "vs_currency": "usd",
        "days": "365",
        "interval": "daily"
    }
    
    # On envoie la demande à l'API
    response = requests.get(url, params=params)
    
    # Si la réponse est correcte (code 200 = succès)
    if response.status_code == 200:
        data = response.json()
        
        # On sauvegarde les données dans un fichier JSON
        with open("data/btc_price.json", "w") as f:
            json.dump(data, f)
        
        print(f"✅ Succès ! {len(data['prices'])} jours de données récupérés")
        return data
    else:
        print(f"❌ Erreur : {response.status_code}")
        return None

# Si on lance ce fichier directement, on exécute la fonction
if __name__ == "__main__":
    fetch_btc_price()