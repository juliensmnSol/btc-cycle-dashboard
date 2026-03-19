import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.fetch_onchain import load_cache
from data.fetch_rsi import fetch_rsi
import requests

def get_indicator(url, key):
    """Garde cette fonction pour le dashboard uniquement"""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return float(r.json()[-1][key])
    except:
        pass
    return None

def calculate_score():
    print("=" * 40)
    print("   BTC CYCLE BOTTOM DETECTOR")
    print("=" * 40)

    # Charge depuis le cache local — pas d'appel API
    cache = load_cache()
    rsi = fetch_rsi()

    nupl    = cache.get("nupl")
    mvrv    = cache.get("mvrv")
    puell   = cache.get("puell")
    funding = cache.get("funding")

    print(f"\nNUPL          : {nupl}")
    print(f"MVRV Z-Score  : {mvrv}")
    print(f"Puell Multiple: {puell}")
    print(f"Funding Rate  : {funding}")
    print(f"RSI           : {rsi}")
    print(f"Mis à jour le : {cache.get('last_updated')}")

    if not all([nupl, mvrv, puell, funding]):
        print("\n❌ Données indisponibles")
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