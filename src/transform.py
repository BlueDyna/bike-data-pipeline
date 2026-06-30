import json
import glob
import pandas as pd

# combine all raw files we've collected so far
all_records = []
for filepath in glob.glob("raw/telraam_*.json"):
    with open(filepath) as f:
        data = json.load(f)
    all_records.extend(data["report"])

df = pd.DataFrame(all_records)

print("Kolommen in de data:", list(df.columns))

# alleen kolommen behouden die geen lijsten/dicts bevatten (bv. geen speed histograms)
simple_cols = [col for col in df.columns if not df[col].apply(lambda x: isinstance(x, (list, dict))).any()]
df = df[simple_cols]

# basic cleanup
df["date"] = pd.to_datetime(df["date"])
df = df.drop_duplicates()
df = df.fillna(0)

print(df.head())
print(f"Total rows: {len(df)}")

df.to_csv("transformed.csv", index=False)