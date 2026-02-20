"""
src/visualizations.py
All plotting functions for UPI Transaction Analysis.
Uses matplotlib + seaborn with a consistent dark theme.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np
import os

# ── Global Style ──────────────────────────────────────────────────────────────
DARK_BG   = "#0d1117"
CARD_BG   = "#161b22"
GRID_CLR  = "#21262d"
TEXT_CLR  = "#e6edf3"
MUTED_CLR = "#8b949e"
ACCENT    = "#58a6ff"
ACCENT2   = "#3fb950"
DANGER    = "#f85149"
WARN      = "#d29922"
PALETTE   = ["#58a6ff","#3fb950","#d29922","#f85149","#bc8cff","#79c0ff","#56d364","#ffa657"]

def set_style():
    plt.rcParams.update({
        "figure.facecolor":  DARK_BG,
        "axes.facecolor":    CARD_BG,
        "axes.edgecolor":    GRID_CLR,
        "axes.labelcolor":   TEXT_CLR,
        "axes.titlecolor":   TEXT_CLR,
        "axes.titlesize":    13,
        "axes.titleweight":  "bold",
        "axes.titlepad":     14,
        "axes.grid":         True,
        "grid.color":        GRID_CLR,
        "grid.linewidth":    0.6,
        "xtick.color":       MUTED_CLR,
        "ytick.color":       MUTED_CLR,
        "xtick.labelsize":   9,
        "ytick.labelsize":   9,
        "legend.facecolor":  CARD_BG,
        "legend.edgecolor":  GRID_CLR,
        "legend.labelcolor": TEXT_CLR,
        "legend.fontsize":   9,
        "text.color":        TEXT_CLR,
        "font.family":       "monospace",
    })

set_style()

def savefig(fig, name: str, output_dir: str = "outputs"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    print(f"  ✅ Saved → {path}")
    return path


# ─────────────────────────────────────────────
# PLOT 1 – Overview KPI Banner
# ─────────────────────────────────────────────
def plot_kpi_banner(info: dict, output_dir="outputs"):
    fig, axes = plt.subplots(1, 5, figsize=(18, 3))
    fig.suptitle("UPI TRANSACTION ANALYSIS  ·  2024", fontsize=15, fontweight="bold",
                 color=TEXT_CLR, y=1.02, x=0.5, ha="center")

    kpis = [
        ("Total Transactions", f"{info['total_transactions']:,}",         ACCENT),
        ("Total Spend",        f"₹{info['total_spend']/100000:.2f}L",     ACCENT2),
        ("Avg Transaction",    f"₹{info['avg_transaction']:,.0f}",         WARN),
        ("Fraud Rate",         f"{info['fraud_rate_pct']}%",              DANGER),
        ("Flagged Txns",       f"{info['flagged_count']}",                DANGER),
    ]
    for ax, (label, val, color) in zip(axes, kpis):
        ax.set_facecolor(CARD_BG)
        for spine in ax.spines.values():
            spine.set_edgecolor(color + "55")
        ax.text(0.5, 0.62, val,   transform=ax.transAxes, ha="center", va="center",
                fontsize=26, fontweight="bold", color=color)
        ax.text(0.5, 0.22, label, transform=ax.transAxes, ha="center", va="center",
                fontsize=9, color=MUTED_CLR, fontweight="normal")
        ax.set_xticks([]); ax.set_yticks([])

    plt.tight_layout()
    return savefig(fig, "01_kpi_banner.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 2 – Monthly Spend Trend
# ─────────────────────────────────────────────
def plot_monthly_trend(monthly_df: pd.DataFrame, output_dir="outputs"):
    fig, ax = plt.subplots(figsize=(14, 5))
    x  = range(len(monthly_df))
    y  = monthly_df["total_spend"] / 1000
    ax.fill_between(x, y, alpha=0.15, color=ACCENT)
    ax.plot(x, y, color=ACCENT, linewidth=2.5, marker="o", markersize=6, markerfacecolor=DARK_BG, markeredgecolor=ACCENT, markeredgewidth=2)

    # Annotate max
    idx = y.idxmax()
    ax.annotate(f"₹{y[idx]:.1f}k", xy=(idx, y[idx]), xytext=(idx, y[idx]+5),
                ha="center", color=ACCENT2, fontsize=9, fontweight="bold")

    ax.set_xticks(list(x))
    ax.set_xticklabels(monthly_df["month_name"].str[:3], fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v:.0f}k"))
    ax.set_title("Monthly Spending Trend (Jan–Dec 2024)")
    ax.set_xlabel("Month"); ax.set_ylabel("Total Spend (₹ thousands)")
    plt.tight_layout()
    return savefig(fig, "02_monthly_trend.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 3 – Category Breakdown (Donut + Bar)
# ─────────────────────────────────────────────
def plot_category_breakdown(cat_df: pd.DataFrame, output_dir="outputs"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Donut
    wedges, texts, autotexts = ax1.pie(
        cat_df["total_spend"], labels=None,
        colors=PALETTE[:len(cat_df)],
        autopct="%1.1f%%", pctdistance=0.75,
        wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2),
        startangle=90
    )
    for at in autotexts:
        at.set(fontsize=8, color=TEXT_CLR)
    ax1.legend(cat_df["category"], loc="lower left", fontsize=8, framealpha=0.3, ncol=2)
    ax1.set_title("Spend Share by Category")

    # Horizontal bar
    bars = ax2.barh(cat_df["category"], cat_df["total_spend"]/1000,
                    color=PALETTE[:len(cat_df)], edgecolor=DARK_BG, height=0.65)
    for bar, val in zip(bars, cat_df["total_spend"]/1000):
        ax2.text(val + 1, bar.get_y() + bar.get_height()/2,
                 f"₹{val:.1f}k", va="center", fontsize=8, color=TEXT_CLR)
    ax2.set_title("Total Spend per Category (₹ thousands)")
    ax2.set_xlabel("Total Spend (₹k)")
    ax2.invert_yaxis()
    plt.tight_layout()
    return savefig(fig, "03_category_breakdown.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 4 – Top Merchants
# ─────────────────────────────────────────────
def plot_top_merchants(merchant_df: pd.DataFrame, output_dir="outputs"):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(merchant_df))]
    bars = ax.barh(merchant_df["merchant"], merchant_df["total_spend"]/1000,
                   color=colors, edgecolor=DARK_BG, height=0.6)
    for bar, val in zip(bars, merchant_df["total_spend"]/1000):
        ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f"₹{val:.1f}k", va="center", fontsize=9, color=TEXT_CLR)
    ax.set_title("Top 10 Merchants by Total Spend")
    ax.set_xlabel("Total Spend (₹ thousands)")
    ax.invert_yaxis()
    plt.tight_layout()
    return savefig(fig, "04_top_merchants.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 5 – Day of Week Pattern
# ─────────────────────────────────────────────
def plot_dayofweek(dow_df: pd.DataFrame, output_dir="outputs"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    colors = [ACCENT2 if d in ["Saturday","Sunday"] else ACCENT for d in dow_df["day_of_week"]]
    ax1.bar(dow_df["day_of_week"].str[:3], dow_df["total_spend"]/1000, color=colors, edgecolor=DARK_BG, width=0.6)
    ax1.set_title("Total Spend by Day of Week")
    ax1.set_ylabel("Total Spend (₹k)")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"₹{v:.0f}k"))

    ax2.bar(dow_df["day_of_week"].str[:3], dow_df["count"], color=colors, edgecolor=DARK_BG, width=0.6)
    ax2.set_title("Transaction Count by Day of Week")
    ax2.set_ylabel("Number of Transactions")

    plt.tight_layout()
    return savefig(fig, "05_dayofweek_pattern.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 6 – Hourly Activity Heatmap
# ─────────────────────────────────────────────
def plot_hourly_heatmap(df: pd.DataFrame, output_dir="outputs"):
    pivot = df.groupby(["day_of_week","hour"])["amount"].count().unstack(fill_value=0)
    order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    pivot = pivot.reindex([d for d in order if d in pivot.index])

    fig, ax = plt.subplots(figsize=(18, 5))
    sns.heatmap(pivot, ax=ax, cmap="Blues", linewidths=0.3, linecolor=DARK_BG,
                annot=True, fmt="d", annot_kws={"size": 7},
                cbar_kws={"label": "Transaction Count"})
    ax.set_title("Transaction Activity Heatmap  (Day × Hour)")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week")
    plt.tight_layout()
    return savefig(fig, "06_hourly_heatmap.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 7 – Fraud Analysis Dashboard
# ─────────────────────────────────────────────
def plot_fraud_dashboard(df: pd.DataFrame, hourly_df: pd.DataFrame,
                          monthly_fraud: pd.DataFrame, output_dir="outputs"):
    fig = plt.figure(figsize=(18, 10))
    fig.suptitle("FRAUD DETECTION ANALYSIS", fontsize=15, fontweight="bold",
                 color=DANGER, y=1.01)

    gs = fig.add_gridspec(2, 3, hspace=0.45, wspace=0.4)

    # (A) Fraud vs Normal Pie
    ax1 = fig.add_subplot(gs[0, 0])
    fraud_counts = df["status"].value_counts()
    ax1.pie(fraud_counts, labels=fraud_counts.index, colors=[ACCENT2, DANGER],
            autopct="%1.1f%%", wedgeprops=dict(edgecolor=DARK_BG, linewidth=2),
            startangle=90, pctdistance=0.75)
    ax1.set_title("Transaction Status Split")

    # (B) Flagged by Hour
    ax2 = fig.add_subplot(gs[0, 1:])
    ax2.bar(hourly_df["hour"], hourly_df["count"], label="Normal", color=ACCENT, alpha=0.5, width=0.8)
    ax2.bar(hourly_df["hour"], hourly_df["flagged"], label="Flagged", color=DANGER, width=0.8)
    ax2.set_title("Flagged Transactions by Hour of Day")
    ax2.set_xlabel("Hour"); ax2.set_ylabel("Count")
    ax2.legend()
    ax2.set_xticks(range(0, 24, 2))

    # (C) Fraud by Month
    ax3 = fig.add_subplot(gs[1, :2])
    x = range(len(monthly_fraud))
    w = 0.35
    ax3.bar([i - w/2 for i in x], monthly_fraud["transaction_count"], width=w,
            label="Total", color=ACCENT, alpha=0.7)
    ax3.bar([i + w/2 for i in x], monthly_fraud["flagged"], width=w,
            label="Flagged", color=DANGER)
    ax3.set_xticks(list(x))
    ax3.set_xticklabels(monthly_fraud["month_name"].str[:3], fontsize=8)
    ax3.set_title("Total vs Flagged Transactions by Month")
    ax3.legend()

    # (D) Amount Distribution: Fraud vs Normal
    ax4 = fig.add_subplot(gs[1, 2])
    normal_amounts = df[df["is_fraud"]==0]["amount"]
    fraud_amounts  = df[df["is_fraud"]==1]["amount"]
    ax4.hist(normal_amounts, bins=30, alpha=0.6, color=ACCENT,  label="Normal", density=True)
    ax4.hist(fraud_amounts,  bins=15, alpha=0.8, color=DANGER, label="Flagged", density=True)
    ax4.set_title("Amount Distribution: Fraud vs Normal")
    ax4.set_xlabel("Amount (₹)"); ax4.set_ylabel("Density")
    ax4.legend()

    plt.tight_layout()
    return savefig(fig, "07_fraud_dashboard.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 8 – Payment Mode & Bank Analysis
# ─────────────────────────────────────────────
def plot_payment_mode(df: pd.DataFrame, output_dir="outputs"):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    mode_df = df.groupby("payment_mode")["amount"].agg(["count","sum"]).reset_index()
    axes[0].bar(mode_df["payment_mode"], mode_df["count"], color=PALETTE[:3], edgecolor=DARK_BG)
    axes[0].set_title("Transactions by Payment Mode")
    axes[0].set_ylabel("Count")

    bank_df = df.groupby("sender_bank")["amount"].sum().sort_values(ascending=False).reset_index()
    axes[1].bar(bank_df["sender_bank"], bank_df["amount"]/1000, color=PALETTE, edgecolor=DARK_BG)
    axes[1].set_title("Total Spend by Sender Bank (₹k)")
    axes[1].set_ylabel("Total Spend (₹k)")
    axes[1].tick_params(axis="x", rotation=30)

    plt.tight_layout()
    return savefig(fig, "08_payment_mode_bank.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 9 – Anomaly Score Distribution
# ─────────────────────────────────────────────
def plot_anomaly_scores(df: pd.DataFrame, output_dir="outputs"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.hist(df[df["is_fraud"]==0]["anomaly_score"], bins=30, color=ACCENT,  alpha=0.7, label="Normal",  density=True)
    ax1.hist(df[df["is_fraud"]==1]["anomaly_score"], bins=15, color=DANGER, alpha=0.8, label="Flagged", density=True)
    ax1.axvline(70, color=WARN, linestyle="--", linewidth=1.5, label="Risk Threshold (70)")
    ax1.set_title("Anomaly Score Distribution")
    ax1.set_xlabel("Anomaly Score (0–100)")
    ax1.set_ylabel("Density")
    ax1.legend()

    # Top 20 risky transactions
    top_risky = df.nlargest(20, "anomaly_score")[["transaction_id","merchant","amount","anomaly_score","is_fraud"]]
    colors = [DANGER if f else ACCENT for f in top_risky["is_fraud"]]
    ax2.barh(top_risky["merchant"] + " (" + top_risky["transaction_id"] + ")",
             top_risky["anomaly_score"], color=colors, edgecolor=DARK_BG)
    ax2.set_title("Top 20 High-Risk Transactions")
    ax2.set_xlabel("Anomaly Score")
    ax2.invert_yaxis()
    ax2.tick_params(axis="y", labelsize=7)

    plt.tight_layout()
    return savefig(fig, "09_anomaly_scores.png", output_dir)


# ─────────────────────────────────────────────
# PLOT 10 – State-wise Spend
# ─────────────────────────────────────────────
def plot_state_spend(state_df: pd.DataFrame, output_dir="outputs"):
    fig, ax = plt.subplots(figsize=(12, 5))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(state_df))]
    bars = ax.bar(state_df["state"], state_df["total_spend"]/1000, color=colors, edgecolor=DARK_BG, width=0.65)
    for bar, val in zip(bars, state_df["total_spend"]/1000):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"₹{val:.0f}k", ha="center", va="bottom", fontsize=8, color=TEXT_CLR)
    ax.set_title("Total UPI Spend by State")
    ax.set_ylabel("Total Spend (₹ thousands)")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    return savefig(fig, "10_state_spend.png", output_dir)
