# File Structure

aave-credit-scoring/
│
## wallet_credit_score.py
│   ↳ Main Python script that:
│     - Loads the transaction JSON
│     - Extracts wallet-level features
│     - Calculates credit scores
│     - Saves scores and analysis results
│
## transactions.json
│   ↳ Sample or full input dataset (raw Aave V2 transactions).
│     - Each item is a transaction record with wallet, action type, timestamp, amount, and asset info.
│
## wallet_scores.json
│   ↳ Output file mapping wallet addresses to their credit scores (0–1000).
│
## score_buckets.json
│   ↳ Bucket-wise count of how many wallets fall into each 100-point score range.
│     - Used to analyze score distribution across users.
│
## score_distribution.png
│   ↳ Bar chart visualization of wallet credit score distribution.
│     - Helpful for quick understanding of data spread and extremes.
│
## README.md
│   ↳ This file.
│     - Describes the project, pipeline, scoring method, features, and how to run everything.
│
├── analysis.md
│   ↳ Analysis of wallet scores.
│     - Includes behavioral trends for low vs high score wallets
│     - Shows score distribution using the plot
│     - Explains how to interpret the model output
