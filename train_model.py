from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(X_train, y_train)

print("✅ Model Trained Successfully!")

accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)


predictions = model.predict(X_test)

print("\nPrediction Results")
print("------------------")

for actual, predicted in zip(y_test, predictions):
    print(f"Actual: {actual:20} Predicted: {predicted}")


from sklearn.metrics import classification_report

print("\nClassification Report")
print("---------------------")

print(classification_report(y_test, predictions))


import joblib
import os

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("✅ Model Saved Successfully!")