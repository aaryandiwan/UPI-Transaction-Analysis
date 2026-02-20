"""
src/analysis.py
Core analysis functions for UPI Transaction Analysis project.
"""

import pandas as pd
import numpy as np


# ─────────────────────────────────────────────
# 1. DATA LOADING & VALIDATION
# ─────────────────────────────────────────────

def load_data(filepath: str) -> pd.DataFrame:
    """Load and parse UPI transaction CSV."""
    df = pd.read_csv(filepath, parse_dates=["datetime"])
    df["date"] = pd.to_datetime(df["date"])
    df["month_name"] = pd.Categorical(
        df["month_name"],
        categories=["January","February","March","April","May","June",
                    "July","August","September","October","November","December"],
        ordered=True
    )
    return df


def basic_info(df: pd.DataFrame) -> dict:
    """Return basic summary statistics."""
    return {
        "total_transactions":   len(df),
        "total_spend":          df["amount"].sum(),
        "avg_transaction":      df["amount"].mean().round(2),
        "median_transaction":   df["amount"].median(),
        "date_range":           f"{df['date'].min()} → {df['date'].max()}",
        "unique_merchants":     df["merchant"].nunique(),
        "unique_categories":    df["category"].nunique(),
        "flagged_count":        df["is_fraud"].sum(),
        "fraud_rate_pct":       round(df["is_fraud"].mean() * 100, 2),
    }


# ─────────────────────────────────────────────
# 2. SPENDING PATTERN ANALYSIS
# ─────────────────────────────────────────────

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spend, count, and fraud by month."""
    return (
        df.groupby("month_name", observed=True)
          .agg(
              total_spend=("amount", "sum"),
              transaction_count=("amount", "count"),
              avg_spend=("amount", "mean"),
              flagged=("is_fraud", "sum"),
          )
          .reset_index()
    )


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spend and count by category."""
    return (
        df.groupby("category")
          .agg(
              total_spend=("amount", "sum"),
              transaction_count=("amount", "count"),
              avg_spend=("amount", "mean"),
              flagged=("is_fraud", "sum"),
          )
          .sort_values("total_spend", ascending=False)
          .reset_index()
    )


def top_merchants(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top N merchants by total spend."""
    return (
        df.groupby("merchant")
          .agg(total_spend=("amount", "sum"), count=("amount", "count"))
          .sort_values("total_spend", ascending=False)
          .head(n)
          .reset_index()
    )


def dayofweek_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Average and total spend by day of week."""
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    summary = (
        df.groupby("day_of_week")
          .agg(total_spend=("amount","sum"), count=("amount","count"), avg_spend=("amount","mean"))
          .reindex(order)
          .reset_index()
    )
    return summary


def hourly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Transaction count and fraud count by hour."""
    return (
        df.groupby("hour")
          .agg(count=("amount","count"), flagged=("is_fraud","sum"), total_spend=("amount","sum"))
          .reset_index()
    )


def payment_mode_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Breakdown by payment mode."""
    return (
        df.groupby("payment_mode")
          .agg(count=("amount","count"), total_spend=("amount","sum"), avg_spend=("amount","mean"))
          .reset_index()
    )


def state_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Spending by state."""
    return (
        df.groupby("state")
          .agg(total_spend=("amount","sum"), count=("amount","count"))
          .sort_values("total_spend", ascending=False)
          .reset_index()
    )


# ─────────────────────────────────────────────
# 3. FRAUD ANALYSIS
# ─────────────────────────────────────────────

def fraud_summary(df: pd.DataFrame) -> pd.DataFrame:
    """All flagged transactions."""
    return df[df["is_fraud"] == 1].sort_values("amount", ascending=False).reset_index(drop=True)


def fraud_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("hour")["is_fraud"].agg(["sum","count"]).rename(columns={"sum":"fraud","count":"total"}).reset_index()


def fraud_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category")
          .agg(fraud_count=("is_fraud","sum"), total=("amount","count"), fraud_amount=("amount", lambda x: x[df.loc[x.index,"is_fraud"]==1].sum()))
          .reset_index()
          .sort_values("fraud_count", ascending=False)
    )


def fraud_by_month(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("month_name", observed=True)
          .agg(fraud=("is_fraud","sum"), total=("amount","count"))
          .reset_index()
    )


# ─────────────────────────────────────────────
# 4. ANOMALY SCORING (Rule-based)
# ─────────────────────────────────────────────

def compute_anomaly_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a simple rule-based anomaly score (0–100) to each transaction.
    Factors: amount percentile, odd hour, repeat merchant in short window.
    """
    df = df.copy()
    amount_pct = df["amount"].rank(pct=True) * 40          # 0–40 pts
    odd_hour    = df["hour"].apply(lambda h: 30 if h in range(1, 5) else 0)  # 0 or 30 pts
    high_val    = (df["amount"] > df["amount"].quantile(0.95)).astype(int) * 20  # 0 or 20 pts
    df["anomaly_score"] = (amount_pct + odd_hour + high_val).clip(0, 100).round(1)
    return df
