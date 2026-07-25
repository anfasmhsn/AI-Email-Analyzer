import pandas as pd

# Read dataset
df = pd.read_csv("data/training_data.csv")

# Features and labels
X = df["email"]
y = df["category"]

# Vectorize
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

X_vector = vectorizer.fit_transform(X)

print(df.head())
print("Feature Matrix:", X_vector.shape)

# Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_vector,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training Data:", X_train.shape)
print("Testing Data :", X_test.shape)

# Train
from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

print("✅ Model Trained Successfully!")

# Accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# Predictions
predictions = model.predict(X_test)

print("\nPrediction Results")
print("------------------")

for actual, predicted in zip(y_test, predictions):
    print(f"Actual: {actual:20} Predicted: {predicted}")

# Save model
import joblib
import os

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("✅ Model Saved Successfully!")