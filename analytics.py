import pandas as pd

df = pd.read_csv("data/email.csv")

print(df)

print("\nCategory Count")
print(df["category"].value_counts())