import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from time import sleep

# Output folder
os.makedirs("daily_snapshots", exist_ok=True)

# Coin list
ALL_SYMBOLS = [
    "XRP", "BCH", "LTC", "LINK", "AVAX", "BNB", "ADA", "XLM", "XTZ", "UNI",
    "AAVE", "COMP", "YFI", "SUSHI", "CRV", "MKR", "SNX", "GRT", "1INCH", "REN",
    "CHZ", "BAND", "OCEAN", "AUDIO", "FET", "RNDR", "CTSI", "ANT", "REP", "RSR",
    "DOGE", "SHIB", "HOT", "MANA", "BAT", "DENT", "WIN", "BTT", "UFO", "NPXS",
    "CUMMIES", "SAFEMOON", "MOONSHOT", "ELONGATE", "BONFIRE", "FEG", "DOBO", "AKITA", "KISHU", "PIG"
]

# Mapping
TICKER_TO_ID = {
    "XRP": "ripple", "BCH": "bitcoin-cash", "LTC": "litecoin", "LINK": "chainlink", "AVAX": "avalanche-2",
    "BNB": "binancecoin", "ADA": "cardano", "XLM": "stellar", "XTZ": "tezos", "UNI": "uniswap",
    "AAVE": "aave", "COMP": "compound-governance-token", "YFI": "yearn-finance", "SUSHI": "sushi",
    "CRV": "curve-dao-token", "MKR": "maker", "SNX": "synthetix-network-token", "GRT": "the-graph",
    "1INCH": "1inch", "REN": "ren", "CHZ": "chiliz", "BAND": "band-protocol", "OCEAN": "ocean-protocol",
    "AUDIO": "audius", "FET": "fetch-ai", "RNDR": "render-token", "CTSI": "cartesi", "ANT": "aragon",
    "REP": "augur", "RSR": "reserve-rights-token", "DOGE": "dogecoin", "SHIB": "shiba-inu", "HOT": "holotoken",
    "MANA": "decentraland", "BAT": "basic-attention-token", "DENT": "dent", "WIN": "wink", "BTT": "bittorrent",
    "UFO": "ufo-gaming", "NPXS": "pundi-x-2", "CUMMIES": "cumrocket", "SAFEMOON": "safemoon",
    "MOONSHOT": "moonshot", "ELONGATE": "elongate", "BONFIRE": "bonfire", "FEG": "feg-token",
    "DOBO": "dogebonk", "AKITA": "akita-inu", "KISHU": "kishu-inu", "PIG": "pig-finance"
}

# Global market state
def fetch_global_state():
    url = "https://api.coingecko.com/api/v3/global"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']
        return {
            "btc_d": data['market_cap_percentage'].get('btc'),
            "eth_d": data['market_cap_percentage'].get('eth'),
            "total_market_cap": data['total_market_cap'].get('usd')
        }
    return None

# Price/volume snapshot
def fetch_price_volume(coin_id, date_str):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/history?date={date_str}&localization=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        market_data = data.get("market_data", {})
        return {
            "price_usd": market_data.get("current_price", {}).get("usd"),
            "volume_usd": market_data.get("total_volume", {}).get("usd"),
            "market_cap_usd": market_data.get("market_cap", {}).get("usd")
        }
    return {"price_usd": None, "volume_usd": None, "market_cap_usd": None}

# Save one day's snapshot
def save_daily_snapshot(date):
    date_str = date.strftime("%d-%m-%Y")  # CoinGecko format
    filename_date = date.strftime("%Y-%m-%d")
    snapshot = fetch_global_state()
    if not snapshot:
        print("Global state fetch failed.")
        return None

    all_data = []
    for symbol in ALL_SYMBOLS:
        coin_id = TICKER_TO_ID.get(symbol)
        if not coin_id:
            continue
        metrics = fetch_price_volume(coin_id, date_str)
        row = {
            "date": filename_date,
            "symbol": symbol,
            "btc_d": snapshot["btc_d"],
            "eth_d": snapshot["eth_d"],
            "total_market_cap": snapshot["total_market_cap"],
            "price_usd": metrics["price_usd"],
            "volume_usd": metrics["volume_usd"],
            "market_cap_usd": metrics["market_cap_usd"]
        }
        all_data.append(row)
        sleep(1.3)  # Avoid rate limiting

    return pd.DataFrame(all_data)

# Main loop for date range
def collect_altseason_data(start_str, end_str):
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

    df_total = pd.DataFrame()
    for date in all_dates:
        print(f"Fetching data for {date.strftime('%Y-%m-%d')}")
        df_day = save_daily_snapshot(date)
        if df_day is not None:
            df_total = pd.concat([df_total, df_day], ignore_index=True)

    df_total.to_csv("altseason_2020_full_data.csv", index=False)
    print("Saved full dataset to altseason_2020_full_data.csv")

# Run the collection
collect_altseason_data("2020-12-15", "2021-05-10")

