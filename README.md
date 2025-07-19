# 🚀 Frontrunner: Altseason Rotation Timing Predictor

Frontrunner is a research and machine learning project that aims to quantify and predict capital flow dynamics during crypto market cycles. By analyzing historical bull runs, the system tracks capital rotation across asset tiers—BTC, ETH, large caps, mid caps, small caps, microcaps, and nanocaps—in order to estimate the delay (Δt) between major cycle milestones (e.g., ETH reaching 50% of ATH) and altcoin pumps. The project further models weekly capital inflows and outflows across the crypto space (CRYPTO_IN / CRYPTO_OUT), including net volume changes by tier, with the goal of training a regressor that predicts the optimal timing for rotating into high-risk, high-reward altcoins. Ultimately, Frontrunner provides a data-driven decision engine to guide entry and exit strategies across the crypto risk spectrum.

## 🧠 Project Objective

**Frontrunner** aims to build a machine learning system that analyzes previous crypto bull runs to learn the timing of capital rotation between market cap tiers:

> **BTC → ETH → Large Caps → Mid Caps → Small Caps → Microcaps**

The key goal is to estimate **Δt (delay in days)** between Ethereum reaching a percentage of its all-time-high (ATH) and the start of major price movements in altcoins of different sizes.

This enables:
- 📈 **Profit optimization** via timely entry
- 🛡️ **Risk reduction** by avoiding inactive holding phases
- 🧠 **Informed capital rotation** throughout the market cycle

---

## 📊 Core Hypothesis

- ETH ATH milestones (e.g. 10%, 30%, 50%, 100%) act as **market cycle clocks**.
- Altcoins respond to ETH’s rise in a **predictable delay pattern**.
- This delay can be modeled using dominance metrics, market cap tiers, and capital flow.

---

## 📌 Methodology

1. Fetch historical data from past bull runs (e.g., 2017, 2021).
2. Detect ETH hitting 10% to 100% of its previous ATH.
3. Identify when mid, small, and micro caps start pumping.
4. Compute `Δt` between ETH event and altcoin pump.
5. Train a machine learning regressor to learn this pattern.

---

## 🎯 Model Inputs

| Category | Features |
|----------|----------|
| **Dominance** | `BTC.D`, `ETH.D`, `OTHERS.D` |
| **Market Caps** | `TOP2`, `TOP3`, `OTHERS`, `TOTAL_MCAP` |
| **Anchors** | `ETH_pct_ATH`, `days_since_ETH_50pct` |
| **Momentum** | `Δ(BTC.D)_7d`, `Δ(OTHERS.D)_7d`, `Δ(mcap_i)_7d` |
| **Token Meta** | `market_cap`, `tier`, `log_mcap`, `narrative` |
| **Optional** | `ETH/BTC`, `DEX_volume`, `days_since_halving` |

---

## 🧪 Target Variable

- **`Δt_pump`**: Days from ETH milestone to pump of altcoin `i`

---

## 📁 Project Structure
frontrunner
├── data
│   ├── processed
│   └── raw
├── LICENSE
├── notebooks
│   └── exploratory.ipynb
├── README.md
├── requirements.txt
└── src
    ├── feature_engineer.py
    ├── fetch_data.py
    ├── labeler.py
    ├── model_train.py
    └── utils.py


---

## 🛠️ Planned Models

- `RandomForestRegressor` (baseline)
- `XGBoost` (boosted performance)
- Optional: `TemporalFusionTransformer` (sequence-aware model)

---

## ✅ Project Goals

- [ ] Build a labeled dataset of coin-level pump timings
- [ ] Train regression models to predict timing (Δt) of alt pumps
- [ ] Integrate signals for capital rotation strategy

---

## ⚠️ Considerations

- Data sparsity for microcaps in early cycles
- Pump detection must avoid false positives
- Potential for survivorship bias in dataset

---

## 💡 Vision

**Frontrunner** is designed to turn historical macro behavior into actionable intelligence for timing your entries during the next altseason — maximizing upside, minimizing drawdowns, and staying ahead of the rotation curve.

