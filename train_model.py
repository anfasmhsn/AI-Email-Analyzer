import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("data/training_data.csv")

X = df["email"]
y = df["category"]


vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

print(df.head())
print(X_vector.shape)