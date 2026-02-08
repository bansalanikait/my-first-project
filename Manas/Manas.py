import pandas as pd

df = pd.read_csv("phishing_site_urls.csv")

# Step 1 — Convert column to normal object
df[df.columns[1]] = df[df.columns[1]].astype(str)

# Step 2 — Replace labels
df[df.columns[1]] = df[df.columns[1]].replace({
    "good": 1,
    "bad": -1
})

# Step 3 — Convert to integer
df[df.columns[1]] = df[df.columns[1]].astype("int8")

df.to_csv("new.csv", index=False)