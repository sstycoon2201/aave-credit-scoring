import json
import pandas as pd
from collections import defaultdict
from datetime import datetime

# Load transaction data from JSON file
with open('transactions.json', 'r') as f:
    data = json.load(f)

# Convert JSON to DataFrame
records = []
for tx in data:
    record = {
        'wallet': tx['userWallet'],
        'action': tx['action'].lower(),
        'amount': float(tx['actionData'].get('amount', 0)) / 1e6,  # assuming USDC/USDT 6 decimals
        'asset_price': float(tx['actionData'].get('assetPriceUSD', 1)),
        'timestamp': tx['timestamp']
    }
    record['usd_value'] = record['amount'] * record['asset_price']
    records.append(record)

df = pd.DataFrame(records)

# Group transactions by wallet
wallets = df['wallet'].unique()
scores = {}

for wallet in wallets:
    user_df = df[df['wallet'] == wallet].sort_values('timestamp')
    score = 500  # start with neutral base score

    num_deposits = len(user_df[user_df['action'] == 'deposit'])
    deposit_usd = user_df[user_df['action'] == 'deposit']['usd_value'].sum()

    num_borrow = len(user_df[user_df['action'] == 'borrow'])
    borrow_usd = user_df[user_df['action'] == 'borrow']['usd_value'].sum()

    num_repay = len(user_df[user_df['action'] == 'repay'])
    repay_usd = user_df[user_df['action'] == 'repay']['usd_value'].sum()

    num_liquidations = len(user_df[user_df['action'] == 'liquidationcall'])

    total_txn = len(user_df)
    unique_days = len(set([datetime.utcfromtimestamp(ts).date() for ts in user_df['timestamp']]))
    repay_to_borrow = (repay_usd / borrow_usd) if borrow_usd > 0 else 1

    # --- Scoring logic ---
    if borrow_usd > 0:
        score += min(repay_to_borrow, 1.5) * 200  # encourage full repayment
    if num_liquidations > 0:
        score -= min(num_liquidations * 50, 200)  # penalize liquidations
    if deposit_usd > 0:
        score += min(deposit_usd / 1000, 5) * 20  # reward large deposits
    if unique_days > 1:
        score += min(unique_days, 30) * 2  # reward active wallets

    # Bound the score between 0 and 1000
    score = max(0, min(1000, round(score)))

    scores[wallet] = score

# Print or save scores
print("Wallet Scores:\n")
for wallet, score in scores.items():
    print(f"{wallet}: {score}")

# Optionally save to JSON
with open("wallet_scores.json", "w") as f:
    json.dump(scores, f, indent=2)

import matplotlib.pyplot as plt

# --- Create Bucket Stats (e.g., 0–100, 100–200, ..., 900–1000) ---
bucket_ranges = [(i, i+100) for i in range(0, 1000, 100)]
bucket_counts = {f"{start}-{end}": 0 for start, end in bucket_ranges}

for score in scores.values():
    for start, end in bucket_ranges:
        if start <= score < end:
            bucket_counts[f"{start}-{end}"] += 1
            break
    if score == 1000:  # Handle edge case for max score
        bucket_counts["900-1000"] += 1

# --- Plot Score Distribution Graph ---
plt.figure(figsize=(10, 6))
plt.bar(bucket_counts.keys(), bucket_counts.values(), color="skyblue", edgecolor="black")
plt.title("Wallet Credit Score Distribution")
plt.xlabel("Score Range")
plt.ylabel("Number of Wallets")
plt.xticks(rotation=45)
plt.tight_layout()

# Save plot
plt.savefig("score_distribution.png")
print("\n📊 Score distribution graph saved as 'score_distribution.png'.")

# Save bucket stats as JSON
with open("score_buckets.json", "w") as f:
    json.dump(bucket_counts, f, indent=2)

print("\n📁 Bucket stats saved to 'score_buckets.json'")
