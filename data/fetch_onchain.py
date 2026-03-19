import requests
import json
import time
import os
from datetime import datetime

CACHE_FILE = "data/onchain_cache.json"

def fetch_all_onchain():
    """
    Récupère tous les indicateurs on-chain en une seule session
    et les sauvegarde en cache local.
    Appelé une fois par jour maximum.
    """
    
    print("Récupération des données on-chain...")
    
    endpoints = {
        "nupl":     ("https://bitcoin-data.com/v1/nupl", "nupl"),
        "mvrv":     ("https://bitcoin-data.com/v1/mvrv-zscore", "mvrvZscore"),
        "puell":    ("https://bitcoin-data.com/v1/puell-multiple", "puellMultiple"),
        "funding":  ("https://bitcoin-data.com/v1/funding-rate", "fundingRate"),
    }
    
    cache = {}
    
    for name, (url, key) in endpoints.items():
        print(f"  Récupération {name}...")
        for attempt in range(3):
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    cache[name] = float(data[-1][key])
                    print(f"  {name} : {cache[name]}")
                    break
                elif r.status_code == 429:
                    print(f"  Rate limit, attente 30s...")
                    time.sleep(30)
                else:
                    print(f"  Erreur {r.status_code}")
                    cache[name] = None
                    break
            except Exception as e:
                print(f"  Erreur : {e}")
                cache[name] = None
        
        # Pause entre chaque indicateur
        time.sleep(5)
    
    # Ajoute la date de mise à jour
    cache["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Sauvegarde dans le cache
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)
    
    print(f"\nCache sauvegardé : {CACHE_FILE}")
    print(f"Mis à jour le : {cache['last_updated']}")
    return cache

def load_cache():
    """
    Charge le cache local.
    Si le cache a plus de 24h ou n'existe pas, le rafraîchit automatiquement.
    """
    
    if not os.path.exists(CACHE_FILE):
        print("Pas de cache trouvé, récupération des données...")
        return fetch_all_onchain()
    
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
    
    # Vérifie si le cache date de plus de 24h
    last_updated = datetime.strptime(cache["last_updated"], "%Y-%m-%d %H:%M")
    hours_old = (datetime.now() - last_updated).total_seconds() / 3600
    
    if hours_old > 24:
        print(f"Cache de {round(hours_old, 1)}h, rafraîchissement...")
        return fetch_all_onchain()
    
    print(f"Cache chargé (mis à jour il y a {round(hours_old, 1)}h)")
    return cache

if __name__ == "__main__":
    fetch_all_onchain()