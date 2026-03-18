import requests

def fetch_mvrv():
    """
    Récupère le MVRV Z-Score via BGeometrics API (gratuit)
    Zones : < 0 = bottom, > 7 = top
    """
    
    print("Calcul du MVRV Z-Score...")
    
    response = requests.get("https://bitcoin-data.com/v1/mvrv-zscore")
    
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        return None
    
    data = response.json()
    latest = data[-1]
    mvrv = float(latest['mvrvZscore'])
    date = latest['d']
    
    print(f"Date : {date}")
    print(f"MVRV Z-Score actuel : {round(mvrv, 4)}")
    
    if mvrv < 0:
        print("🟢 Zone de bottom — opportunité historique")
        signal = "BOTTOM"
    elif mvrv < 2:
        print("🟡 Zone neutre — marché sain")
        signal = "NEUTRAL"
    elif mvrv < 5:
        print("🟠 Zone de chaleur — prudence")
        signal = "WARM"
    else:
        print("🔴 Zone de top — euphorie dangereuse")
        signal = "TOP"
    
    return {"mvrv": round(mvrv, 4), "signal": signal, "date": date}

if __name__ == "__main__":
    fetch_mvrv()