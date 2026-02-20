"""
UPI Transaction Dataset Generator
Generates a realistic synthetic dataset for analysis.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

CATEGORIES = [
    "Food & Dining", "Shopping", "Transport", "Utilities",
    "Entertainment", "Healthcare", "Education", "Travel"
]

MERCHANTS = {
    "Food & Dining":   ["Swiggy", "Zomato", "McDonald's", "Domino's", "Cafe Coffee Day", "Blinkit", "BigBasket"],
    "Shopping":        ["Amazon", "Flipkart", "Myntra", "Meesho", "Nykaa", "Ajio", "Snapdeal"],
    "Transport":       ["Ola", "Uber", "Rapido", "Metro Card", "IRCTC", "RedBus", "InDrive"],
    "Utilities":       ["BESCOM", "Airtel", "Jio", "BWSSB", "Gas Agency", "Vi", "BSNL"],
    "Entertainment":   ["Netflix", "Hotstar", "BookMyShow", "Spotify", "YouTube Premium", "ZEE5", "SonyLIV"],
    "Healthcare":      ["PharmEasy", "1mg", "Apollo Pharmacy", "Medlife", "Netmeds", "Practo"],
    "Education":       ["Coursera", "Udemy", "BYJU'S", "Unacademy", "WhiteHat Jr", "Vedantu"],
    "Travel":          ["MakeMyTrip", "Goibibo", "OYO", "Airbnb", "Cleartrip", "EaseMyTrip"],
}

STATES = [
    "Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Telangana",
    "Gujarat", "Rajasthan", "Uttar Pradesh", "West Bengal", "Madhya Pradesh"
]

PAYMENT_MODES = ["UPI ID", "QR Code", "Phone Number"]
BANKS = ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB", "Canara", "BOB"]

def generate_dataset(n=1000):
    dates = pd.date_range("2024-01-01", "2024-12-31", periods=n)
    dates = dates + pd.to_timedelta(np.random.randint(0, 86400, n), unit='s')
    dates = dates.sort_values()

    categories = np.random.choice(CATEGORIES, n, p=[0.22, 0.20, 0.15, 0.12, 0.10, 0.08, 0.07, 0.06])
    merchants  = [np.random.choice(MERCHANTS[c]) for c in categories]

    # Amount distribution per category
    amount_params = {
        "Food & Dining":   (300, 150),
        "Shopping":        (1200, 800),
        "Transport":       (180, 100),
        "Utilities":       (600, 300),
        "Entertainment":   (350, 150),
        "Healthcare":      (500, 400),
        "Education":       (2000, 1500),
        "Travel":          (3500, 2500),
    }
    amounts = []
    for c in categories:
        mu, sigma = amount_params[c]
        val = int(max(50, np.random.normal(mu, sigma)))
        amounts.append(val)

    hours = dates.hour

    # Fraud detection: anomalous = very high amount + odd hours (1–5 AM)
    is_fraud = np.array([
        (amt > 5000 and hr in range(1, 5)) or
        (amt > 7000 and np.random.rand() < 0.4) or
        (amt > 4000 and hr in range(2, 4) and np.random.rand() < 0.3)
        for amt, hr in zip(amounts, hours)
    ])

    statuses = np.where(is_fraud, "Flagged", "Success")

    df = pd.DataFrame({
        "transaction_id":   [f"TXN{str(i+1).zfill(5)}" for i in range(n)],
        "date":             dates.date,
        "time":             dates.time,
        "datetime":         dates,
        "month":            dates.month,
        "month_name":       dates.strftime("%B"),
        "day_of_week":      dates.day_name(),
        "hour":             hours,
        "category":         categories,
        "merchant":         merchants,
        "amount":           amounts,
        "payment_mode":     np.random.choice(PAYMENT_MODES, n, p=[0.50, 0.30, 0.20]),
        "sender_bank":      np.random.choice(BANKS, n),
        "receiver_bank":    np.random.choice(BANKS, n),
        "state":            np.random.choice(STATES, n),
        "status":           statuses,
        "is_fraud":         is_fraud.astype(int),
    })

    return df


if __name__ == "__main__":
    df = generate_dataset(1000)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/upi_transactions.csv", index=False)
    print(f"✅ Dataset generated: {len(df)} transactions")
    print(df.head())
