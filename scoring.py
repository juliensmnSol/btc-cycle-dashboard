import requests
import time
from data.fetch_rsi import fetch_rsi

def get_indicator(url, key):
    """Récupère un indicateur avec retry automatique"""
    for i in range(3):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                return float(data[-1][key])
            time.sleep(10)
        except:
            time.sleep(10)
    return None

def calculate_score():
    print("=" * 40)
    print("   BTC CYCLE BOTTOM DETECTOR")
    print("=" * 40)
    print("Récupération des données (patiente 30s)...")

    nupl    = get_indicator("https://bitcoin-data.com/v1/nupl", "nupl")
    time.sleep(5)
    mvrv    = get_indicator("https://bitcoin-data.com/v1/mvrv-zscore", "mvrvZscore")
    time.sleep(5)
    puell   = get_indicator("https://bitcoin-data.com/v1/puell-multiple", "puellMultiple")
    time.sleep(5)
    funding = get_indicator("https://bitcoin-data.com/v1/funding-rate", "fundingRate")
    time.sleep(5)
    rsi     = fetch_rsi()

    print(f"\nNUPL          : {nupl}")
    print(f"MVRV Z-Score  : {mvrv}")
    print(f"Puell Multiple: {puell}")
    print(f"Funding Rate  : {funding}")
    print(f"RSI           : {rsi}")

    if not all([nupl, mvrv, puell, funding]):
        print("\n❌ Données indisponibles, réessaie dans 5 minutes")
        return None

    nupl_score    = max(0, min(100, (nupl + 1) / 2 * 100))
    mvrv_score    = max(0, min(100, (mvrv + 2) / 12 * 100))
    puell_score   = max(0, min(100, (puell - 0.3) / 4.7 * 100))
    rsi_score     = rsi
    funding_score = max(0, min(100, (funding + 0.003) / 0.006 * 100))

    score = round(
        nupl_score    * 0.30 +
        mvrv_score    * 0.25 +
        puell_score   * 0.20 +
        rsi_score     * 0.15 +
        funding_score * 0.10, 1
    )

    print(f"\nSCORE FINAL : {score}/100")

    if score < 25:
        print("🟢 SIGNAL D'ACCUMULATION — Entrée justifiée sur BTC/SOL/ETH")
    elif score < 45:
        print("🟡 ZONE DE RECOVERY — Accumulation progressive possible")
    elif score < 65:
        print("🟡 ZONE NEUTRE — Pas de signal fort")
    elif score < 80:
        print("🟠 ZONE DE CHALEUR — Prudence")
    else:
        print("🔴 ZONE DE TOP — Danger")

    print("=" * 40)
    return score

if __name__ == "__main__":
    calculate_score()