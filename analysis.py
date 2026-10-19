"""
Mission 4, Business Decision, CEO £100 challenge and bonus 3/4.
Run AFTER scraper.py has produced competitor_books.csv:   python analysis.py
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

csv = sys.argv[1] if len(sys.argv) > 1 else "competitor_books.csv"
df = pd.read_csv(csv)
print(f"Rows: {len(df)}   Columns: {list(df.columns)}\n")

# ---------------- Mission 4: seven questions ----------------
print("1. Most expensive:", df.loc[df.Price.idxmax(), ["Title", "Price"]].tolist())
print("2. Cheapest:      ", df.loc[df.Price.idxmin(), ["Title", "Price"]].tolist())
print(f"3. Average price:  £{df.Price.mean():.2f}")
print("4. 5-star books:  ", int((df.Rating == 5).sum()))
in_stock_pct = df.Availability.str.contains("In stock", case=False).mean() * 100
print(f"5. In stock:       {in_stock_pct:.1f}%")
print("6. Top 5 highest-rated (ties broken by lower price; many books share 5 stars):")
print(df.sort_values(["Rating", "Price"], ascending=[False, True]).head(5)[["Title", "Price", "Rating"]].to_string(index=False))
five = df[df.Rating == 5]
print("7. Cheapest 5-star:", five.loc[five.Price.idxmin(), ["Title", "Price"]].tolist(), "\n")

# ---------------- CEO £100 challenge: 0/1 knapsack (exact optimum) ----------------
# Weight = price in pence, value = rating, capacity = 10,000 pence.
cap = 10000
w = (df.Price * 100).round().astype(int).to_numpy()
v = df.Rating.to_numpy()
n = len(df)
best = np.zeros(cap + 1, dtype=np.int32)
keep = np.zeros((n, cap + 1), dtype=bool)
for i in range(n):
    wi, vi = w[i], v[i]
    if wi > cap:
        continue
    cand = best[: cap + 1 - wi] + vi
    better = cand > best[wi:]
    keep[i, wi:] = better
    best[wi:] = np.where(better, cand, best[wi:])
c, chosen = cap, []
for i in range(n - 1, -1, -1):
    if keep[i, c]:
        chosen.append(i)
        c -= w[i]
pick = df.iloc[chosen[::-1]][["Title", "Price", "Rating"]]
print("CEO £100 CHALLENGE (optimal)")
print(pick.to_string(index=False))
print(f"Books: {len(pick)}   Total cost: £{pick.Price.sum():.2f}   Total rating score: {pick.Rating.sum()}\n")

# ---------------- Bonus 3 + 4: rating counts and bar chart ----------------
counts = df.Rating.value_counts().sort_index()
print("Books per rating level:\n", counts.to_string(), "\n")
ax = counts.plot(kind="bar", color="#3b6ea5", edgecolor="none", figsize=(6, 4))
ax.set_xlabel("Star rating")
ax.set_ylabel("Number of books")
ax.set_title("Competitor books by star rating")
ax.bar_label(ax.containers[0])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("rating_counts.png", dpi=150)
print("Saved rating_counts.png")

# Evidence for the recommendation
print("\nAverage price by rating:\n", df.groupby("Rating").Price.mean().round(2).to_string())
cheap_top = df[(df.Rating >= 4) & (df.Price < df.Price.mean())]
print(f"\nBooks rated 4+ and priced below average: {len(cheap_top)} ({len(cheap_top)/len(df):.0%} of catalogue)")
