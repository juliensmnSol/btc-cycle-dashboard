import requests

def fetch_puell():
    """
    Récupère le Puell Multiple via BGeometrics API (gratuit)
    Mesure la pression de vente des mineurs
    Zones : < 0.5 = bottom, > 4 = top
    """
    
    print("Calcul du Puell Multiple...")
    
    response = requests.get("https://bitcoin-data.com/v1/puell-multiple")
    
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        return None
    
    data = response.json()
    latest = data[-1]
    puell = float(latest['puellMultiple'])
    date = latest['d']
    
    print(f"Date : {date}")
    print(f"Puell Multiple actuel : {round(puell, 4)}")
    
    if puell < 0.5:
        print("🟢 Mineurs sous pression — zone de bottom")
        signal = "BOTTOM"
    elif puell < 1:
        print("🟡 Mineurs en légère pression — zone saine")
        signal = "NEUTRAL"
    elif puell < 2:
        print("🟡 Mineurs profitables — marché normal")
        signal = "NORMAL"
    elif puell < 4:
        print("🟠 Mineurs très profitables — prudence")
        signal = "WARM"
    else:
        print("🔴 Mineurs en euphorie — zone de top")
        signal = "TOP"
    
    return {"puell": round(puell, 4), "signal": signal, "date": date}

if __name__ == "__main__":
    fetch_puell()