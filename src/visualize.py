import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'..\data\output.csv')

# Clean and convert to float
df['price_increase_clean'] = (
    df['price_increase']
    .astype(str)
    .str.replace('+', '', regex=False)
    .str.replace('%', '', regex=False)
    .str.replace(',', '.', regex=False)
    .str.replace('/', '', regex=False)
    .str.strip()
)

# Convert to numeric (invalid strings -> NaN)
df['price_increase_clean'] = pd.to_numeric(df['price_increase_clean'], errors='coerce')
print(df[['price_increase', 'price_increase_clean']].head(99))
print(df['price_increase_clean'].describe())

# Convert the date column to datetime
df['date_str'] = pd.to_datetime(df['date_str'], errors='coerce')
print(df['date_str'])

# Optional cutoff date
cutoff_date = '2025-01-01'
if cutoff_date:
    cutoff_date = pd.to_datetime(cutoff_date)
    df = df[df['date_str'] >= cutoff_date]

print(f"Number of listings after {cutoff_date.date()}: {len(df)}")

bins = [
    -25, -22.5, -20, -17.5, -15, -12.5, -10, -7.5, -5, -2.5, 0,
     2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30,
     32.5, 35, 37.5, 40, 42.5, 45, 47.5, 50
]
labels = [
    '-25–-22.5%', '-22.5–-20%', '-20–-17.5%', '-17.5–-15%', '-15–-12.5%', '-12.5–-10%',
    '-10–-7.5%', '-7.5–-5%', '-5–-2.5%', '-2.5–0%',
    '0–2.5%', '2.5–5%', '5–7.5%', '7.5–10%', '10–12.5%', '12.5–15%',
    '15–17.5%', '17.5–20%', '20–22.5%', '22.5–25%', '25–27.5%', '27.5–30%',
    '30–32.5%', '32.5–35%', '35–37.5%', '37.5–40%', '40–42.5%', '42.5–45%',
    '45–47.5%', '47.5–50%'
]

df['price_range'] = pd.cut(df['price_increase_clean'], bins=bins, labels=labels, right=False)

counts = df['price_range'].value_counts().sort_index()
print(counts)

plt.figure(figsize=(8,5))
counts.plot(kind='bar')

plt.title('Distribution of Price Increases (%)')
plt.xlabel('Price Increase Range')
plt.ylabel('Number of Listings')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
