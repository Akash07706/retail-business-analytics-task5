"""
Retail Business Analytics - Task 5
Dataset: UCI Online Retail (2010-12-01 to 2011-12-09)
Run: python main.py
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "Online Retail.xlsx"
OUT = ROOT / "visualizations"
OUT.mkdir(exist_ok=True)

df = pd.read_excel(DATA)
df["InvoiceNo"] = df["InvoiceNo"].astype(str)
df["IsCancellation"] = df["InvoiceNo"].str.startswith("C")
duplicates = int(df.duplicated().sum())
missing_customer = int(df["CustomerID"].isna().sum())
missing_description = int(df["Description"].isna().sum())
clean = df.drop_duplicates()
sales = clean[
    (~clean["IsCancellation"]) &
    (clean["Quantity"] > 0) &
    (clean["UnitPrice"] > 0)
].copy()
sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]
sales["Month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

print("Rows in source:", len(df))
print("Exact duplicate rows:", duplicates)
print("Missing CustomerID:", missing_customer)
print("Missing Description:", missing_description)
print("Cancellation invoice rows:", int(df["IsCancellation"].sum()))
print("Analysis sales lines:", len(sales))
print("Revenue (GBP):", round(sales["Revenue"].sum(), 2))
print("Unique orders:", sales["InvoiceNo"].nunique())
print("Unique identified customers:", sales["CustomerID"].nunique())
print("Average order value (GBP):", round(sales["Revenue"].sum()/sales["InvoiceNo"].nunique(), 2))

monthly = sales.groupby("Month")["Revenue"].sum().sort_index()
plt.figure(figsize=(10,5))
plt.bar(monthly.index, monthly.values)
plt.title("Monthly Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (GBP)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=180)
plt.close()

countries = sales.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
plt.barh(countries.sort_values().index, countries.sort_values().values)
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (GBP)")
plt.tight_layout()
plt.savefig(OUT / "country_revenue.png", dpi=180)
plt.close()

products = sales.dropna(subset=["Description"]).groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.barh(products.sort_values().index, products.sort_values().values)
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (GBP)")
plt.tight_layout()
plt.savefig(OUT / "top_products_revenue.png", dpi=180)
plt.close()

sales.to_csv(ROOT / "cleaned_online_retail_sales.csv", index=False)
print("Outputs saved in:", OUT)
