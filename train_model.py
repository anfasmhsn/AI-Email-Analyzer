import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("data/training_data.csv")

X = df["email"]
y = df["category"]


vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

print(df.head())
print(X_vector.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_vector,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Data:", X_train.shape)
print("Testing Data :", X_test.shape)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(X_train, y_train)

print("✅ Model Trained Successfully!")

accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)

import joblib
import os

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("✅ Model Saved Successfully!")