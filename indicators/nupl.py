import requests

def fetch_nupl():
    """
    Récupère le NUPL via BGeometrics API (gratuit, pas de clé)
    Données on-chain réelles depuis 2013
    """
    
    print("Calcul du NUPL...")
    
    response = requests.get("https://bitcoin-data.com/v1/nupl")
    
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        return None
    
    data = response.json()
    
    # On prend la dernière valeur (la plus récente)
    latest = data[-1]
    nupl = float(latest['nupl'])
    date = latest['d']
    
    print(f"Date : {date}")
    print(f"NUPL actuel : {round(nupl, 4)}")
    
    if nupl < 0:
        print("🟢 Capitulation — zone de bottom historique")
        signal = "BOTTOM"
    elif nupl < 0.25:
        print("🟡 Espoir — début de recovery")
        signal = "HOPE"
    elif nupl < 0.5:
        print("🟡 Optimisme")
        signal = "OPTIMISM"
    elif nupl < 0.75:
        print("🟠 Confiance/anxiété")
        signal = "BELIEF"
    else:
        print("🔴 Euphorie — zone de top")
        signal = "EUPHORIA"
    
    return {"nupl": round(nupl, 4), "signal": signal, "date": date}

if __name__ == "__main__":
    fetch_nupl()