import joblib

# Load the trained model
model = joblib.load("models/model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


def classify_email(email):

    email_vector = vectorizer.transform([email])

    prediction = model.predict(email_vector)

    return prediction[0]