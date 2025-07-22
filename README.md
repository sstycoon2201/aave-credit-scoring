# File Structure

aave-credit-scoring/
│
├── wallet_credit_score.py
│   ↳ Main Python script that:
│     - Loads the transaction JSON
│     - Extracts wallet-level features
│     - Calculates credit scores
│     - Saves scores and analysis results
│
├── transactions.json
│   ↳ Sample or full input dataset (raw Aave V2 transactions).
│     - Each item is a transaction record with wallet, action type, timestamp, amount, and asset info.
│
├── wallet_scores.json
│   ↳ Output file mapping wallet addresses to their credit scores (0–1000).
│
├── score_buckets.json
│   ↳ Bucket-wise count of how many wallets fall into each 100-point score range.
│     - Used to analyze score distribution across users.
│
├── score_distribution.png
│   ↳ Bar chart visualization of wallet credit score distribution.
│     - Helpful for quick understanding of data spread and extremes.
│
├── README.md
│   ↳ This file.
│     - Describes the project, pipeline, scoring method, features, and how to run everything.
│
├── analysis.md
│   ↳ Analysis of wallet scores.
│     - Includes behavioral trends for low vs high score wallets
│     - Shows score distribution using the plot
│     - Explains how to interpret the model output


# aave-credit-scoring
Internship assignment for Zeru AI engineering Internship

# 🧠 Aave V2 Wallet Credit Scoring Model

This project builds a machine learning-inspired wallet credit scoring model using **DeFi transaction-level data** from the **Aave V2 protocol**. The aim is to analyze on-chain behavior and assign a **credit score between 0 and 1000** to each wallet address, reflecting how responsibly it interacts with the protocol.

---

## 📌 Problem Statement

The goal is to build a wallet credit scoring system based on historical Aave transactions. Each record represents a wallet's action such as `deposit`, `borrow`, `repay`, `redeemunderlying`, or `liquidationcall`.

We score each wallet using behavioral patterns — e.g., repayments vs. borrowings, frequency of liquidations, and overall usage quality. Higher scores indicate responsible usage; lower scores indicate risky or exploitative behavior.

---

## ⚙️ Method & Architecture

### 💾 Data Input

- A JSON file (`transactions.json`) containing ~100K raw Aave V2 transactions
- Each record includes:
  - Wallet address
  - Action type (e.g., deposit, borrow)
  - Timestamp
  - Transaction amount
  - Asset price in USD

---

### 🏗️ Processing Pipeline

1. **Load and Parse JSON Data** using `pandas`
2. **Group Records by Wallet**
3. **Feature Engineering**:
    - Total deposits, borrows, repayments
    - USD value of all financial actions
    - Number of liquidations
    - Repay-to-borrow ratio
    - Active days
4. **Scoring Algorithm**:
    - Start with base score: 500
    - Increase score for:
        - Higher repayment ratios
        - Higher deposits
        - More active days
    - Penalize for:
        - Liquidations
        - High borrowing without repayment
5. **Output**: 
    - A final JSON file (`wallet_scores.json`) mapping each wallet to a score between 0 and 1000.

---

## 📈 Features Used for Scoring

| Feature | Description |
|--------|-------------|
| `num_deposits` | Number of deposit transactions |
| `deposit_usd` | Total USD value deposited |
| `num_borrow` | Number of borrow actions |
| `borrow_usd` | Total USD borrowed |
| `num_repay` | Number of repayment actions |
| `repay_usd` | Total USD repaid |
| `repay_to_borrow_ratio` | Repay amount / Borrow amount |
| `num_liquidations` | Number of liquidation events |
| `unique_days` | Number of unique days active |

---

## 🧮 How to Run

### Requirements

- Python 3.x
- pandas
- matplotlib

Install dependencies:
```bash
pip install pandas matplotlib


