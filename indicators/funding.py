import requests

def fetch_funding():
    """
    Récupère le Funding Rate via BGeometrics API (gratuit)
    Mesure le sentiment des traders sur les marchés dérivés
    Négatif = marché majoritairement short = potentiel short squeeze
    Positif élevé = marché majoritairement long = risque de liquidation
    """
    
    print("Calcul du Funding Rate...")
    
    response = requests.get("https://bitcoin-data.com/v1/funding-rate")
    
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}")
        return None
    
    data = response.json()
    latest = data[-1]
    funding = float(latest['fundingRate'])
    date = latest['d']
    
    print(f"Date : {date}")
    print(f"Funding Rate actuel : {round(funding, 6)}")
    
    if funding < -0.001:
        print("🟢 Funding négatif — marché short, potentiel reversal haussier")
        signal = "BULLISH"
    elif funding < 0.0001:
        print("🟡 Funding neutre — marché équilibré")
        signal = "NEUTRAL"
    elif funding < 0.001:
        print("🟠 Funding légèrement positif — légère pression haussière")
        signal = "WARM"
    else:
        print("🔴 Funding très positif — marché suracheté, risque de correction")
        signal = "BEARISH"
    
    return {"funding": round(funding, 6), "signal": signal, "date": date}

if __name__ == "__main__":
    fetch_funding()