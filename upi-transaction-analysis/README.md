# 📊 UPI Transaction Analysis & Visualization

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-0.12-teal)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> A comprehensive **Exploratory Data Analysis (EDA)** project on UPI (Unified Payments Interface) transactions in India — covering spending patterns, category breakdowns, time-based trends, and fraud detection.

---

## 📌 Overview

This project analyzes **1,000 synthetic UPI transactions** (Jan–Dec 2024) to uncover:

- 📈 Monthly and weekly **spending trends**
- 🏷️ **Category-wise** breakdown (Food, Shopping, Travel, etc.)
- 🏪 **Top merchants** by transaction volume and value
- 🕐 **Time-based patterns** — hourly heatmaps, peak hours
- 🚨 **Fraud detection** — rule-based anomaly scoring
- 🗺️ **State-wise** spending distribution
- 💳 **Payment mode** and bank analysis

---

## 🗂️ Project Structure

```
upi-transaction-analysis/
│
├── 📓 notebooks/
│   └── UPI_Transaction_Analysis.ipynb    # Main analysis notebook (run in Colab)
│
├── 📁 data/
│   ├── generate_data.py                  # Synthetic dataset generator
│   └── upi_transactions.csv             # Generated dataset (1000 rows)
│
├── 📁 src/
│   ├── analysis.py                       # Core analysis & aggregation functions
│   └── visualizations.py                # All plotting functions (reusable)
│
├── 📁 outputs/                           # Auto-generated charts & CSV exports
│   ├── 01_kpi_banner.png
│   ├── 02_monthly_trend.png
│   ├── 03_category_breakdown.png
│   ├── 04_top_merchants.png
│   ├── 05_time_patterns.png
│   ├── 06_activity_heatmap.png
│   ├── 07_fraud_analysis.png
│   ├── 08_anomaly_scores.png
│   ├── 09_payment_bank.png
│   ├── 10_state_analysis.png
│   ├── 11_distributions_correlations.png
│   ├── monthly_summary.csv
│   ├── category_summary.csv
│   ├── flagged_transactions.csv
│   └── high_risk_transactions.csv
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Option A — Google Colab (Recommended)

1. Open [Google Colab](https://colab.research.google.com/)
2. Click **File → Upload notebook** and upload `notebooks/UPI_Transaction_Analysis.ipynb`
3. Run all cells — everything is self-contained!

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

---

### Option B — Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/upi-transaction-analysis.git
cd upi-transaction-analysis

# Install dependencies
pip install -r requirements.txt

# (Optional) Generate dataset
python data/generate_data.py

# Launch notebook
jupyter notebook notebooks/UPI_Transaction_Analysis.ipynb
```

---

## 📊 Visualizations

| # | Chart | Description |
|---|-------|-------------|
| 1 | KPI Banner | Total spend, avg txn, fraud rate at a glance |
| 2 | Monthly Trend | Area chart of spending across Jan–Dec |
| 3 | Category Breakdown | Donut chart + horizontal bar |
| 4 | Top Merchants | Top 10 by total spend |
| 5 | Time Patterns | Day-of-week & hourly spend/count |
| 6 | Activity Heatmap | Day × Hour transaction density |
| 7 | Fraud Dashboard | Multi-panel fraud analysis |
| 8 | Anomaly Scores | Rule-based risk scoring |
| 9 | Payment & Bank | Mode distribution + bank analysis |
| 10 | State Analysis | Geographic spend distribution |
| 11 | Distributions | Amount histograms, boxplots, correlation matrix |

---

## 🚨 Fraud Detection Logic

A **rule-based anomaly score (0–100)** is computed for each transaction:

| Factor | Weight |
|--------|--------|
| Amount percentile rank | 0–40 pts |
| Transaction in high-risk hours (1–5 AM) | +30 pts |
| Amount > 95th percentile | +20 pts |

Transactions scoring **> 70** are flagged as high-risk.

**Fraud heuristics:**
- Amount > ₹5,000 **AND** hour between 1–5 AM
- Amount > ₹7,000 (any hour)
- Amount > ₹4,000 between 2–4 AM

---

## 📈 Key Findings

- 🏆 **Travel** and **Education** categories have the highest average transaction values
- 🕑 **Peak fraud window**: 1:00 AM – 5:00 AM
- 📅 **Weekends** show higher spending on Food & Entertainment
- 💳 **UPI ID** is the most used payment mode (50%)
- 🌆 **Maharashtra** and **Karnataka** lead in total UPI spend

---

## 🛠️ Tech Stack

| Library | Usage |
|---------|-------|
| `pandas` | Data manipulation & aggregation |
| `numpy` | Numerical operations & synthetic data |
| `matplotlib` | Core plotting engine |
| `seaborn` | Heatmaps & styled charts |
| `jupyter` | Interactive notebook environment |

---

## 📝 Dataset

This project uses a **synthetically generated** dataset designed to mimic realistic UPI transaction patterns in India. It includes:

- 1,000 transactions across Jan–Dec 2024
- 8 spending categories, 50+ merchants
- 10 Indian states, 8 major banks
- Realistic fraud patterns (odd hours + high amounts)

> ⚠️ *This is synthetic data for educational purposes only.*

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

*Made with ❤️ using Python · Pandas · Matplotlib · Seaborn*
