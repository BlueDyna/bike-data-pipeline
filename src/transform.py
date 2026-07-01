import json
import glob
import os
import pandas as pd

# ==========================
# Meest recente JSON-bestand zoeken
# ==========================

files = glob.glob("raw/telraam_*.json")

if not files:
    raise FileNotFoundError("Geen bestanden gevonden in de map 'raw/'.")

latest_file = max(files, key=os.path.getmtime)

print(f"Meest recente bestand: {latest_file}")

# ==========================
# JSON-bestand inladen
# ==========================

with open(latest_file, "r", encoding="utf-8") as f:
    data = json.load(f)

if "report" not in data:
    raise ValueError("Geen 'report'-veld gevonden in het JSON-bestand.")

df = pd.DataFrame(data["report"])

print(f"{len(df)} records ingelezen.")

# ==========================
# Enkel eenvoudige kolommen behouden
# ==========================

simple_cols = [
    col for col in df.columns
    if not df[col].apply(lambda x: isinstance(x, (list, dict))).any()
]

df = df[simple_cols]

# ==========================
# Datum verwerken
# ==========================

df["date"] = (
    pd.to_datetime(df["date"], utc=True)
      .dt.tz_convert("Europe/Brussels")
      .dt.tz_localize(None)
)

# ==========================
# Numerieke kolommen
# ==========================

exclude = ["date", "interval", "timezone"]

for col in df.columns:
    if col not in exclude:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================
# Data opschonen
# ==========================

df = df.drop_duplicates()

df = df.fillna(0)

df = df.sort_values("date")

df.reset_index(drop=True, inplace=True)

# ==========================
# Opslaan
# ==========================

df.to_csv("transformed.csv", index=False)

print("\nTransformatie voltooid.")
print(df.head())
print(f"Totaal aantal rijen: {len(df)}")