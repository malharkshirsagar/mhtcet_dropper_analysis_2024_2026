import pandas as pd

# Load your dataset
df = pd.read_csv("verified_droppers_only.csv", dtype=str)

# Remove rows where student full name is empty, NaN, or just whitespace
df_clean = df.dropna(subset=["student full name"])
df_clean = df_clean[df_clean["student full name"].str.strip() != ""]

# Save back out
df_clean.to_csv("matched_dropper_percentiles_clean.csv", index=False)
print(f"Dropped {len(df) - len(df_clean)} empty-name rows.")
