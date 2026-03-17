import json
import pandas as pd

def calculate_rsi(prices, period=14):
    """
    Calcule le RSI (Relative Strength Index)
    period = 14 par défaut, mais on l'utilisera avec 7 pour simuler le 1W
    
    Le RSI mesure la force des hausses vs les baisses
    - Au dessus de 70 = surachat (potentiel top)
    - En dessous de 30 = survente (potentiel bottom)
    """
    
    # On convertit la liste de prix en Series pandas
    # pandas est une librairie qui permet de manipuler des données comme un tableau Excel
    series = pd.Series(prices)
    
    # On calcule la différence entre chaque jour et le précédent
    delta = series.diff()
    
    # On sépare les jours positifs (hausses) et négatifs (baisses)
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # On calcule la moyenne des hausses et des baisses sur la période
    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()
    
    # RS = ratio entre la force des hausses et des baisses
    rs = avg_gain / avg_loss
    
    # RSI = formule finale qui donne une valeur entre 0 et 100
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def fetch_rsi():
    """
    Charge les prix BTC sauvegardés et calcule le RSI
    """
    
    print("Calcul du RSI...")
    
    # On charge le fichier JSON qu'on a créé avec fetch_price.py
    with open("data/btc_price.json", "r") as f:
        data = json.load(f)
    
    # Les prix sont dans data['prices'], chaque entrée = [timestamp, prix]
    # On extrait uniquement les prix (index 1)
    prices = [entry[1] for entry in data['prices']]
    
    # On calcule le RSI sur 7 périodes (équivalent hebdomadaire sur données daily)
    rsi_values = calculate_rsi(prices, period=7)
    
    # On affiche le RSI actuel (dernière valeur)
    current_rsi = round(rsi_values.iloc[-1], 2)
    print(f"RSI actuel : {current_rsi}")
    
    # Interprétation
    if current_rsi < 30:
        print("🟢 RSI en zone de survente — signal potentiel de bottom")
    elif current_rsi > 70:
        print("🔴 RSI en zone de surachat — attention au top")
    else:
        print("🟡 RSI neutre")
    
    return current_rsi

if __name__ == "__main__":
    fetch_rsi()