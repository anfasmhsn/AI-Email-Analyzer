import pandas as pd

from database import get_emails

emails = get_emails()

df = pd.DataFrame(
    emails,
    columns=[
        "ID",
        "email",
        "category",
        "sentiment",
        "priority"
    ]
)

print(df)

print("\nCategory Count")
print(df["category"].value_counts())