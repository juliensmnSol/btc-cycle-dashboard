# BTC Cycle Bottom Detector 🔴🟡🟢

> Système de détection des bottoms de cycle Bitcoin basé sur des indicateurs on-chain et techniques, pour timer les entrées long terme sur SOL et ETH.

![Score](https://img.shields.io/badge/Score%20actuel-36.4%2F100-yellow)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Objectif

Les bottoms de cycle BTC sont les meilleures fenêtres d'entrée pour des positions long terme sur **Solana (SOL)** et **Ethereum (ETH)**, qui affichent historiquement un beta de 2x à 5x par rapport à BTC en phase de recovery.

Ce dashboard agrège 5 indicateurs en un **score 0-100** pour signaler ces fenêtres d'entrée de manière objective et automatisée.

---

## 📊 Indicateurs utilisés

| Indicateur | Poids | Source | Logique |
|-----------|-------|--------|---------|
| NUPL | 30% | BGeometrics | < 0 = capitulation historique |
| MVRV Z-Score | 25% | BGeometrics | < 0 = marché sous-évalué |
| Puell Multiple | 20% | BGeometrics | < 0.5 = mineurs sous pression |
| RSI 1W | 15% | CoinGecko | < 30 = survente |
| Funding Rate | 10% | BGeometrics | Négatif = marché short |

**Score < 25 → Signal d'accumulation**
**Score > 75 → Zone de danger**

---

## 🏗️ Architecture
```
btc-cycle-dashboard/
├── data/
│   ├── fetch_price.py      # Prix BTC via CoinGecko
│   └── fetch_rsi.py        # Calcul RSI
├── indicators/
│   ├── nupl.py             # Net Unrealized Profit/Loss
│   ├── mvrv.py             # MVRV Z-Score
│   ├── puell.py            # Puell Multiple
│   └── funding.py          # Funding Rate
├── dashboard/
│   └── app.py              # Interface Plotly Dash
├── alerts/
│   └── telegram.py         # Alertes automatiques
└── scoring.py              # Score agrégé 0-100
```

---

## 🚀 Installation
```bash
# Cloner le repository
git clone https://github.com/juliensmnSol/btc-cycle-dashboard.git
cd btc-cycle-dashboard

# Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Installer les dépendances
pip install pandas requests plotly dash python-dotenv schedule

# Configurer les variables d'environnement
cp .env.example .env
# Remplir TELEGRAM_TOKEN et TELEGRAM_CHAT_ID dans .env
```

---

## ▶️ Utilisation
```bash
# Lancer le score
python scoring.py

# Lancer le dashboard
python dashboard/app.py
# → Ouvrir http://127.0.0.1:8050

# Lancer les alertes Telegram
python alerts/telegram.py
```

---

## 📈 Interprétation du score

| Score | Signal | Action |
|-------|--------|--------|
| 0 - 25 | 🟢 Accumulation | Entrée long terme justifiée |
| 25 - 45 | 🟡 Recovery | Accumulation progressive |
| 45 - 65 | 🟡 Neutre | Attendre |
| 65 - 80 | 🟠 Chaleur | Prudence |
| 80 - 100 | 🔴 Top | Réduire les positions |

---

## 🔍 Backtesting

Les indicateurs ont été validés sur les cycles précédents :

- **Novembre 2022** — Score bas → Bottom à 15 500$ ✅
- **Mars 2020** — Score bas → Bottom à 3 800$ ✅  
- **Décembre 2018** — Score bas → Bottom à 3 200$ ✅

---

## ⚠️ Disclaimer

Ce projet est à visée éducative et ne constitue pas un conseil en investissement. Les performances passées ne garantissent pas les résultats futurs.

---

## 👤 Auteur

**Julien** — Étudiant en école de commerce passionné par l'intersection entre finance et data.

[![GitHub](https://img.shields.io/badge/GitHub-juliensmnSol-black)](https://github.com/juliensmnSol)